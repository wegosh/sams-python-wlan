from getmac import getmac, get_mac_address
import socket
from IPy import IP
from manuf import manuf
import netifaces
import subprocess
from math import log10
import rssi
import schedule, time
import fcntl
import struct
import ipaddress
import asyncio
from datetime import datetime, timedelta
import json
import requests
import os

current_network_interface = netifaces.gateways()['default'][netifaces.AF_INET][1]
DOMAIN = "wegorz.uk"
#DOMAIN = "127.0.0.1"

async def clear_arp(ip, interface_name=''):
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
            ip_bytes = int(ipaddress.IPv4Address(ip)).to_bytes(4, byteorder='big')
            fcntl.ioctl(sock.fileno(),0x8953, struct.pack('hh48s16s', socket.AF_INET, 0, ip_bytes, interface_name[:15].encode()))
        except OSError as e:
            break
        finally:
            sock.close()
            struct.pack('hh48s16s', socket.AF_INET, 0, ip_bytes, interface_name[:15].encode())

def get_device_ip():   
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    sock_addr = sock.getsockname()[0]
    ip_addr = str(sock_addr)
    sock.close()
    return ip_addr

def get_mac_address_list(ip_address = '192.168.1.1', i_range = [1, 255], hide_empty_macs = False, hide_device_names = False) -> list:
    device_parser = manuf.MacParser(update=False)
    mac_address_list = []
    ip_parts = ip_address.split('.')
    get_device_ip()
    


    for iter in range(i_range[0], i_range[1]):

        current_ip = f'{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{iter}'
        
        mac_addr = get_mac_address(ip=current_ip, network_request=True)
        
        mac_dict = {'ip': current_ip, 'mac': mac_addr, 'device': None}
        
        if mac_addr != '00:00:00:00:00:00' and mac_addr != None:
            device_name = device_parser.get_manuf_long(str(mac_addr))
            if device_name != None:
                mac_dict['device'] = "Not Available"
                mac_address_list.append(mac_dict)
            elif(hide_device_names != True):
                mac_dict['device'] = "Not available"
                mac_address_list.append(mac_dict)
        elif(hide_empty_macs != True):
            mac_dict['mac'] = "00:00:00:00:00:00"
            mac_dict['device'] = "Not available"
            mac_address_list.append(mac_dict)
        elif(current_ip == get_device_ip()):
            mac_addr = getmac.get_mac_address( network_request=False, interface=current_network_interface)
            device_name = device_parser.get_manuf_long(str(mac_addr))
            mac_dict['ip'] = f'{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{iter}'
            mac_dict['device'] = "Not available"
            mac_dict['mac'] = mac_addr
            mac_address_list.append(mac_dict)
    #print(mac_address_list)
    print('ARP table len: ', len(mac_address_list))
    return mac_address_list

def get_all_aps():
    rssi_scanner = rssi.RSSI_Scan('enp33s0')
    ap_info = rssi_scanner.getAPinfo()
    print(ap_info)
    
last_items = []
RST_STATE = False
last_datetime_read = None


def get_user_from_api(mac_addr = "") -> int:
    global DOMAIN
    API_URL = f'https://{DOMAIN}/api/users/'
    PARAMS = {'user_device_mac': mac_addr}
    response = requests.get(url = API_URL, params = PARAMS, allow_redirects=True)
    if response.status_code < 399:
        json_response = response.json()
        print(json_response)
        for item in json_response:
            if item is not None:
                return item['id']
    else:
        print("Error during handling API call to User, status: ", response.status_code)

def get_room_from_api(mac_addr = "90:4d:4a:7f:73:67") -> int:
    global DOMAIN

    API_URL = f'https://{DOMAIN}/api/room/'
    PARAMS = {'mac_addr': mac_addr}
    response = requests.get(url = API_URL, params = PARAMS, allow_redirects=True)
    
    if response.status_code < 399:
        json_response = response.json()
        print(json_response)
        for item in json_response:
            if item is not None:
                return item['id']
    else:
        print("Error during handling API call to Room, status: ", response.status_code)



def send_data_to_api():
    global RST_STATE
    global DOMAIN
    try:
        RST_STATE = True

        with open('Attendance.json', 'r') as fp:
            attendance = json.load(fp)
            for key in attendance.keys():
                user_id = get_user_from_api(mac_addr=key)
                room_id = get_room_from_api()
                if user_id is not None and room_id is not None:
                    data = {
                        'user': user_id,
                        'room': room_id,
                        'start_attendance_dt': attendance[key]['datetime_started'],
                        'duration_in_session': timedelta(seconds = attendance[key]['duration']),
                        'end_attendance_dt': attendance[key]['datetime_end'],
                        'attendance_method': "WLA"
                    }
                    response = requests.post(f'https://{DOMAIN}/api/attendance/', data = data, allow_redirects=True)
                    print("Api responded - ", response.status_code, f'\tfor user id {user_id} and room id {room_id}')
                    if response.status_code < 399:
                        print("Response ok. Status: ", response.status_code)
                    else:
                        print("Error. Status: ", response.status_code)
                else:
                    print("User or room item does not exists")
    except IOError as e:
        print("File does not exists... ")
    finally:
        RST_STATE = False

        if os.path.exists("Attendance.json"):
            os.remove("Attendance.json")
        else:
            print("System has tried to remove the file which does not exists.") 




def write_data_to_file(dict_arr = [], duration = 0):
    now_dt = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
    if dict_arr is not None:
        try:
            with open('Attendance.json', 'r') as fp:
                attendance = json.load(fp)
                print("attendance type: ", type(attendance))
                for single_dict in dict_arr:
                    key = ""
                    for k in single_dict.keys():
                        key = k
                    if key in attendance:
                        single_dict['datetime_started'] = attendance[k]['datetime_started']
                        single_dict['duration'] = attendance[k]['duration'] + duration
                        single_dict['datetime_end'] = now_dt
                        attendance[k] = {'datetime_started': single_dict['datetime_started'], 'duration': single_dict['duration'], 'datetime_end': single_dict['datetime_end']}
                    else:
                        single_dict['datetime_started'] = now_dt
                        single_dict['duration'] = duration
                        single_dict['datetime_end'] = now_dt
                        attendance[k] = {'datetime_started': single_dict['datetime_started'], 'duration': single_dict['duration'], 'datetime_end': single_dict['datetime_end']}
                    # single_dict['duration'] += duration
                    # single_dict['datetime_end'] = now_dt

        except IOError:
            print('File with attendance session has not been found. Creating new file')
            attendance = {}
            for single_dict in dict_arr:
                key = ""
                for k in single_dict.keys():
                    key = k

                single_dict['datetime_started'] = now_dt 
                single_dict['duration'] = duration
                single_dict['datetime_end'] = now_dt
                attendance[k] = {'datetime_started': single_dict['datetime_started'], 'duration': single_dict['duration'], 'datetime_end': single_dict['datetime_end']}
            print('Attendance session file has been created')

        with open('Attendance.json', 'w') as fp:
            json.dump(attendance, fp, indent=4)


def task():
    global RST_STATE
    global last_datetime_read
    global last_items

    if RST_STATE == False or RST_STATE == True:

        devices_in_range = get_mac_address_list(get_device_ip(), i_range=[1,80], hide_empty_macs=True, hide_device_names=False) #Get all devices with mac addresses available in range of IPs
        inner_list = [] #Temporary list

        for i in range(len(devices_in_range.copy())):
            inner_list.append({devices_in_range[i]['mac']: {'datetime_started': None, 'duration': 0, 'datetime_end': None}})
        print(inner_list)
        #inner_list = list(set(inner_list))
        current_datetime_read = datetime.now()
        if last_datetime_read is None:
            last_datetime_read = current_datetime_read
        else:
            duration = datetime.now() - last_datetime_read #timedelta seconds
            write_data_to_file(dict_arr = inner_list, duration = duration.seconds)
            last_datetime_read = current_datetime_read
        
        # last = set(last_items)
        # current = set(inner_list)
        
        # if last == current:
        #     print("No changes in list")
        # else:
        #     #Do work here
        #     print("Changes in list has been detected")
        #     print('\nSymetric difference for items: ', last^current)
        #     print('\nIntersection last(curr)      : ', last.intersection(current))

        
        
        last_items = inner_list
        print("\ncurrent list: ", len(inner_list))
    else:
        print("File write or read is in progress")


async def main():
    print("Running...\n\n")
    WAIT = 3
    POPULATING_PASSES = 4
    ONE_SESSION = 6

    #arp_clear_task = asyncio.create_task(clear_arp(get_device_ip(), interface_name = current_network_interface))
    
    ts = datetime.now()
    schedule.every(5).seconds.do(task)
    schedule.every(120).seconds.do(send_data_to_api)

    #schedule.every(15).seconds.do()
    count = 0
    while(True):
        print(f'job {count}:\n')
        if count % ONE_SESSION <= POPULATING_PASSES:
            print(f'Populating ARP table - {count % ONE_SESSION} pass...')
            get_mac_address_list(get_device_ip(), i_range=[1,80], hide_empty_macs=True, hide_device_names=False)
        else:
            schedule.run_pending()
            duration = datetime.now() - ts
            ts = datetime.now()
            print(f'\n\n=================================\n\n\tTime elapsed\n\t{duration}\n\n=================================\n\n')
        if count % ONE_SESSION == 0:
            ip_parts = get_device_ip().split('.')
            print(f'\nAwaiting... {WAIT} sec before cleaning ARP table')
            await asyncio.sleep(WAIT)
            for iter in range(1, 255):
                current_ip = f'{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{iter}'
                await clear_arp(current_ip, interface_name = current_network_interface)
            print("ARP table cleaned\n")
        print(f'Awaiting... {WAIT} sec')
        await asyncio.sleep(WAIT)
            
        count += 1
        


asyncio.run(main())