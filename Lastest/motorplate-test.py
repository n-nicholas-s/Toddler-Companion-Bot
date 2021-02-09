import time                                  #import the time module
import piplates.MOTORplate as MOTOR
import sys
import os
import serial
import Sensor
import RPi.GPIO as GPIO

# dummy = MOTOR.getINTflag0(1)
# intFLAG = 0
# intBITS = 0

prox = 150  #Sensor Distance limit (mm)

a = 0 #Acceleration (sec)

dc = 40   #Duty Cycle (%)

# def moveDone():
#     global intBITS, intFLAG
#     intBITS = MOTOR.getINTflag0(1)
#     intFLAG = 1

def motorINT():
    MOTOR.enabledcSTOPint(0,1)#Start DC motor
    MOTOR.enabledcSTOPint(0,2)
    MOTOR.enabledcSTOPint(0,3)
    MOTOR.enabledcSTOPint(0,4)
    


def Forward():                                    
    MOTOR.dcCONFIG(0,1,'ccw',dc,a)           #configure dc motor 2 on the MOTORplate at address 0 being configured for clockwise 
    MOTOR.dcCONFIG(0,2,'ccw',dc,a)           #motion at a 50% duty cycle and 1 seconds of acceleration 
    MOTOR.dcCONFIG(0,3,'ccw',dc,a)
    MOTOR.dcCONFIG(0,4,'ccw',dc,a)
    
def Backward():
    MOTOR.dcCONFIG(0,1,'cw',dc,a)         
    MOTOR.dcCONFIG(0,2,'cw',dc,a)           
    MOTOR.dcCONFIG(0,3,'cw',dc,a)
    MOTOR.dcCONFIG(0,4,'cw',dc,a)

def Right():
    MOTOR.dcCONFIG(0,1,'cw',dc,a)         
    MOTOR.dcCONFIG(0,2,'ccw',dc,a)           
    MOTOR.dcCONFIG(0,3,'ccw',dc,a)
    MOTOR.dcCONFIG(0,4,'cw',dc,a)

def Left():
    MOTOR.dcCONFIG(0,1,'ccw',dc,a)         
    MOTOR.dcCONFIG(0,2,'cw',dc,a)           
    MOTOR.dcCONFIG(0,3,'cw',dc,a)
    MOTOR.dcCONFIG(0,4,'ccw',dc,a)
    
# def CCW():
#     MOTOR.dcCONFIG(0,1,'ccw',50,2)         
#     MOTOR.dcCONFIG(0,2,'ccw',50,2)           
#     MOTOR.dcCONFIG(0,3,'cw',50,2)
#     MOTOR.dcCONFIG(0,4,'cw',50,2)
# 
# def CW():
#     MOTOR.dcCONFIG(0,1,'cw',50,2)         
#     MOTOR.dcCONFIG(0,2,'cw',50,2)           
#     MOTOR.dcCONFIG(0,3,'ccw',50,2)
#     MOTOR.dcCONFIG(0,4,'ccw',50,2)
    
def Start():
    MOTOR.dcSTART(0,1)#Start DC motor
    MOTOR.dcSTART(0,2)
    MOTOR.dcSTART(0,3)
    MOTOR.dcSTART(0,4)
       
def Speed():                      
    MOTOR.dcSPEED(0,1,75.0)                     #increase speed to 100%
    MOTOR.dcSPEED(0,2,75.0)
    MOTOR.dcSPEED(0,3,75.0)
    MOTOR.dcSPEED(0,4,75.0)  

def Stop():
    MOTOR.dcSTOP(0,1)                             #stop the motor
    MOTOR.dcSTOP(0,2)
    MOTOR.dcSTOP(0,3)
    MOTOR.dcSTOP(0,4)

# GPIO.setmode(GPIO.BCM)  
# GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #set up GPIO 22 as an input 
# GPIO.add_event_detect(22, GPIO.FALLING, callback=moveDone)  # detect interrupts
# motorINT()
# MOTOR.intEnable(1)   


    
def main():
#     global intFLAG, intBITS
    error = 8190
    sensor1 = error 
    sensor2 = error 
    sensor3 = error 
    sensor4 = error 

    x = int(sys.argv[1])
    d = int(sys.argv[2])
    print("Recieve: " + str(x) + ", "  + str(d))

        
    sensor1, sensor2, sensor3, sensor4, ax, ay, az, o= Sensor.read_proximity_sensor()
        
    print(sensor1, sensor2, sensor3, sensor4, ax, ay, az, o)
        

        
    if d == 0 and x != 0 and x != 1 :
#         if (intFLAG == 1):               #check to see if interrupt occurred
#             intFLAG=0               #if INT, clear flag
#             print(intBITS)
        print("[INFO] Robot changing direcction")
        Stop()
        time.sleep(1)
        


            
    if x == 8 :
        if int(sensor1) >= prox:
            Forward()
            Start()
            print("[INFO] Robot moving FORWARD")
        else:
            print ("[INFO] Object Infront of Robot")
            Stop()
            

    elif x == 2:
        if int(sensor2) >= prox:
            Backward()
            Start()
            print("[INFO] Robot moving BACKWARD")
        else:
            print ("[INFO] Object Behind of Robot")
            Stop()

    elif x == 4:
        if int(sensor4) >= prox:
            Left()
            Start()
            print("[INFO] Robot moving Left")
        else:
            print ("[INFO] Object on the Left of Robot")
            Stop()

                
    elif x == 6:
        if int(sensor3) >= prox:
            Right()
            Start()
            print("[INFO] Robot moving RIGHT")
        else:
            print ("[INFO] Object on the Right of Robot")
            Stop()

    elif x == 0:
        Stop()
        print("[INFO] Robot STOPPED")
            
    elif x == 1 :
        Stop()
                    
    else:
        pass



                 

if __name__ == '__main__':
    main()
    GPIO.cleanup()
    print("\n")

    
