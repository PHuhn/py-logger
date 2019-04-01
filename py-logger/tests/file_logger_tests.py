""" module: tests of file logger injected class """
import unittest
from unittest.mock import patch, mock_open
from datetime import date as Date, timedelta as TimeDelta
import logger
#
# https://medium.com/@yeraydiazdiaz/what-the-mock-cheatsheet-mocking-in-python-6a71db997832
#
class FileLoggerTests(unittest.TestCase):
    """ class: tests of file logger injected class """
    def test_constructor(self):
        """ test method: tests of file logger constructor """
        sut = logger.FileLogger('')
        self.assertIsNotNone(sut)
        self.assertIsNotNone(sut.today)
        self.assertIsNotNone(sut.log_name)
        self.assertGreater(len(sut.log_name), 14)
    #
    def test_constructor_with_folder(self):
        """ test method: tests of file logger constructor """
        sut = logger.FileLogger('/var/log/doorlight')
        self.assertEquals('/var/log/doorlight/', sut.log_folder)
    #
    def test_get_today(self):
        """ test method: tests of file logger write """
        sut = logger.FileLogger('')
        self.assertEqual(Date.today(), sut.get_today())
    #
    def test_write_log(self):
        """ test method: tests of file logger write """
        m_open = mock_open()
        # patch target = 'package.module.ClassName'
        with patch('builtins.open', m_open):
            sut = logger.FileLogger('')
            sensor = logger.Sensor('key1', 'Door', 'somewhere', 12, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, sut, None)
            sut.write_log(sensor.log(1))
            m_open.assert_called_with(sut.log_name, 'a')
            handle = m_open()
            self.assertEqual(handle.write.call_count, 4)
    #
    def test_write_log_new_day_set_log_name(self):
        """ test method: tests of file logger constructor """
        m_open = mock_open()
        # patch target = 'package.module.ClassName'
        with patch('builtins.open', m_open):
            sut = logger.FileLogger('')
            current_log_name = sut.log_name
            d = Date.today() - TimeDelta(days = 1)
            sut.set_log_name(Date.today() - TimeDelta(days = 1))
            self.assertNotEquals(current_log_name, sut.log_name)
            sensor = logger.Sensor('key1', 'Door', 'somewhere', 12, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, sut, None)
            sut.write_log(sensor.log(1))
            m_open.assert_called_with(current_log_name, 'a')
    #
if __name__ == '__main__':
    unittest.main()
