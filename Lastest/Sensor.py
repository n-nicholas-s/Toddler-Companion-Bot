import serial

def read_proximity_sensor():
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()

    while True:
        ser.write("M\n".encode('ascii'))
        line = ser.readline().decode('utf-8').rstrip()
        if line != b"":
            data = line.split(" ")
            break
                
    if len(data) == 8: 
        return data
    else:
        return 8190, 8190, 8190, 8190, 0, 0, 0, 0

if __name__ == '__main__':
    read_proximity_sensor()
