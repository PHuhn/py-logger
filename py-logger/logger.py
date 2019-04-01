#!/usr/bin/python3
""" the door and light module """
# ============================================================================
# Copyright (c) 2019 Northern Software Group
# This software is owned by Northern Software Group.  Unauthorized copying,
# distribution or changing of this software is prohibited.
#
import json
## import gpiozero as GPIO
from datetime import datetime as DateTime, date as Date
from pathlib import Path
import sys as Sys
import signal
import sql_logger
import nrdp_logger
import abstract_logger
#
class DefaultSensor():
    """ class: the default sensor """
    #
    # Door settings ['closed', 'open']
    # Light settings ['off', 'on']
    # Refrig settings ['ok', 'alarm']
    # Unknown settings ['no pwr', 'power']
    #
    def __init__(self, valid_type, valid_value, start_hr_min_sec, end_hr_min_sec, name, settings):
        self.name = name
        if len(settings[0]) < 2:
            print(name + ' not valid settings ' + settings)
            settings = ['no pwr', 'power']
        self.settings = settings
        self.valid_type = 'never'
        self.valid_value = int(valid_value)
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
            return '{0},{1},{2},{3},Warning,Sensor bad i/o: {4}'.format(dt_str, key_str, self.name, location_str, i_o)
        status = self.get_status(dt_str, i_o)
        # 0=Date, 1=key, 2=name, 3=location, 4=status, 5=setting per i_o
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
        # print(self.valid_type, self.valid_value, i_o, self.valid_value != i_o, status)
        return status
    #
class Sensor():
    """ class: the sensor of door or light """
    def __init__(self, key, sensor_type, location, gpio, valid_type, valid_value, start_hr_min_sec, end_hr_min_sec, settings, btn, output_logger, nrdp_logger):
        self.key = key
        self.type = sensor_type
        self.location = location
        self.gpio = int(gpio)
        self.btn = btn
        self.output_logger = output_logger
        self.fld_count = 6
        self.nrdp = False
        if nrdp_logger != None:
            self.nrdp = True
        self.nrdp_logger = nrdp_logger
        #
        self.sensor = None
        self.sensor = DefaultSensor(valid_type, valid_value, start_hr_min_sec, end_hr_min_sec, sensor_type, settings)
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
        cnt = self.output_logger.write_log(log_msg)
        if self.nrdp == True:
            self.nrdp_logger.write_log(log_msg)
        return cnt
#
class FileLogger(abstract_logger.AbstractLogger):
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
        self.log_name = self.log_folder + today_str + '-py-logger.log'
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
class ConsoleLogger(abstract_logger.AbstractLogger):
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
    def __init__(self, output_logger, nrdp_logger):
        self.sql_server = object
        self.monitor_events = []
        self.output_logger = output_logger
        self.nrdp_logger = nrdp_logger
    #
    def log_process_main(self, file_path):
        """ function: application main """
        self.log_logo()
        print("The arguments are: ", file_path)
        #
        input_file = Path(file_path)
        if input_file.exists():
            # path/file exists
            print('Press <ENTER> to exit.')
            print('Sensor devices:')
            # key, sensor_type, location, gpio, valid_type, valid_value, start_hr_min_sec, end_hr_min_sec, btn, output_logger)
            sensor = Sensor('Id', 'Type', 'Location', 0, 'A', 0, '00:00:00', '23:59:59', ['no', 'yes'], None, self.output_logger, None)
            log_msg = '{0},{1},{2},{3},{4},** Starting logger **'.format(
                sensor.log_now(), 'Id', 'Type', 'Location', 'Status')
            self.output_logger.write_log(log_msg)
            #
            config_file = open(file_path, "r")
            for line in config_file:
                line = line.rstrip()
                row = line.split(',')
                if row[0] != 'id':
                    pin = int(row[3])
                    settings = row[8].split('|')
                    btn = None
                    ## btn = GPIO.Button(pin)
                    # key, sensor_type, location, gpio, valid_type, valid_value, start_hr_min_sec, end_hr_min_sec, btn, output_logger, nrdp_logger)
                    sensor = Sensor(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], settings, btn, self.output_logger, self.nrdp_logger)
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
    @staticmethod
    def log_logo():
        """ function: display character based logo """
        print("  +--------------------------+")
        print("  |  ==== ======== ========  |")
        print("  |  ==== ======== ========  |   py-logger ")
        print("  |  ==== ======== ========  |")
        print("  |  ==== ======== ========  |")
        print("  +--------------------------+")
#
if __name__ == '__main__':
    #
    CONFIG_JSON_FILE = 'config.json'
    ARGC = len(Sys.argv)
    if ARGC == 2:
        if (Sys.argv[1][0] == '-'):
            print('Usage: ' + Sys.argv[0] + ' <JSON config file>')
            exit(0)
        CONFIG_JSON_FILE = Sys.argv[1]
        print('Using ' + CONFIG_JSON_FILE + ' JSON config file')
    OUTPUT_LOGGER = None
    NRDP_LOGGER = None
    with open(CONFIG_JSON_FILE, 'r') as f:
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
        PORT = SQL['Port']
        # if user is left blank then it will try trusted connection
        USER = SQL['User']
        PASSWORD = ''
        if USER == '':
            print('Using trusted connection')
        else:
            print('Using user:' + USER)
            PASSWORD = SQL['Password']
        print('Server:', SERVER, ', DB:', DB, ', Driver:', ODBC_DRIVER, ', Port:', PORT, ', User:', USER)
        OUTPUT_LOGGER = sql_logger.SqlLogger(SERVER, DB, USER, PASSWORD, PORT, ODBC_DRIVER)
    if OUTPUT_LOGGER is None:
        print('No valid output logger assigned.')
        print(' Output logger options are: Console/File/Sql')
        exit()
    if CONFIG['Nrdp'].lower() == 'true':
        NAGIOS = CONFIG['Nagios']
        URL = NAGIOS['Url']
        TOKEN = NAGIOS['Token']
        HOST = NAGIOS['Host']
        SERVICE_POSTFIX = NAGIOS['Service']
        STATE = NAGIOS['State']
        CHECK_TYPE = NAGIOS['CheckType']
        NRDP_LOGGER = nrdp_logger.NagiosLogger(URL, TOKEN, HOST, SERVICE_POSTFIX , STATE, CHECK_TYPE)
        print(URL, TOKEN, HOST, SERVICE_POSTFIX)
    LOGGERS = Loggers(OUTPUT_LOGGER, NRDP_LOGGER)
    LOGGERS.log_process_main(file_path=SENSOR_FILE)
    exit(0)
#
