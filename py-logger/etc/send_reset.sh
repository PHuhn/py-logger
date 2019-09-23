#!/bin/bash
# ============================================================================
# Send via NRDP a message about a refrigerator
#
 LNUM=$((`grep -n "authorized_tokens"  /usr/local/nrdp/server/config.inc.php | grep "array" | cut -d: -f1` + 1))
 TOKEN=`head -n${LNUM} /usr/local/nrdp/server/config.inc.php | tail -n1 | cut -d"," -f1`
 TOKEN=`echo ${TOKEN} | sed -e 's/^"//' -e 's/"$//'`
 DT=`date +'%Y-%m-%d %H:%M:%S'`
 #
 echo ${TOKEN}
 # OK: refrigerator in room 116
 python3 ../send_nrdp.py -u http://localhost/nrdp/ -t ${TOKEN} -H raspberrypi -c 1 -s refrig-116-sensor-logger -S 0 -o "${DT},refrig-116,refrig,116,OK: refrigerator in room 116"
 echo $?
#
