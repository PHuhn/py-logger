""" module: library of sql server functionality """
# ============================================================================
# Copyright (c) 2019 Northern Software Group
# This software is owned by Northern Software Group.  Unauthorized copying,
# distribution or changing of this software is prohibited.
#
from datetime import datetime as DateTime
from pathlib import Path
import os
import pyodbc
import abstract_logger
#
# https://github.com/mkleehammer/pyodbc/wiki
# http://www.freetds.org/userguide/freetdsconf.htm
# https://stackoverflow.com/questions/24906016/exception-value-08001-08001-unixodbcfreetdssql-serverunable-to-con
#
class SqlLogger(abstract_logger.AbstractLogger):
    """ class: collection of sql server functiuonality (library) """
    def __init__(self, server_name, db_name, user, password, port='1433', odbc_driver='SQL Server'):
        self.logger_name = 'SqlDatabase' # required property
        self.connection_str = ''
        self.connection = None
        self.locked = False
        self.err_file_name = 'door_light_sql_err.log'
        if user == '':
            self.connection_str = \
                self.sql_connection_trusted_string(server_name, db_name, odbc_driver)
        else:
            self.connection_str = \
                self.sql_connection_user_string(server_name, db_name, user, password, port, odbc_driver)
        self.connection = self.sql_connection(self.connection_str)
    ##
    # sql functions
    #   sql_connection_trusted_string
    #   sql_connection
    #   sql_execute
    ##
    def sql_connection_trusted_string(self, server_name, db_name, odbc_driver='SQL Server'):
        """ construct a sql server connection string, creation of a trusted connection,
        which does not require a user name and password.
        """
        driver = 'Driver={' + odbc_driver + '};Trusted_Connection=yes;'
        server = 'Server=' + server_name + ';'
        database = 'Database=' + db_name + ';'
        return driver + server + database
    #
    def sql_connection_user_string(self, server_name, db_name, user, pwd, port_num='1433', odbc_driver='SQL Server'):
        """ construct a sql server connection string, creation of a of a connection,
        which does requires a user name and password.
        """
        driver = 'Driver={' + odbc_driver + '};'
        port = 'PORT=' + port_num + ';'
        server = 'Server=' + server_name + ';'
        database = 'Database=' + db_name + ';'
        user_pwd = 'UID=' + user + ';PWD=' + pwd + ';'
        print('Server:', server, ', DB:', database, ', Driver:', driver, ', Port:', port, ', User:', user)
        return driver + port + server + database + user_pwd
    #
    def sql_connection(self, connection_string):
        """ construct a sql server connection """
        self.connection = pyodbc.connect(connection_string)
        return self.connection
    #
    def sql_execute(self, sql_command):
        """ Execute sql command, create a cursor from the connection """
        count = 0
        if sql_command != '':
            # reconnect if connection was dropped...
            cursor = None
            try:
                cursor = self.connection.cursor()
            except pyodbc.Error as exc:
                sql_state = exc.args[0]
                if sql_state == '08S01':
                    self.connection.close()
                    self.connection = self.sql_connection()
                    cursor = self.connection.cursor()
            cursor.execute(sql_command)
            count = cursor.rowcount
            print(count, 'rows affected')
            self.connection.commit()
            cursor.close()
            del cursor
        else:
            print('ERROR: empty sql command string.')
        return count
    #
    def sql_insert_log_string(self, log):
        """ construct an insert command, INSERT INTO DoorLight """
        # dt_str, key_str, self.name, location_str, status, msg
        if log == '':
            log = '{0},unk-key,unk-type,unk-log,unk-status, Empty log data log.'.format(DateTime.now())
        log_fld = log.split(',')
        return self.sql_format_insert_log_string(log_fld, log)
    #
    def sql_format_insert_log_string(self, log_fld, log_msg):
        """ construct an insert command, INSERT INTO DoorLight """
        sql_command = ''
        sql_values = "VALUES( '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}' )".format(DateTime.now().strftime('%Y-%m-%d %H:%M:%S'), log_fld[0], log_fld[1], log_fld[2], log_fld[3], log_fld[4], log_fld[5], log_msg)
        sql_command = 'INSERT INTO DoorLight ( CreateDate, LogDate, [Key], [Type], [Location], [Status], Msg, [Log] ) ' + sql_values
        print(sql_values)
        return sql_command
    #
    def write_log(self, log_msg):
        """ method: write a log event for this msg """
        ret_count = 0
        if log_msg != '':
            count = self.sql_execute(self.sql_insert_log_string(log_msg))
            if count == 0:
                with open(self.err_file_name, 'a') as file_handle:
                    print(log_msg, file=file_handle)
            else:
                ret_count += 1
                ret_count += self.sql_err_file_retry()
        return ret_count
    #
    def sql_err_file_retry(self):
        """ method: write the sql write failed record to retry withing to sql """
        ret_count = 0
        input_file = Path(self.err_file_name)
        if input_file.exists() and self.locked is False:
            self.locked = True
            delete = True
            with open(self.err_file_name, 'r') as file_handle:
                for line in file_handle:
                    log_msg = line.split(',')
                    if len(log_msg) > 3:
                        if self.sql_execute(self.sql_format_insert_log_string(log_msg, line)) == 0:
                            delete = False
                        else:
                            ret_count += 1
            if delete is False:
                os.remove(self.err_file_name)
            self.locked = False
        return ret_count
#
