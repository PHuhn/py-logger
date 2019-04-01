""" module: tests of sensor """
import unittest
import logger
#
class SensorTests(unittest.TestCase):
    """ class: tests of sensor """
    def test_d_name(self):
        """ method: test get_type_name """
        # 'R', 0, '06:00:00' ,'17:00:00', 
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        self.assertEqual('Door', sut.get_type_name())
    #
    def test_d_settings(self):
        """ method: test get_type_settings """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        self.assertEqual(['closed', 'open'], sut.get_type_settings())
    #
    # door-115,D,115,4,R,0,08:00:00,17:00:00
    def test_d_range_warning(self):
        """ method: test get_type_settings """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '08:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 07:49:22', sut.key, sut.location, sut.gpio, 1).split(',')
        print(log[5])
        self.assertEqual('Warning', log[4])
        log = sut.sensor.log('2018-12-12 07:49:22', sut.key, sut.location, sut.gpio, 0).split(',')
        print(log[5])
        self.assertEqual('OK', log[4])
    #
    def test_d_log_0(self):
        """ method: test of log """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 06:59:22', sut.key, sut.location, sut.gpio, 0).split(',')
        self.assertEqual('id-1', log[1])
        self.assertEqual('Door', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('OK', log[4])
        self.assertEqual('OK: Door at location: somewhere is closed', log[5])
    #
    def test_d_log_1(self):
        """ method: test of log """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 05:59:22', sut.key, sut.location, sut.gpio, 1).split(',')
        self.assertEqual('id-1', log[1])
        self.assertEqual('Door', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('Warning', log[4])
        self.assertEqual('Warning: Door at location: somewhere is open', log[5])
    #
    def test_d_log_2(self):
        """ method: test of log error """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 05:59:22', sut.key, sut.location, sut.gpio, 2).split(',')
        self.assertEqual('id-1', log[1])
        self.assertEqual('Door', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('Warning', log[4])
        self.assertEqual('Sensor bad i/o: 2', log[5])
    #
    def test_sensor_d_display(self):
        """ method: test of display """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        display = sut.display()
        self.assertEqual('Sensor - id: id-1, type: Door, loc: somewhere, gpio: 19', display)
    #
    def test_sensor_d_misc(self):
        """ method: test misc property values """
        sut = logger.Sensor('id-1', 'Door', 'somewhere', 19, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, logger.ConsoleLogger(), None)
        self.assertEqual('id-1', sut.key)
        self.assertEqual('Door', sut.type)
        self.assertEqual('somewhere', sut.location)
        self.assertEqual(19, sut.gpio)
    #
    def test_l_name(self):
        """ method: test get_type_name """
        sut = logger.Sensor('id-1', 'Light', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['off', 'on'], None, logger.ConsoleLogger(), None)
        self.assertEqual('Light', sut.get_type_name())
    #
    def test_l_settings(self):
        """ method: test get_type_settings """
        sut = logger.Sensor('id-1', 'Light', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['off', 'on'], None, logger.ConsoleLogger(), None)
        self.assertEqual(['off', 'on'], sut.get_type_settings())
    #
    # light-115,L,115,18,R,0,08:00:00,17:00:00
    def test_l_range_warning(self):
        """ method: test get_type_settings """
        sut = logger.Sensor('id-1', 'Light', 'somewhere', 19, 'R', 0, '08:00:00' ,'17:00:00', ['off', 'on'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 07:49:22', sut.key, sut.location, sut.gpio, 1).split(',')
        print(log[1], log[2], log[3], log[4], log[5])
        self.assertEqual('Warning', log[4])
        log = sut.sensor.log('2018-12-12 07:49:22', sut.key, sut.location, sut.gpio, 0).split(',')
        print(log[1], log[2], log[3], log[4], log[5])
        self.assertEqual('OK', log[4])
    #
    def test_l_log_0(self):
        """ method: test of log """
        sut = logger.Sensor('id-2', 'Light', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['off', 'on'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 05:59:22', sut.key, sut.location, sut.gpio, 0).split(',')
        self.assertEqual('id-2', log[1])
        self.assertEqual('Light', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('Warning', log[4])
        self.assertEqual('Warning: Light at location: somewhere is off', log[5])
    #
    def test_l_log_2(self):
        """ method: test of log error """
        sut = logger.Sensor('id-2', 'Light', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['off', 'on'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 05:59:22', sut.key, sut.location, sut.gpio, 2).split(',')
        self.assertEqual('id-2', log[1])
        self.assertEqual('Light', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('Sensor bad i/o: 2', log[5])
    #
    def test_r_name(self):
        """ method: test get_type_name """
        # Refrig-116,Refrig,116,21,N,0,00:00:00,23:59:59,ok|alarm
        sut = logger.Sensor('id-1', 'Refrig', 'somewhere', 19, 'N', 1, '06:00:00' ,'23:59:59', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        self.assertEqual('Refrig', sut.get_type_name())
    #
    def test_r_settings(self):
        """ method: test get_type_settings """
        sut = logger.Sensor('id-1', 'R', 'somewhere', 19, 'N', 1, '00:00:00' ,'23:59:59', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        self.assertEqual(['ok', 'alarm'], sut.get_type_settings())
    #
    def test_r_u_settings(self):
        """ method: test get_type_settings """
        sut = logger.Sensor('id-1', 'R', 'somewhere', 19, 'N', 1, '06:00:00' ,'23:59:59', 'ok,alarm', None, logger.ConsoleLogger(), None)
        self.assertEqual(['no pwr', 'power'], sut.get_type_settings())
    #
    def test_r_log_0(self):
        """ method: test of log """
        sut = logger.Sensor('id-3', 'Refrig', 'somewhere', 19, 'N', 0, '06:00:00' ,'23:59:59', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 05:59:22', sut.key, sut.location, sut.gpio, 0).split(',')
        self.assertEqual('id-3', log[1])
        self.assertEqual('Refrig', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('OK', log[4])
        self.assertEqual('OK: Refrig at location: somewhere is ok', log[5])
    #
    def test_r_log_1(self):
        """ method: test of log """
        sut = logger.Sensor('id-3', 'Refrig', 'somewhere', 19, 'N', 0, '06:00:00' ,'23:59:59', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 05:59:22', sut.key, sut.location, sut.gpio, 1).split(',')
        self.assertEqual('id-3', log[1])
        self.assertEqual('Refrig', log[2])
        self.assertEqual('somewhere', log[3])
        self.assertEqual('Warning', log[4])
        self.assertEqual('Warning: Refrig at location: somewhere is alarm', log[5])
    # refrig-116,Refrig,116,22,N,0,00:00:00,23:59:59,ok|alarm
    def test_r_log_2(self):
        """ method: test of log error """
        sut = logger.Sensor('id-3', 'X', 'somewhere', 19, 'N', 0, '06:00:00' ,'17:00:00', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 09:59:22', sut.key, sut.location, sut.gpio, 2).split(',')
        self.assertEqual('Warning', log[4])
        self.assertEqual('Sensor bad i/o: 2', log[5])
    #
    # def valid_log_msg(self, log_msg):
    #
    def test_r_valid_log_msg_0(self):
        """ method: test of log error """
        sut = logger.Sensor('id-3', 'X', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 09:59:22', sut.key, sut.location, sut.gpio, 0)
        self.assertEqual(True, sut.valid_log_msg(log))
    #
    def test_r_valid_log_msg_2(self):
        """ method: test of log error """
        sut = logger.Sensor('id-3', 'X', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        log = sut.sensor.log('2018-12-12 09:59:22', sut.key, sut.location, sut.gpio, 2)
        self.assertEqual(True, sut.valid_log_msg(log))
    #
    def test_r_valid_log_msg_bad(self):
        """ method: test of log error """
        sut = logger.Sensor('id-3', 'X', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        self.assertEqual(False, sut.valid_log_msg('2018-12-12,K,N,L,S'))
    #
    def test_r_sensor_log_0(self):
        """ method: test of log error """
        sut = logger.Sensor('id-3', 'X', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        cnt = sut.log(0)
        self.assertEqual(1, cnt)
    #
    def test_r_sensor_log_2(self):
        """ method: test of log error """
        sut = logger.Sensor('id-3', 'X', 'somewhere', 19, 'R', 1, '06:00:00' ,'17:00:00', ['ok', 'alarm'], None, logger.ConsoleLogger(), None)
        cnt = sut.log(2)
        self.assertEqual(1, cnt)
    #
if __name__ == '__main__':
    unittest.main()
