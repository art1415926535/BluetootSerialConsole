Bluetooth Serial Console
=============

Example of work:
```
python3 main.py
> help

Commands:
 connect [DEVICE_NAME]:  search new device or connect by DEVICE_NAME
 disconnect :  disconnect from device
 send DATA :  send DATA
 help :  this text
 exit :  stops console loops and exits program

> connect
Searching for devices...
Select your device by entering its coresponding number or type [exit]:
1: C0:14:3D:C8:78:FA
2: 00:16:74:E0:63:17 ST DISCO2 R16
3: 00:13:01:08:17:72 linvor
> 3
You have selected linvor
Connected!
00:13:01:08:17:72 [linvor]> send hello
00:13:01:08:17:72 [linvor]> send bye
00:13:01:08:17:72 [linvor]> disconnect
> connect linvor
Searching for linvor
You have selected linvor
Connected!
00:13:01:08:17:72 [linvor]> exit
```
