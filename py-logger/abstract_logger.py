""" module: abstract class template for a logger """
# ============================================================================
# Copyright (c) 2019 Northern Software Group
# This software is owned by Northern Software Group.  Unauthorized copying,
# distribution or changing of this software is prohibited.
#
from abc import ABCMeta, abstractmethod
#
class AbstractLogger(object):
    """ class: abstract class logger
    abc @ attributes as follows:
     * @abstractmethod
     * @abstractclassmethod
     * @abstractstaticmethod
     * @abstractproperty
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def write_log(self, log_msg):
        """ method: abstract method logger """
        print('not implemented')
        return 0
#
