#!/bin/bash
# ============================================================================
# Send via NRDP a message about a refrigerator
#
 PROGNAME=$(basename "$0")
 RPI_HOST=raspberrypi
 SERVICE=refrig-116-sensor-logger
 #
 if [ "$1" == "-h" -o "$1" == "-?" ]; then
   cat <<EOF

  Usage: ${PROGNAME} [options]
  -h    this help text.
  -r    raspberry pi host,   default value: ${RPI_HOST}
  -s    Service name,        default value: ${SERVICE}

  Example:  ${PROGNAME} -r r-pi01 -s refrig-service-01

EOF
   exit
 fi
 #
 while getopts ":r:s:" option
 do
   case "${option}"
   in
     r) RPI_HOST=${OPTARG};;
     s) SERVICE=${OPTARG};;
   esac
 done
 echo "Host: ${RPI_HOST}, service: ${SERVICE}"
 #
 LNUM=$((`grep -n "authorized_tokens"  /usr/local/nrdp/server/config.inc.php | grep "array" | cut -d: -f1` + 1))
 TOKEN=`head -n${LNUM} /usr/local/nrdp/server/config.inc.php | tail -n1 | cut -d"," -f1`
 TOKEN=`echo ${TOKEN} | sed -e 's/^"//' -e 's/"$//'`
 DT=`date +'%Y-%m-%d %H:%M:%S'`
 #
 # echo ${TOKEN}
 # : Danger refrigerator alert in room 116
 python3 ../send_nrdp.py -u http://localhost/nrdp/ -t ${TOKEN} -H ${RPI_HOST} -c 1 -s ${SERVICE} -S 1 -o "${DT},refrig-116,refrig,116,WARNING: Danger refrigerator alert in room 116"
 echo $?
#