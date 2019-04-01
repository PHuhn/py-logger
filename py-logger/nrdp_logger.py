""" module: library to log string to Nagios's NRDP adapter """
# ============================================================================
# Copyright (c) 2019 Northern Software Group
# This software is owned by Northern Software Group.  Unauthorized copying,
# distribution or changing of this software is prohibited.
#
import argparse, sys
import send_nrdp
from pathlib import Path
import os
import abstract_logger
#
class NagiosLogger(object):
    """ class: to passively log a string to Nagios """
    def __init__(self, url, token, host, service, state, check_type):
        self.logger_name = 'NagiosLogger' # required property
        self.nrdp =  send_nrdp.send_nrdp()
        self.retry_locked = False
        self.err_file_name = 'door_light_nrdp_err.log'
        self.url = url
        self.token = token
        self.host = host
        self.service_postfix = service
        self.state = state
        self.check_type = check_type
    #
    def write_log(self, log_msg):
        """ method: write a log event for this msg """
        ret = 0
        if log_msg != '':
            ret = self.nagios_send(log_msg)
        return ret
    #
    def nagios_send(self, log_msg):
        count = 0
        if log_msg != '':
            # 2019-01-16 15:36:15,door-115,Door,115,OK,OK: Door at location: 115 is closed
            # usage:
            #  send_nrdp.py [-h] [-u URL] [-t TOKEN] [-H HOSTNAME] [-s SERVICE] [-S STATE] [-o OUTPUT] [-f FILE] [-d DELIM] [-c CHECKTYPE]
            #
            # = check_type
            log_fld = log_msg.split(',')
            service = log_fld[1] + '-' + self.service_postfix
            state = '0'
            if log_fld[4].lower() != 'ok':
                state = '1'
            sys.argv = ['nrdp_logger.py', '-u', self.url, '-t', self.token, '-H', self.host, '-s', service, '-S', state, '-o', log_msg, '-c', self.check_type]
            parser = argparse.ArgumentParser(description='send_nrdp.py usage.', prog='nrdp_main.py')
            parser.add_argument('-u', action="store", dest="url", help="REQUIRED: URL")
            parser.add_argument('-t', action="store", dest="token", help="REQUIRED: token")
            parser.add_argument('-H', action="store", dest="hostname", help="passive host/service")
            parser.add_argument('-S', action="store", dest="state", help="current service state")
            parser.add_argument('-o', action="store", dest="output", help="Text output of passive check result")
            parser.add_argument('-c', action="store", dest="checktype", help="1 for passive")
            parser.add_argument('-s', action="store", dest="service", help="The name of the service associated with the passive check result.")
            # no value passed to -d -f
            parser.add_argument('-d', action="store", dest="delim", help="Processing piped data delimiter")
            parser.add_argument('-f', action="store", dest="file", help="This file will be sent to the NRDP server")
            #
            args = parser.parse_args()
            #
            # setup will return count of messages
            count = self.nrdp.setup(args)
        return count
    #
    def nagios_err_file_retry(self):
        """ method: write the sql write failed record to retry withing to sql """
        ret_count = 0
        input_file = Path(self.err_file_name)
        if input_file.exists() and self.retry_locked is False:
            self.retry_locked = True
            delete = True
            with open(self.err_file_name, 'r') as file_handle:
                for line in file_handle:
                    log_msg = line.split(',')
                    if len(log_msg) > 3:
                        count = self.nagios_send(log_msg)
                        if count == 0:
                            delete = False
                        else:
                            ret_count += 1
            if delete is False:
                os.remove(self.err_file_name)
            self.retry_locked = False
        return ret_count
#
