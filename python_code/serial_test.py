import serial

ser = serial.Serial("/dev/ttyAMA0", 9600)

char = ser.read(20)
print char

