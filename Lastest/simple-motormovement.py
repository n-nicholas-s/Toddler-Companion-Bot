import os
from threading import Thread, Event
import time

prev = 0
x = 0



 
 
# It sends signals from one to another thread
bridge = Event()
 
 
def func():
    global x
    while True:
        x = input("Forward/Backward/Left/Right/Measurements? 8/2/4/6/0 \n").upper()
        motorMovement(x)
        time.sleep(0.1)
 

        
def motorMovement (movement): 
    global prev
    
    if prev == movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(1) + " " + str(1))
    elif prev != movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(0) + " " + str(1))


    prev = movement

def main():

    while True:

        main_thread = Thread(target=func)
        
        # We start the thread and will wait for 0.5 seconds then the code will continue to execute
        main_thread.start()
    
        main_thread.join(timeout=0.1)
        
        motorMovement(x)



        
    


if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        exit()
        

    
    

        

    
    
    

    
