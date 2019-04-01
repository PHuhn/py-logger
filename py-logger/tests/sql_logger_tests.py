"""  """
import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import os
import sql_logger
import pyodbc
import logger
#
class SqlLoggerTests(unittest.TestCase):
    """ class: tests for sql server library """
    #
    def setUp(self):
        self.server = '.\\Express'
        self.database = 'Logging'
        self.sql_logger = sql_logger.SqlLogger(self.server, self.database, '', '')
    ##
    # sql functions
    #   sql_connection_trusted_string
    #   sql_connection
    #   sql_execute
    #   log_process_load_iis_incident_types
    #   sql_insert_network_log
    ##
    def test_sql_connection_trusted_string(self):
        """ test of: sql_connection_trusted_string, creation of a trusted connection.
        which does not require a user name and password.
        """
        conn_str = self.sql_logger.sql_connection_trusted_string(self.server, self.database)
        server = 'Server=' + self.server + ';'
        database = 'Database=' + self.database + ';'
        found = False
        try:
            conn_str.index(server)
            found = True
        except ValueError:
            found = False
        self.assertEqual(True, found)
        found = False
        try:
            conn_str.index(database)
            found = True
        except ValueError:
            found = False
        self.assertEqual(True, found)
    #
    def test_sql_connection_good(self):
        """ test of: sql_connection, of one that should succeed.  If it fails it will
        throw an exception.
        """
        conn_str = self.sql_logger.sql_connection_trusted_string(self.server, self.database)
        self.sql_logger.sql_connection(conn_str)
    #
    def test_sql_connection_mock(self):
        """ test of: sql_connection, using a patch mock """
        from unittest.mock import patch
        with patch("pyodbc.connect") as mock_connect:
            self.sql_logger.sql_connection('mock connection')
            print(self.sql_logger.connection)
            mock_connect.assert_called_with('mock connection')
    #
    def test_sql_connection_bad2(self):
        """ test of: sql_connection, DatabaseError are as follows:
        DataError
        OperationalError
        IntegrityError
        InternalError
        ProgrammingError
        NotSupportedError
        """
        conn_str = self.sql_logger.sql_connection_trusted_string(self.server, 'xxxx')
        try:
            self.sql_logger.sql_connection(conn_str)
            self.assertEqual('-exception not raised', '')
        except pyodbc.ProgrammingError as exc:
            print(exc)
    #
    def test_sql_execute_bad_mock(self):
        """ test of: sql_execute, using a mock """
        from unittest.mock import patch
        with patch("pyodbc.connect") as mock_connect:
            # Set-up
            # Act
            self.sql_logger.sql_connection('mock connection string')
            count = self.sql_logger.sql_execute('')
            print(count)
            # Assert
            self.assertEqual(count, 0)
    # https://stackoverflow.com/questions/35143055/how-to-mock-psycopg2-cursor-object
    def test_sql_execute_mock(self):
        """ test of: sql_execute, using a mock """
        from unittest.mock import patch
        with patch("pyodbc.connect") as mock_connect:
            # Set-up
            mock_connect.return_value.cursor.return_value.rowcount.return_value = 1
            # Act
            self.sql_logger.sql_connection('mock connection string')
            count = self.sql_logger.sql_execute('mock command')
            print(self.sql_logger.connection)
            print(count.return_value)
            # Assert
            mock_connect.assert_called_with('mock connection string')
            self.assertEqual(count.return_value, 1)
            mock_connect.return_value.cursor.return_value.execute.assert_called()
    #
    def test_write_log(self):
        """ test method: tests of sql logger write """
        input_file = Path(self.sql_logger.err_file_name)
        if input_file.exists():
            os.remove(self.sql_logger.err_file_name)
        from unittest.mock import patch
        with patch("pyodbc.connect") as mock_connect:
            # Set-up
            mock_connect.return_value.cursor.return_value.rowcount.return_value = 1
            # Act
            self.sql_logger.sql_connection('mock connection string')
            sensor = logger.Sensor('key1', 'Door', 'somewhere', 12, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, self.sql_logger, None)
            count = sensor.log(1)
            self.assertEqual(1, count)
    #
    @patch('sql_logger.os')
    @patch('sql_logger.Path')
    def test_sql_err_file_retry_mock(self, mock_os, mock_path): # ):
        """ test method: tests of sql logger write """
        from unittest.mock import patch
        with patch("pyodbc.connect") as mock_connect:
            # Set-up
            mock_connect.return_value.cursor.return_value.rowcount.return_value = 1
            # m_open = mock_open()
            mock_path.return_value = True
            # 2019-01-17 14:10:24,id-3,Sensor-19,somewhere,OK,OK: Sensor-19 at location: somewhere is no pwr
            # LogDate, [Key], [Type], [Location], Status, Msg
            file_content_mock = '\n'.join(['2018-01-01,Key1,Door,room,OK,OK: message data', '2018-01-01,Key2,Light,room,OK,OK: message data'])
            # Act
            with patch("builtins.open", new = mock_open(read_data =file_content_mock), create =True) as m_open:
                m_open.return_value.__iter__.return_value = file_content_mock.splitlines()
                self.sql_logger.sql_connection('mock connection string')
                sensor = logger.Sensor('key1', 'Door', 'somewhere', 12, 'R', 0, '06:00:00' ,'17:00:00', ['closed', 'open'], None, self.sql_logger, None)
                count = self.sql_logger.sql_err_file_retry()
                m_open.assert_called_once_with('door_light_sql_err.log', 'r')
                self.assertEqual(2, count)
                # 'door_light.log'
    #
    def test_patch_read_data(self):
        """ test method: tests of sql logger write """
        file_content_mock = '\n'.join(['2018-01-01,Key1,message data', '2018-01-01,Key2,message data'])
        test_file = 'door_light.log'
        # Act
        with patch("builtins.open", new = mock_open(read_data=file_content_mock), create=True) as m_open:
            m_open.return_value.__iter__.return_value = file_content_mock.splitlines()
            with open(test_file, 'r') as file_handle:
                for line in file_handle:
                    print(line)
        m_open.assert_called_once_with(test_file, 'r')
    #
    # this takes too long to fail
    #def test_sql_connection_bad1(self):
    #    """ test of: sql_connection,
    #    """
    #    try:
    #        self.sql_logger.sql_connection('.\\xxxx', self.database)
    #        self.assertEqual('-exception not raised', '')
    #    except:
    #        idx = -1
    #
if __name__ == '__main__':
    unittest.main()
