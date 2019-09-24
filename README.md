# py-logger

## Overview

This solution contains the following:
- py-logger (python logger).

py-logger contains the following python files:
- logger.py
- abstract_logger.py
- sql_logger.py
- nrdp_logger.py
- send_nrdp.py

## Configuration Files

- config.dat,
- config.json.

## Required libraries

- pyodbc,
- gpiozero.

## Configurable Log Outputs

- Console,
- File (daily),
- Database.

and the above can add logging to:

- Nagios.

### Logging Attributes (config.dat)

- Id (needs to be unique across all sources)
- Type (type of sensor)
- Room (location)
- GP I/O (Raspberry-PI General Purpose I/O port #)
- Value type (R=range/A=always/N=never)
- Valid value (either 0 or 1)
- Start Time (range valid start time)
- End Time (range valid end time)
- Settings (2 string values seperated by |, example "ok|alarm", the first value is if 0 and second value if 1)
- Notification (nagios if responsible person should be notified)

Example:
```
id,type,room,gpio,valtyp,vadval,start,end,settings,notification
door-115,Door,115,4,R,0,08:00:00,17:00:00,closed|open,0
light-115,Light,115,18,R,0,08:00:00,17:00:00,off|on,0
door-116,Door,116,17,A,0,00:00:00,23:59:59,closed|open,0
refrig-116,Refrig,116,22,N,0,00:00:00,23:59:59,ok|alarm,1
```

### Logging Configuration (config.json)

```
{
  "SensorConfigFile": "config.dat",
  "OutputLogger": "Console",
  "Nrdp": "true",
  "Console": {},
  "File": {
    "Folder": ""
  },
  "Sql": {
    "OdbcDriver": "SQL Server",
    "ServerName": "192.168.0.21\\SQLExpress",
    "Port": "55109",
    "DbName": "Logging",
    "User": "RaspPI",
    "Password": "Colony-0RaspPI-0"
  },
  "Nagios": {
    "Url": "http://localhost/nrdp/",
    "Token": "u%test-token",
    "Host": "raspberrypi",
    "Service": "sensor-logger",
    "State": "0",
    "CheckType": "1"
  }
}
```

### Installation Instructions ##

```
sudo mkdir /usr/local/src
cd /usr/local/src
sudo wget https://codeload.github.com/PHuhn/py-logger/zip/master -Opy-logger.zip
sudo unzip py-logger.zip
sudo rm py-logger.zip
cd ./py-logger-master/py-logger/.
  <configure the config.dat and test the configuration with the following:
   sudo python3 py-logger.py
  >
  <configure the config.json, I suggest leaving it in console output, so you can return here and change and retest the configuration>
cd etc
sudo chmod 755 *.sh
sudo ./py-logger-install.sh
  <configure the config.json in /usr/local/py-logger directory>
```

### Other Documents ##

Also see:

[Configuring config.dat](https://github.com/PHuhn/py-logger/wiki/Configuring-config.dat) 

Good luck, Phil
