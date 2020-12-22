import time                                  #import the time module
import piplates.MOTORplate as MOTOR
import sys

def Forward():                                    
    MOTOR.dcCONFIG(0,1,'ccw',50,2)           #configure dc motor 2 on the MOTORplate at address 0 being configured for clockwise 
    MOTOR.dcCONFIG(0,2,'ccw',50,2)           #motion at a 50% duty cycle and 1 seconds of acceleration 
    MOTOR.dcCONFIG(0,3,'ccw',50,2)
    MOTOR.dcCONFIG(0,4,'ccw',50,2)
    
def Backward():
    MOTOR.dcCONFIG(0,1,'cw',50,2)         
    MOTOR.dcCONFIG(0,2,'cw',50,2)           
    MOTOR.dcCONFIG(0,3,'cw',50,2)
    MOTOR.dcCONFIG(0,4,'cw',50,2)

def Left():
    MOTOR.dcCONFIG(0,1,'cw',50,2)         
    MOTOR.dcCONFIG(0,2,'ccw',50,2)           
    MOTOR.dcCONFIG(0,3,'ccw',50,2)
    MOTOR.dcCONFIG(0,4,'cw',50,2)

def Right():
    MOTOR.dcCONFIG(0,1,'ccw',50,2)         
    MOTOR.dcCONFIG(0,2,'cw',50,2)           
    MOTOR.dcCONFIG(0,3,'cw',50,2)
    MOTOR.dcCONFIG(0,4,'ccw',50,2)
    
def CCW():
    MOTOR.dcCONFIG(0,1,'ccw',50,2)         
    MOTOR.dcCONFIG(0,2,'ccw',50,2)           
    MOTOR.dcCONFIG(0,3,'cw',50,2)
    MOTOR.dcCONFIG(0,4,'cw',50,2)

def CW():
    MOTOR.dcCONFIG(0,1,'cw',50,2)         
    MOTOR.dcCONFIG(0,2,'cw',50,2)           
    MOTOR.dcCONFIG(0,3,'ccw',50,2)
    MOTOR.dcCONFIG(0,4,'ccw',50,2)
    
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
                                                  #wait for deceleration
    
def main():
#       x = input("Forward/Backward/Left/Right/Measurements? 8/2/4/6/9/7 \n").upper()
    
        x = int(sys.argv[1])
#         t = float(sys.argv[2])/2
        print("Recieve: " + str(x))
#         print("Recieve: " + str(t))
        
        if (x == 8): 
            Forward()
            Start()
#             Speed()
#             time.sleep(0.1) 
#             Stop()

        elif ( x == 2):
            Backward()
            Start()
#             Speed()
#             time.sleep(0.1) 
#             Stop()

        elif ( x == 6):
            Left()
            Start()
#             Speed()
#             time.sleep(0.1)  

            
        elif ( x == 4):
            Right()
            Start() 
            Speed()
#             time.sleep(0.1) 


            
#         elif ( x == 9):
#             CCW()
#             Start()
#             time.sleep(1) 
#             Speed()
#             time.sleep(1) 
#             Stop()
# 
#             
#         elif ( x == 7):
#             CW()
#             Start()
#             time.sleep(1) 
#             Speed()
#             time.sleep(1) 
#             Stop()
        elif ( x == 0 ):
            Stop()
           
            
        else:
            print("Invalid Input\n")
            

            
    

if __name__ == '__main__':
    main()
    
