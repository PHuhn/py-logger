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


### Other Documents ##


Good luck, Phil
