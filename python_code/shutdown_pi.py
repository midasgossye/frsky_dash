#!/bin/python

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def Shutdown(channel):
	os.system("pico2wave -w /home/pi/Frsky-dashboard/sounds/shtdwn.wav 'System shutting down' && aplay /home/pi/Frsky-dashboard/sounds/shtdwn.wav")
	time.sleep(2)
	os.system("sudo shutdown -h now")

GPIO.add_event_detect(12, GPIO.FALLING, callback= Shutdown, bouncetime = 2000)

while 1:
	time.sleep(1)


