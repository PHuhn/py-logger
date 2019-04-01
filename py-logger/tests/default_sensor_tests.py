""" module: tests of default sensor """
import unittest
from datetime import datetime as DateTime
import logger
#
class DefaultSensorTests(unittest.TestCase):
    """ class: tests of default sensor """
    def test_default_sensor_constructor(self):
        """ method: test get_type_name """
        settings = ['closed', 'open']
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Door', settings)
        self.assertEqual('range', sut.valid_type)
        self.assertEqual(1, sut.valid_value)
        self.assertEqual(DateTime(1900, 1, 1, 6, 0), sut.start_time)
        self.assertEqual(DateTime(1900, 1, 1, 16, 0), sut.end_time)
        self.assertEqual('Door', sut.name)
        self.assertEqual(settings, sut.settings)
    #
    def test_default_sensor_constructor_never(self):
        """ method: test get_type_name """
        sut = logger.DefaultSensor('N', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        self.assertEqual('never', sut.valid_type)
    #
    def test_default_sensor_constructor_always(self):
        """ method: test get_type_name """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        self.assertEqual('always', sut.valid_type)
    #
    # def get_hr_min_sec(hr_min_sec_str):
    #
    def test_default_sensor_get_hr_min_sec_00(self):
        """ method: test get_hr_min_sec """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_hr_min_sec('00:00:00')
        self.assertEqual(DateTime(1900, 1, 1, 0, 0, 0), tm)
    #
    def test_default_sensor_get_hr_min_sec_0(self):
        """ method: test get_hr_min_sec """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_hr_min_sec('0:0:0')
        self.assertEqual(DateTime(1900, 1, 1, 0, 0, 0), tm)
    #
    def test_default_sensor_get_hr_min_sec_hour(self):
        """ method: test get_hr_min_sec """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_hr_min_sec('18:00:00')
        self.assertEqual(DateTime(1900, 1, 1, 18, 0, 0), tm)
    #
    def test_default_sensor_get_hr_min_sec_minute(self):
        """ method: test get_hr_min_sec """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_hr_min_sec('00:18:00')
        self.assertEqual(DateTime(1900, 1, 1, 0, 18, 0), tm)
    #
    def test_default_sensor_get_hr_min_sec_second(self):
        """ method: test get_hr_min_sec """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_hr_min_sec('00:00:18')
        self.assertEqual(DateTime(1900, 1, 1, 0, 0, 18), tm)
    #
    # def get_date_str_time(self, dt_str):
    #
    def test_default_sensor_get_date_str_time(self):
        """ method: test get_type_name """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_date_str_time('2019-12-12 00:00:00')
        self.assertEqual(DateTime(1900, 1, 1, 0, 0, 0), tm)
    #
    def test_default_sensor_get_date_str_time_seconds(self):
        """ method: test get_type_name """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_date_str_time('2019-12-12 01:01:01')
        self.assertEqual(DateTime(1900, 1, 1, 1, 1, 1), tm)
    #
    def test_default_sensor_get_date_str_time_minutes(self):
        """ method: test get_type_name range """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_date_str_time('2019-12-12 01:01:00')
        self.assertEqual(DateTime(1900, 1, 1, 1, 1, 0), tm)
    #
    def test_default_sensor_get_date_str_time_hours(self):
        """ method: test get_type_name range """
        sut = logger.DefaultSensor('A', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        tm = sut.get_date_str_time('2019-12-12 01:00:00')
        self.assertEqual(DateTime(1900, 1, 1, 1, 0, 0), tm)
    #
    # def get_status(self, dt_str, i_o):
    #
    def test_default_sensor_get_status_out_range_valid(self):
        """ method: test get_status range """
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        status = sut.get_status('2019-12-12 01:00:00', 1)
        print(status, '2019-12-12 01:00:00', 1)
        self.assertEqual('OK', status)
    #
    def test_default_sensor_get_status_out_range_invalid(self):
        """ method: test get_status range """
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        status = sut.get_status('2019-12-12 01:00:00', 0)
        print(status, '2019-12-12 01:00:00', 0)
        self.assertEqual('Warning', status)
    #
    def test_default_sensor_get_status_in_range_valid(self):
        """ method: test get_status """
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        status = sut.get_status('2019-12-12 07:00:00', 1)
        print(status, '2019-12-12 07:00:00', 1)
        self.assertEqual('OK', status)
    #
    def test_default_sensor_get_status_in_range_invalid(self):
        """ method: test get_status """
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        status = sut.get_status('2019-12-12 07:00:00', 0)
        print(status, '2019-12-12 07:00:00', 0)
        self.assertEqual('OK', status)
    #
    def test_default_sensor_get_status_never_valid(self):
        """ method: test get_status range """
        sut = logger.DefaultSensor('NEVER', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        status = sut.get_status('2019-12-12 01:00:00', 1)
        self.assertEqual('OK', status)
    #
    def test_default_sensor_get_status_never_invalid(self):
        """ method: test get_status range """
        sut = logger.DefaultSensor('NEVER', 1, '06:00:00', '16:00:00', 'Door', ['closed', 'open'])
        status = sut.get_status('2019-12-12 01:00:00', 0)
        self.assertEqual('Warning', status)
    #
    # def log(self, dt_str, key_str, location_str, pin, i_o):
    #
    def test_default_sensor_log_range_valid(self):
        """ method: test get_status range """
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Unknown', ['no pwr', 'power'])
        log = sut.log('2019-12-12 07:00:00', 'k-1', 'L-1', 'P-1', 0)
        print(log)
        self.assertEqual('2019-12-12 07:00:00,k-1,Unknown,L-1,OK,OK: Unknown at location: L-1 is no pwr', log)
    #
    def test_default_sensor_log_range_invalid(self):
        """ method: test get_status range """
        sut = logger.DefaultSensor('RANGE', 1, '06:00:00', '16:00:00', 'Unknown', ['no pwr', 'power'])
        log = sut.log('2019-12-12 01:00:00', 'k-1', 'L-1', 'P-1', 0)
        print(log)
        self.assertEqual('2019-12-12 01:00:00,k-1,Unknown,L-1,Warning,Warning: Unknown at location: L-1 is no pwr', log)
    #
    def test_default_sensor_log_never_refrig(self):
        """ method: test get_status range """
        # Refrig-116,Refrig,116,21,N,0,00:00:00,23:59:59,ok|alarm
        sut = logger.DefaultSensor('Never', 0, '00:00:00', '23:59:59', 'refrig', ['ok', 'alarm'])
        log = sut.log('2019-12-12 01:00:00', 'refrig-116', 'Rm 110', 'P-1', 0)
        print(log)
        self.assertEqual('2019-12-12 01:00:00,refrig-116,refrig,Rm 110,OK,OK: refrig at location: Rm 110 is ok', log)
        log = sut.log('2019-12-12 01:01:00', 'refrig-116', 'Rm 110', 'P-1', 1)
        print(log)
        self.assertEqual('2019-12-12 01:01:00,refrig-116,refrig,Rm 110,Warning,Warning: refrig at location: Rm 110 is alarm', log)
    #
    def test_default_sensor_log_rang_door(self):
        """ method: test get_status range """
        # door-115,Door,115,4,R,0,08:00:00,17:00:00,closed|open
        sut = logger.DefaultSensor('Range', 0, '07:00:00', '16:59:59', 'door', ['closed', 'open'])
        log = sut.log('2019-12-12 01:00:00', 'door-116', 'Rm 110', 'P-1', 0)
        print(log)
        self.assertEqual('2019-12-12 01:00:00,door-116,door,Rm 110,OK,OK: door at location: Rm 110 is closed', log)
        log = sut.log('2019-12-12 01:01:00', 'door-116', 'Rm 110', 'P-1', 1)
        print(log)
        self.assertEqual('2019-12-12 01:01:00,door-116,door,Rm 110,Warning,Warning: door at location: Rm 110 is open', log)
    #
if __name__ == '__main__':
    unittest.main()
