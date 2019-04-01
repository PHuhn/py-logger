#
#
#
  for f in `ls *.py`; do
	echo "Editing $f"
    sed -i -e "s/\r//" $f
  done
  for f in `ls config.*`; do
	echo "Editing $f"
    sed -i -e "s/\r//" $f
  done
  for f in `ls *.sh`; do
	echo "Editing $f"
    sed -i -e "s/\r//" $f
  done

  sed -i -e "s/## //" -e "s/input()/signal.pause()/" logger.py
  sed -i -e "s/Press \<ENTER\> to exit./Press \^c to exit./" logger.py
  # 
  sudo apt update
  apt list --upgradable
  #
  # Then install the package for Python 3:
  sudo apt install python3-gpiozero
  sudo apt-get install python3-pyodbc
  sudo apt-get install freetds-dev freetds-bin unixodbc-dev tdsodbc

  # configure driver names with odbcinst.ini
  sudo cat <<EOF >> /tmp/odbcinst.ini
[FreeTDS]
Description=FreeTDS Driver
Driver=/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
Setup=/usr/lib/arm-linux-gnueabihf/odbc/libtdsS.so
[SQL Server]
Description=FreeTDS Driver
Driver=/usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
Setup=/usr/lib/arm-linux-gnueabihf/odbc/libtdsS.so
EOF
  sudo cp /tmp/odbcinst.ini /etc/odbcinst.ini
#
