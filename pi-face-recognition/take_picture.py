import picamera
import time
import os



x = input("Do you want register your face into Recognisable List? Y/N \n").upper()
if (x =='Y') :
    Name = input("Enter your name: ")
    
    with picamera.PiCamera() as camera: #use PiCamera
        camera.start_preview()
        os.mkdir('/home/pi/pi-face-recognition/dataset/'+ Name)
        try:
            for i, filename in enumerate(
                    camera.capture_continuous
                    ('/home/pi/pi-face-recognition/dataset/'+ Name +'/{counter:04d}.jpg')): #Capture and name
                print(filename)
                time.sleep(1)
                if i == 3:
                    break
        finally:
            camera.stop_preview()
else:
    exit()