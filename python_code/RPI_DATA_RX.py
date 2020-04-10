#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 16:25:26 2017

@author: midas
"""
import os
import serial
import time

millis = lambda: int(round(time.time() * 1000))
def read_data():
    DATA_1 = ser.read().encode("hex")
    DATA_2 = ser.read().encode("hex")
    DATA_3 = ser.read().encode("hex")
    DATA_4 = ser.read().encode("hex")
    
    DATA = DATA_4 + DATA_3 + DATA_2 + DATA_1
    return DATA
def TTS(text):
    TTS_str = "pico2wave -w /home/pi/Frsky-dashboard/sounds/TTS.wav '" + text + "' && aplay /home/pi/Frsky-dashboard/sounds/TTS.wav"
    os.system(TTS_str)
    ser.flushInput()
def play_wav(path_name, file_name):
    play_str = "aplay " + path_name + '/' + file_name
    os.system(play_str)
    ser.flushInput()
    

# === ADC BATTERY CALIBRATION CONSTANT ===
ADC_cal = 5.651248396 
# === Warning thresholds ===
RSSI_warn_thes = 30
BATT_warn_thes = 10.6
#ser = serial.Serial('COM13', 57600, timeout=1)
ser = serial.Serial('/dev/ttyAMA0', 57600, timeout=1)
TTS('Free Sky smart Dashboard')
time.sleep(5)

proc_str = ""
got_telem = False
min_RSSI = 100
voice_delay = 30000
warn_voice_delay = 10000
prev_time = millis()
prev_time_warn = millis()
RSSI = 0
RXBAT = 0
while(1):
    if ((millis() - prev_time) > voice_delay) and got_telem:
        TTS("Battery voltage at " + str(RXBAT) + " Volts.")
        time.sleep(1)
        TTS("R S S I Level at " + str(RSSI))
        prev_time = millis()
        
    if ((millis() - prev_time_warn) > warn_voice_delay):
        if not(got_telem):
            play_wav("/home/pi/Frsky-dashboard/sounds","lost_signal.wav") 
            TTS("No Telemetry available.")
            prev_time_warn = millis()
        elif RSSI < RSSI_warn_thes:
            play_wav("/home/pi/Frsky-dashboard/sounds","lost_signal.wav") 
            TTS("Low R S S I level!")
            prev_time_warn = millis()
        elif RXBAT < BATT_warn_thes:
            play_wav("/home/pi/Frsky-dashboard/sounds","lost_signal.wav") 
            TTS("Low Battery Voltage!")
            prev_time_warn = millis()

    raw_str = ser.read()
    HEX_c = raw_str.encode("hex")
    if HEX_c == '7e':
        raw_str = ser.read()
        HEX_c = raw_str.encode("hex")
        response_ID = HEX_c
    if HEX_c == '10':
        raw_DATA_ID_1 = ser.read().encode("hex")
        raw_DATA_ID_2 = ser.read().encode("hex")
        DATA_ID = raw_DATA_ID_2 + raw_DATA_ID_1
        print "Got data from:", response_ID, "with data type:", DATA_ID
        if DATA_ID == 'f101':
            RSSI_raw = read_data()
            RSSI = int(RSSI_raw, 16)
            if RSSI > 0:
                got_telem = True
            else:
                got_telem = False
            
            print "RSSI=",RSSI, "MIN=", min_RSSI

        elif DATA_ID == 'f102':
            ADC1_raw = read_data()
            ADC1 = round(int(ADC1_raw, 16)*(3.3/255.0), 2)
            print "ADC1=", ADC1
        elif DATA_ID == 'f104':
            RXBAT_raw = read_data()
            RXBAT = round(int(RXBAT_raw, 16)*(3.3/255.0) * ADC_cal, 2)
            print "RxBat=", RXBAT
        elif DATA_ID == 'f105':
            SWR_raw = read_data()
            SWR = int(SWR_raw, 16)
            print "SWR=",SWR
            
