#!/usr/bin/python3
""" the door and light module """
import json
## import gpiozero as GPIO
from datetime import datetime as DateTime, date as Date
from pathlib import Path
# import os
import signal
import sql_logger
#
class DoorSensor():
    """ class: the door sensor """
    def __init__(self, valid_type, valid_value, start_time, end_time, name='Door'):
        self.name = name
        self.settings = ['closed', 'open']
        self.valid_type = 'always'
        self.vaild_value = valid_value
        valid_type = valid_type[0].lower()
        if valid_type == 'a':
            self.valid_type = 'always'
        else:
            if valid_type == 'n':
                self.valid_type = 'never'
            else:
                if valid_type == 'r':
                    self.valid_type = 'range'
        self.start_time = DateTime.strptime(start_time, '%H:%M')
        self.end_time = DateTime.strptime(end_time, '%H:%M')
    #
    def log(self, dt_str, key_str, location_str, pin, i_o):
        """ log a specific way for this sensor type, io is 0 or 1
        required comma seperated field of log date, key and message
        """
        if i_o < 0 or i_o >= len(self.settings):
            return '{0},{1},{2},{3},Warning,Sensor bad i/o: {4}'.format(dt_str, key_str, self.name, location_str, i_o)
        status = self.get_status(dt_str, i_o)
        return '{0},{1},{2},{3},{4},Door at location: {3} is {5}'.format(dt_str, key_str, self.name, location_str, status, self.settings[i_o])
    #
    def date_str_time(dt_str):
        ret = DateTime.strptime('00:00', '%H:%M')
        dt = DateTime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        ret.hours = dt.hours
        ret.minutes = dt.minutes
        return ret
    #
    def get_status(self, dt_str, i_o):
        status = 'OK'
        if self.valid_type == 'never' and self.valid_value != i_o:
            status = 'Warning'
        if self.valid_type == 'range':
            if self.start_time <= self.date_str_time(dt_str) <= self.end_time and self.valid_value == i_o:
                status = 'OK'
            else:
                status = 'Warning'
        return status
    #
class LightSensor():
    """ class: the light sensor """
    def __init__(self, valid_type, valid_value, start_time, end_time, name='Light'):
        self.name = name
        self.settings = ['off', 'on']
    def log(self, dt_str, key_str, location_str, pin, i_o):
        """ log a specific way for this sensor type, io is 0 or 1
        required comma seperated field of log date, key and message
        """
        if i_o < 0 or i_o >= len(self.settings):
            return '{0},{1},{2},{3},Sensor bad i/o: {4}'.format(dt_str, key_str, self.name, location_str, i_o)
        return '{0},{1},{2},{3},Light at location: {3} is {4}'.format(dt_str, key_str, self.name, location_str, self.settings[i_o])
    #
    def date_str_time(dt_str):
        ret = DateTime.strptime('00:00', '%H:%M')
        dt = DateTime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        ret.hours = dt.hours
        ret.minutes = dt.minutes
        return ret
    #
    def get_status(self, dt_str, i_o):
        status = 'OK'
        if self.valid_type == 'never' and self.valid_value != i_o:
            status = 'Warning'
        if self.valid_type == 'range':
            if self.start_time <= self.date_str_time(dt_str) <= self.end_time and self.valid_value == i_o:
                status = 'OK'
            else:
                status = 'Warning'
        return status
    #
class DefaultSensor():
    """ class: the default sensor """
    #
    # Door settings ['closed', 'open']
    # Light settings ['off', 'on']
    #
    def __init__(self, valid_type='always', valid_value=1, start_hr_min_sec='', end_hr_min_sec='', name='Unknown', settings=['no pwr', 'power']):
        self.name = name
        self.settings = settings
        self.valid_type = 'never'
        self.valid_value = valid_value
        valid_type = valid_type[0].lower()
        if valid_type == 'a':
            self.valid_type = 'always'
        else:
            if valid_type == 'r':
                self.valid_type = 'range'
        self.start_time = self.get_hr_min_sec(start_hr_min_sec)
        self.end_time = self.get_hr_min_sec(end_hr_min_sec)
    #
    def log(self, dt_str, key_str, location_str, pin, i_o):
        """ log a specific way for this sensor type, io is 0 or 1
        required comma seperated field of log date, key and message
        """
        if i_o < 0 or i_o >= len(self.settings):
            return '{0},{1},{2},{3},Sensor bad i/o: {4}'.format(dt_str, key_str, self.name, location_str, i_o)
        status = self.get_status(dt_str, i_o)
        # 0=Date, 1=key, 2=name, 3=location, 4:status, 5:setting per i_o
        return '{0},{1},{2},{3},{4},{4}: {2} at location: {3} is {5}'.format(
            dt_str, key_str, self.name, location_str, status, self.settings[i_o])
    #
    def get_date_str_time(self, dt_str):
        """ method take in dt_str and output generic time (hr-minute) """
        return self.get_hr_min_sec(dt_str.split(' ')[1])
    #
    @staticmethod
    def get_hr_min_sec(hr_min_sec_str):
        """ method take in time string and output generic time value """
        if hr_min_sec_str == '': hr_min_sec_str = '00:00:00'
        return DateTime.strptime(hr_min_sec_str, '%H:%M:%S')
    #
    def get_status(self, dt_str, i_o):
        """ method take in dt_str and current i_o, output status of OK or Warning """
        status = 'OK'
        if self.valid_type == 'never' and self.valid_value != i_o:
            status = 'Warning'
        if self.valid_type == 'range':
            if not self.start_time <= self.get_date_str_time(dt_str) <= self.end_time:
                if self.valid_value != i_o:
                    status = 'Warning'
        return status
    #
class Sensor():
    """ class: the sensor of door or light """
    def __init__(self, key, sensor_type, location, gpio, btn, output_logger):
        self.key = key
        self.type = sensor_type
        self.location = location
        self.gpio = int(gpio)
        self.btn = btn
        self.output_logger = output_logger
        self.fld_count = 5
        #
        self.sensor = DefaultSensor('Sensor-'+str(gpio))
        if self.type.upper() == 'L':
            self.sensor = LightSensor()
        if self.type.upper() == 'D':
            self.sensor = DoorSensor()
    #
    def valid_log_msg(self, log_msg):
        """ method: check if string is a valid log message """
        return len(log_msg.split(',')) == self.fld_count
    #
    def get_type_name(self):
        """ method: get_type_name returns logical name of sensor """
        return self.sensor.name
    #
    def get_type_settings(self):
        """ method: get_type_settings returns the name of the binary string values for sensor """
        return self.sensor.settings
    #
    def display(self):
        """ method: display returns a to_string of the class for sensor """
        return "Sensor - id: {0}, type: {1}, loc: {2}, gpio: {3}".format( \
            self.key, self.get_type_name(), self.location, self.gpio)
    #
    def log_now(self):
        """ method: display returns a string values of datetime now for logging """
        now = DateTime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    #
    def log0(self):
        """ method: log returns a string log record """
        return self.log(0)
    def log1(self):
        """ method: log returns a string log record """
        return self.log(1)
    def log(self, i_o):
        """ method: log returns a string log record """
        log_msg = self.sensor.log(self.log_now(), self.key, self.location, self.gpio, i_o)
        return self.output_logger.write_log(log_msg)
#
class FileLogger(object):
    """ class: logs output filessystem log file based upon date """
    def __init__(self, log_folder):
        self.logger_name = 'File' # required property
        self.log_folder = log_folder
        self.today = None
        self.log_name = ''
        #
        if log_folder != '':
            if log_folder[-1] != '/':
                self.log_folder = log_folder + '/'
        self.set_log_name(self.get_today())
    #
    def get_today(self):
        """ method: get date string of today """
        return Date.today()
    #
    def set_log_name(self, today):
        """ method: set date to today, and today's log file name """
        self.today = today
        today_str = today.strftime("%Y-%m-%d")
        self.log_name = self.log_folder + today_str + '-dl.log'
    # required method of write_log
    def write_log(self, log_msg):
        """ method: write a log event for this sensor (not sensor type) """
        today = self.get_today()
        # inforce daily log file
        if today != self.today:
            self.set_log_name(today)
        with open(self.log_name, 'a') as file_handle:
            print(log_msg, file=file_handle)
        return 1
#
class ConsoleLogger(object):
    """ class: logs output filessystem log file based upon date """
    def __init__(self):
        self.logger_name = 'Console' # required property
    # required method of write_log that returns a count
    def write_log(self, log_msg):
        """ method: write a log event for this message """
        print(log_msg)
        return 1
#
class Loggers(object):
    """ class: NetGear logs load of network incidents """
    def __init__(self, output_logger):
        self.sql_server = object
        self.monitor_events = []
        self.output_logger = output_logger
    #
    def log_process_main(self, file_path):
        """ function: application main """
        print("The arguments are: ", file_path)
        #
        input_file = Path(file_path)
        if input_file.exists():
            # path/file exists
            print('Press <ENTER> to exit.')
            print('Sensor devices:')
            config_file = open(file_path, "r")
            for line in config_file:
                line = line.rstrip()
                row = line.split(',')
                if row[0] != 'id':
                    pin = int(row[3])
                    btn = None
                    ## btn = GPIO.Button(pin)
                    sensor = Sensor(row[0], row[1], row[2], row[3], btn, self.output_logger)
                    ## btn.when_pressed = sensor.log1
                    ## btn.when_released = sensor.log0
                    self.monitor_events.append(sensor)
                    is_active = 0
                    ## if btn.is_active == True: is_active = 1
                    sensor.log(is_active)
            config_file.close()
            input()
        else:
            print(file_path, ' not found')
#
if __name__ == '__main__':
    #
    OUTPUT_LOGGER = None
    with open('config.json', 'r') as f:
        CONFIG = json.load(f)
    SENSOR_FILE = CONFIG['SensorConfigFile']
    OUTPUT_LOGGER_TYPE = CONFIG['OutputLogger'].lower()
    print(SENSOR_FILE, OUTPUT_LOGGER_TYPE)
    if OUTPUT_LOGGER_TYPE == 'console':
        OUTPUT_LOGGER = ConsoleLogger()
    if OUTPUT_LOGGER_TYPE == 'file':
        FILE = CONFIG['File']
        FOLDER = FILE['Folder']
        OUTPUT_LOGGER = FileLogger(FOLDER)
    if OUTPUT_LOGGER_TYPE == 'sql':
        SQL = CONFIG['Sql']
        SERVER = SQL['ServerName']
        DB = SQL['DbName']
        ODBC_DRIVER = SQL['OdbcDriver']
        # if user is left blank then it will try trusted connection
        USER = SQL['User']
        PASSWORD = ''
        if USER == '':
            print('Using trusted connection')
        else:
            print('Using user:' + USER)
            PASSWORD = SQL['Password']
        print('Server:', SERVER, 'DB:', DB, 'User:', USER)
        OUTPUT_LOGGER = sql_logger.SqlLogger(SERVER, DB, USER, PASSWORD, ODBC_DRIVER)
    if OUTPUT_LOGGER is None:
        print('No valid output logger assigned.')
        print(' Output logger options are: Console/File/Sql')
        exit()
    LOGGERS = Loggers(OUTPUT_LOGGER)
    LOGGERS.log_process_main(file_path=SENSOR_FILE)
    exit(0)
#
