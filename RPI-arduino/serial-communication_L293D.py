import serial
import time

def Forward():
    ser.write("8".encode('ascii'))

def Backward():
    ser.write("2".encode('ascii'))

def Left():
    ser.write("4".encode('ascii'))
    
def Right():
    ser.write("6".encode('ascii'))
    
def stop():
    ser.write("S".encode('ascii'))

def RotateRight():
    ser.write("9".encode('ascii'))

def RotateLeft():
    ser.write("7".encode('ascii'))
    

def main():

    while True:
        
        x = input("Forward/Backward/Left/Right/Measurements? 8/2/4/6/9/7 \n").upper()
 
        if (x == '8'):
            Forward()
            time.sleep(0.5)
            stop()
            main()
        elif ( x == '2'):
            Backward()
            time.sleep(0.5)
            stop()
            main()
            
        elif ( x == '6'):
            Left()
            time.sleep(0.5)
            stop()
            main()
            
        elif ( x == '4'):
            Right()
            time.sleep(0.5)
            stop()
            main()
            
        elif ( x == '9'):
            RotateRight()
            time.sleep(0.5)
            stop()
            main()
            
        elif ( x == '7'):
            RotateLeft()
            time.sleep(0.5)
            stop()
            main()

        elif ( x == 'M'):
            ser.write("M".encode('ascii'))
            incomingByte = ser.readline().decode('utf-8').rstrip()
            print(incomingByte)

                    
            
        else:
            print("Invalid Input\n")
            

            
    

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.flush()
    main()

    


