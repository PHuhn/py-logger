import unittest
import unittest.mock as Mock
# from unittest.mock import patch, mock_open
from urllib import request as UrlRequest, parse as UrlParse
import nrdp_logger
#
class NagiosLoggerTests(unittest.TestCase):
    #
    def setUp(self):
        self.err_file_name = 'door_light.log'
        self.url = 'http://192.168.0.27/nrdp'
        self.token = '==#fake-token#=='
        self.host = 'raspberrypi'
        self.service = 'door-light'
        self.state = '0'
        self.check_type = '1'
        self.sut = nrdp_logger.NagiosLogger(
            self.url, self.token, self.host, self.service, self.state, self.check_type)
    #
    def test_constructor(self):
        """ method: test the constructor """
        self.assertIsNotNone(self.sut)
        self.assertEqual(self.url, self.sut.url)
        self.assertEqual(self.token, self.sut.token)
        self.assertEqual(self.host, self.sut.host)
        self.assertEqual(self.service, self.sut.service_postfix)
        self.assertEqual(self.state, self.sut.state)
        self.assertEqual(self.check_type, self.sut.check_type)
    #
    #patch('UrlRequest.FancyURLopener')
    def test_write_log_bad(self):
        """ method: test the constructor """
        # Set-up
        message = "2018-12-18 11:11:00,key,type,somewhere,OK,OK: Sensor is on"
        mock_data = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<result>\n<status>-1</status>\n<message>BAD</message>\n</result>".encode('utf8')
        with Mock.patch("urllib.request.urlopen", new = Mock.mock_open(read_data =mock_data), create =True) as m_open:
            # Act
            ret = self.sut.write_log(message)
            # Test
            self.assertEqual(-1, ret)
        # response_mock = Mock.MagicMock()
        # response_mock.read.return_value = 'ok'
        # f = opener.open(url, params)
        # mock_urlopen.return_value.__enter__.return_value.read.return_value = 'ok'
        # m_open = Mock.mock_open()
        # m_open.read = Mock.MagicMock()
        # mock_urlopen.return_value.open.return_value.read.return_value = m_open
        # mock_urlopen.return_value = response_mock
    #
    def test_write_log_good(self):
        """ method: test the constructor """
        # Set-up
        message = "2018-12-18 11:11:00,key,type,somewhere,OK,OK: Sensor is on"
        mock_data = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<result>\n<status>0</status>\n<message>OK</message>\n</result>".encode('utf8')
        with Mock.patch("urllib.request.urlopen", new = Mock.mock_open(read_data =mock_data), create =True) as m_open:
            # Act
            ret = self.sut.write_log(message)
            # Test
            self.assertEqual(1, ret)
    #
    #def test_write(self):
    #    """ method: test the constructor """
    #    xml="<?xml version='1.0'?>\n<checkresults>\n</checkresult>";
    #    mock_data = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<result>\n<status>-1</status>\n<message>BAD</message>\n</result>".encode('utf8')
    #    query_data = UrlParse.urlencode({'token': self.token.strip(), 'cmd': 'submitcheck', 'XMLDATA': xml});
    #    url_data = "{0}?{1}".format(self.url, query_data)
    #    print(url_data)
    #    with Mock.patch("urllib.request.urlopen", new = Mock.mock_open(read_data =mock_data), create =True) as m_open:
    #        with UrlRequest.urlopen(url_data) as f:
    #            print(f.read().decode('utf-8'))
    #
if __name__ == '__main__':
    unittest.main()
