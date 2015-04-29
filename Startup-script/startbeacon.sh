#!/bin/bash

### BEGIN INIT INFO
# Provides:          startbeacon
# Required-Start:    $local_fs 
# Required-Stop:     $local_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: startbeacon
### END INIT INFO

echo "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
echo "Setting up iBeacon"

sudo /home/pi/bluez/bluez-5.11/tools/hciconfig hci0 up
sudo /home/pi/bluez/bluez-5.11/tools/hciconfig hci0 leadv 3
sudo /home/pi/bluez/bluez-5.11/tools/hciconfig hci0 noscan
sudo /home/pi/bluez/bluez-5.11/tools/hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61 03 00 00 02 C8 00

