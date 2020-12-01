import serial
import time

def Forward():
    ser.write("F".encode('ascii'))

def Backward():
    ser.write("B".encode('ascii'))

def Left():
    ser.write("L".encode('ascii'))
    
def Right():
    ser.write("R".encode('ascii'))
    
def stop():
    ser.write("S".encode('ascii'))
    

def main():

    while True:
        
        x = input("Forward/Backward/Left/Right/Measurements? F/B/L/R/S/M \n").upper()
 
        if (x == 'F'):
            Forward()
            time.sleep(1)
            stop()
            main()
        elif ( x == 'B'):
            Backward()
            time.sleep(1)
            stop()
            main()
            
        elif ( x == 'L'):
            Left()
            time.sleep(1)
            stop()
            main()
            
        elif ( x == 'R'):
            Right()
            time.sleep(1)
            stop()
            main()
#         elif ( x == 'S'):
#             stop()
#             main()
        elif ( x == 'M'):
            ser.write("M".encode('ascii'))
            incomingByte = ser.readline().decode('utf-8').rstrip()
            print(incomingByte)

                    
            
        else:
            print("Invalid Input\n")
            

            
    

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    main()

    


