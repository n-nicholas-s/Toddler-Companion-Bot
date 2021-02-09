import RPi.GPIO as GPIO
import time
import Sensor
import os
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN , pull_up_down= GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN , pull_up_down= GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN , pull_up_down= GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.IN , pull_up_down= GPIO.PUD_DOWN)
GPIO.setup(5, GPIO.IN , pull_up_down= GPIO.PUD_DOWN)
print("ready")
prev = 0
move = prev

s = 1


def motorMovement (movement): 
    global prev
    
    if prev == movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(1))
    elif prev != movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(0))

    prev = movement



    
        
while True:
    if(GPIO.input(26) == True) or (GPIO.input(19) == True) or (GPIO.input(13) == True) or (GPIO.input(6) == True) or (GPIO.input(5) == True):
        s = 1
    
    while s == 1:

        sensor1, sensor2, sensor3, sensor4, ax, ay, az, o= Sensor.read_proximity_sensor()
        
        if(GPIO.input(26) == True):
        
            print("stop")
            move = 0
           
            
        if(GPIO.input(19) == True):
        
            print("right")
            move = 6
           
            
        if(GPIO.input(13) == True):
        
            print("go")
            move = 8
      
            
        if(GPIO.input(6) == True):
        
            print("back")
            move = 2
       
            
        if(GPIO.input(5) == True):
        
            print("left")
            move = 4
            

            


        if (float(ax) >= 2.5 or float(ax) <= -2.5) or (float(ay) >= 2.5 or float(ay) <= -2.5):
            move = 0
            s = 0
        
        motorMovement(move)

       
            
      
               
