#!/bin/bash
#
# ============================================================================
# Copyright (c) 2019 Northern Software Group
# This software is owned by Northern Software Group.  Unauthorized copying,
# distribution or changing of this software is prohibited.
#
# Installing py-logger
#  Written by: Phil Huhn
#  Version 1
#
# program values:
PROGNAME=$(basename "$0")
REVISION="1.0.1"
# Varialbes:
LOG_DIR=/var/log
LOCAL_DIR=/usr/local
INIT_DIR=/etc/init.d
# place to put file logs '/var/log'
if [ ! -d "${LOG_DIR}/py-logger" ]; then
    echo "${PROGNAME}:${LINENO}: making ${LOG_DIR}/py-logger directory."
    sudo mkdir ${LOG_DIR}/py-logger
fi
# place to put py-logger source
if [ ! -d "${LOCAL_DIR}/py-logger" ]; then
    echo "${PROGNAME}:${LINENO}: making ${LOCAL_DIR}/py-logger directory."
    sudo mkdir ${LOCAL_DIR}/py-logger
fi
#
if [ ! -f "${LOCAL_DIR}/py-logger/config.json" ]; then
    echo "${PROGNAME}:${LINENO}: copying to ${LOCAL_DIR}/py-logger directory."
    sudo cp ../config.* ${LOCAL_DIR}/py-logger/.
    sudo cp ../*.py ${LOCAL_DIR}/py-logger/.
    echo "${PROGNAME}:${LINENO}: editing ${LOCAL_DIR}/py-logger/config.json file."
    sudo sed -i -e "s/\"OutputLogger\": \"Console\"/\"OutputLogger\": \"File\"/" ${LOCAL_DIR}/py-logger/config.json
    sudo sed -i -e "s/\"Folder\": \"\"/\"Folder\": \"\/var\/log\/py-logger\"/" ${LOCAL_DIR}/py-logger/config.json
	#
	# configure and install systemd service
    cat << EOF > /tmp/py-logger.service
[Unit]
Description=py-logger
BindTo=network.target

[Install]
WantedBy=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/py-logger/logger.py
WorkingDirectory=/usr/local/py-logger
Type=simple
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

EOF
	mv /tmp/py-logger.service /etc/systemd/system/.
    systemctl enable /etc/systemd/system/py-logger.service
    systemctl start py-logger
	#
fi
#
if [ -f "py-logger.sh" ]; then
    echo "${PROGNAME}:${LINENO}: copying initctl script py-logger.sh to ${INIT_DIR} directory."
    # Usage: py-logger.sh {start|stop|restart|status}
    sudo cp ./py-logger.sh ${INIT_DIR}/.
    sudo chmod 755 ${INIT_DIR}/py-logger.sh
    sudo ln -s ${INIT_DIR}/py-logger.sh /etc/rcS.d/S99py-logger
fi
# End of this script
