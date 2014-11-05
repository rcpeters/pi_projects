# Quick Re-Start 
Assume you already have followed [https://learn.adafruit.com/pibeacon-ibeacon-with-a-raspberry-pi/adding-ibeacon-data](https://learn.adafruit.com/pibeacon-ibeacon-with-a-raspberry-pi/adding-ibeacon-data) once.

       cd ~/bluez/bluez-5.11/
       sudo tools/hciconfig hci0 up
       sudo tools/hciconfig hci0 leadv
       sudo tools/hciconfig hci0 noscan
       sudo tools/hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 1A 1A FF 4C 00 02 15 E2 0A 39 F4 73 F5 4B C4 A1 2F 17 D1 AD 07 A9 61 00 00 00 00 C8 00

Note: for Android "BEACONinside" would scan and find it. 
