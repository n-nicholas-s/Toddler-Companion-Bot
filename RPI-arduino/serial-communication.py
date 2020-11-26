
import serial

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
        x = input("Forward/Backward/Counter-Clockwise/Clockwise? F/B/L/R/S \n").upper()
        if (x == 'F'):
            Forward()
            main()
        elif ( x == 'B'):
            Backward()
            main()
            
        elif ( x == 'L'):
            Left()
            main()
            
        elif ( x == 'R'):
            Right()
            main()
        elif ( x == 'S'):
            stop()
            main()
        else:
            print("Invalid Input\n")
    

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    main()

    


