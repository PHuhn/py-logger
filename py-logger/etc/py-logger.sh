#!/bin/bash
#
# ============================================================================
# Copyright (c) 2019 Northern Software Group
# This software is owned by Northern Software Group.  Unauthorized copying,
# distribution or changing of this software is prohibited.
#
# initctl - init daemon control script for py-logger
#  Written by: Phil Huhn
#  Version 1
#
function pid_logger()
{
    if [ ! -f ${RUN_FILE} ]; then
        echo "py-logger is not running."
        return 1
    fi
    LOGGER_PID=`head -n 1 ${RUN_FILE}`
    return 0
}
# program values:
PROGNAME=$(basename "$0")
REVISION="1.0.0"
# Varialbes:
RUN_FILE=/run/py-logger.lock
LOCAL_DIR=/usr/local
# See how we were called.
case "$1" in
    start)
        echo -n "Starting py-logger: "
        pid_logger
        if [ $? == 0 ]; then
            echo "py-logger already started."
            exit 0
        fi
        touch ${RUN_FILE}
        python3.7 ${LOCAL_DIR}/py-logger/logger.py > /dev/null &
        echo $! >> ${RUN_FILE}
        echo "Started."
        ;;
    stop)
        echo -n "Stopping py-logger: "
        pid_logger
        if [ $? == 1 ]; then
            exit 0
        fi
        kill ${LOGGER_PID}
        rm ${RUN_FILE}
        echo "Stopped."
        ;;
    restart|reload|force-reload)
        $0 stop
        $0 start
        ;;
    status)
        pid_logger
        if [ $? == 0 ]; then
            echo "py-logger is running at pid: ${LOGGER_PID}"
        fi
        ;;
    *)
        echo "Usage: ${PROGNAME} {start|stop|restart|reload|force-reload|status}"
        exit 1
        ;;
esac
exit 0
# End of this script
