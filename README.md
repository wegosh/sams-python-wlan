# SAMS py-wlan discovery 
## _Smart Attendance Monitoring System - Python WLAN discovery_

![Website status](https://img.shields.io/website-up-down-green-red/http/wegorz.uk)

PY-wlan discovery is an extension that allows discovering devices MAC addresses in local network through wlan. After discovering different devices the script compares devices adresses with the ones available through api. If there is a match in both room assigned MAC address and Student device mac address then the attendance data is sent to server through API.


### _The API can be accessed from_:
- [API - ```requires additional input. Otherwise 404```][api/*] 

### _API choices are (replace * with one from below)_:
- room/<optional int>
- attendance/<optional int>
- building/<optional int>
- course/<optional int>
- module/<optional int>
- users/<optional int>



## Features

- Get current device ip and mac (Raspberry pi)
- List all devices connected to the WLAN and LAN
- Check avaiable interfaces 
- GET user and room data from api
- POST attendance data to api
- Read and write data to file to process attendance data


## Requires additional work in future


> As every piece of software, SAMS py-wlan discovery requires additional work 
> in order to improve the way it works and its performance.
> Until now there are few issues recognised with this software.

### _To improve:_
- Send packets to all devices to make them always discoverable
- Improve the performance
- Improve the code quality


# Tech

SAMS py-wlan discovery uses Python with multiple packages to make calls to api and process the data.

### Programming languages

- [Python v3.8.5][python] - Script has been build using python v3.8.5. Other versions of python were not tested.

### Server

- [RaspianOS][raspios] - Linux distribution for Raspberry PI
- [RaspberryPI 4B][raspi] - Device used as a server
- [Sagecom cs50001][router] - Router used for testing the script **

### Frameworks

- [Getmac v0.8.2][getmac] - A python package that allows discovering device MAC address
- [Socket][socket] - Python built-in package that allows the program to get device ip and clear ARP table that contains MAC addresses
- [Manuf v1.1.1][manuf] - Package that takes device name and manufacturer from MAC address *
- [Netifaces v0.10.4][netifaces] - Used to get interfaces available in the device
- [Requests v2.23.0][requests] - Request package is used to make GET and POST calls to API
- [RSSI v1.0.2][rssi] - RSSI package used to get info about access point. It can be used to acquire approximate location of device if there are at least three APs**
- [Schedule v1.1.0][schedule] - Schedule package is used to schedule task and run them in fixed time intervals


```*```  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp ```- currently not used```\
```**``` &nbsp;&nbsp;&nbsp;&nbsp; ```- Access Point(s)```

# Installation

Smart Attendance Monitoring System runs on 
- [ ] \(Not supported) &nbsp; ~~Windows~~ 
- [-] \(Not Tested) &nbsp; MacOS
- [x] Linux &nbsp; ```Recommended```

Install the required files

```sh
cd sams-python-wlan
python3 -m pip install -r requirements.txt
```
_Check if any errors occurred. If there are any errors report them to the [Owner][my_email]. In message provide traceback from python or screenshot with the issue._

If there are no errors try to run the application. ```Stay in the same directory as before``` - ```sams-python-wlan```

```To run the program you need to have admin permissions in order for the program to run correctly.```

To run program &nbsp; ```Network wide```
```sh
sudo python3 network_scanner.py
```

### Accessing the website 
To check if the program is running correctly wait 2 - 3 minutes and go to [API][api/att] to confirm that the attendance is there. 
```Remember that your device MAC address has to be assigned to your username and the WLAN device you are using has to be assigned to a room```

```python
async def main():
    ...
    
    ts = datetime.now()
    schedule.every(5).seconds.do(task) - #Change 5 to any other number to schedule main task differently (getting devices and adding them to file)
    schedule.every(120).seconds.do(send_data_to_api) #Change seconds -> minutes to send data to api every 120mins. Additionally change 120 -> 60 mins

    ...
```

If you need any other information how to modify the program then &nbsp; ![](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg) &nbsp; [My mail][my_email]

# Related repositories

![Github badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) ![iOS badge](https://img.shields.io/badge/iOS-000000?style=for-the-badge&logo=ios&logoColor=white)
[SAMS iOS app for beacons][sams-ios] 
[iOS pods required for the app][sams-ios-pods]

![Github badge](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white) ![Django badge](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white) ![MongoDB badge](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white) ![Ubuntu badge](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)
[Smart Attendance Monitoring System][sams] 


![](https://img.shields.io/badge/Microsoft_Outlook-0078D4?style=for-the-badge&logo=microsoft-outlook&logoColor=white) ![](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)
[My university email][my_email]


[api/*]: <https://wegorz.uk/api/*>
[api/att]: <https://wegorz.uk/api/attendance>
[python]: <https://www.python.org/>

[ubuntu]: <https://ubuntu.com/>
[digitalocean]: <https://www.digitalocean.com/>
[mongo]: <https://www.mongodb.com/cloud/atlas>
[getmac]: <https://pypi.org/project/getmac/>
[socket]: <https://pypi.org/project/socket.py/>
[manuf]: <https://pypi.org/project/manuf/>
[netifaces]: <https://pypi.org/project/netifaces/0.10.4/>
[requests]: <https://pypi.org/project/requests/2.23.0/>
[rssi]: <https://pypi.org/project/rssi/>
[schedule]: <https://pypi.org/project/schedule/>
[raspios]: <https://www.raspberrypi.org/software/operating-systems/>
[my_email]: <mailto:P17237274@my365.dmu.ac.uk>

[sams-ios]: <https://github.com/wegosh/sams-ios-main>
[sams-ios-pods]: <https://github.com/wegosh/sams-ios-pods>
[sams]: <https://github.com/wegosh/>
