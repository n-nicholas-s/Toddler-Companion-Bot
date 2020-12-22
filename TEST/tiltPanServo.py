#!/usr/bin/env python3
import serial
import random
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()

angle1 = 180
angle2 = 90
    

msg = "" + str(angle1) + ", " + str(angle2)
print(msg)