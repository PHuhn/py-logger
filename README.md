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

### Logging Points (config.dat)

- Id
- Type
- Room
- Gp I/O
- Value type
- Valid value
- Start Time
- End Time
- Settings
- Notification

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
  <configure the config.dat and test the configuration>
  <configure the config.json, I suggest leaving it in console output>
cd etc
sudo chmod 755 *.sh
sudo ./py-logger-install.sh
  <configure the config.json in /usr/local/py-logger directory>
```

### Other Documents ##


Good luck, Phil
