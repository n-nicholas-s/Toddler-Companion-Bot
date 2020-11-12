import RPi.GPIO as GPIO
import time

Servo1 = 17
Servo2 = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(Servo1, GPIO.OUT)
GPIO.setup(Servo2, GPIO.OUT)

p1 = GPIO.PWM(Servo1, 50) # GPIO 17 for PWM with 50Hz
p2 = GPIO.PWM(Servo2, 50) # GPIO 18 for PWM with 50Hz
p1.start(0) # Initialization
p2.start(0) # Initialization

def Forward():
    p1.ChangeDutyCycle(2.5)
    p2.ChangeDutyCycle(12.5)
    time.sleep(1.0)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    
def Backward():
    p1.ChangeDutyCycle(12.5)
    p2.ChangeDutyCycle(2.5)
    time.sleep(1.0)
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    
def CCW():
    p1.ChangeDutyCycle(12.5)
    p2.ChangeDutyCycle(12.5)
    time.sleep(1.5) #Servo Turn 90 degrees
    #time.sleep(2.0) #Servo Turn 180 degrees
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    

def CW():
    p1.ChangeDutyCycle(2.5)
    p2.ChangeDutyCycle(2.5)
    time.sleep(1.5)#Servo Turn 90 degrees
    #time.sleep(2.0) #Servo Turn 180 degrees
    p1.ChangeDutyCycle(0)
    p2.ChangeDutyCycle(0)
    
    
def stop():
    p1.stop()
    p2.stop()
    

def main():
    x = input("Forward/Backward/Counter-Clockwise/Clockwise? F/B/CCW/CW \n").upper()
    if (x == 'F'):
            Forward()
            main()

    elif ( x == 'B'):
        while True:
            Backward()
            main()
            
    elif ( x == 'CCW'):
            CCW()
            main()
            
    elif ( x == 'CW'):
            CW()
            main()
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()

   
    

