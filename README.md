# frsky_dash

A DIY Frsky telemetry dashboard with Text-To-Speech functionality. Using a RPi to decode the signals sent by the Frsky XJT module and calling out the battery voltage, RSSI level, ... using pico2wave TTS.

## Getting the TTS working

In my experience Pico Text to Speech is one of the best free offline TTS programs out there for linux. An overview of available TTS packages for the RPi can be found [here](https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)). Unfortunately the required packages are no longer part of the standard raspbian distro. 

By following these steps you can download and install the required packages from the older raspbian distro. This method has been tested and proved to be working on raspbian/debian buster February 2020 with a raspberry pi zero V1.3 (source [bugs.launchpad.net](https://bugs.launchpad.net/raspbian/+bug/1835974))

```bash
wget http://archive.raspberrypi.org/debian/pool/main/s/svox/libttspico-utils_1.0+git20130326-3+rpi1_armhf.deb

wget http://archive.raspberrypi.org/debian/pool/main/s/svox/libttspico0_1.0+git20130326-3+rpi1_armhf.deb

sudo apt-get install -f ./libttspico0_1.0+git20130326-3+rpi1_armhf.deb ./libttspico-utils_1.0+git20130326-3+rpi1_armhf.deb
```
