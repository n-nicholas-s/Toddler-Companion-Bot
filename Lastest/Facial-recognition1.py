import cv2
import numpy as np
import os
import time
import paho.mqtt.client as mqtt
import temp
import grove_d6t
import pigpio

#define Servos GPIOs
# panServo = 27
tiltServo = 17





s = None

def on_connect(client, userdata, flags, rc):
    print("Connected With Result Code: {}".format(rc))
   
def on_disconnect(client, userdata, rc):
    print("[INFO] Connection has Disconnected")
    
def on_message(client, userdata, message):
    global s
    print("received message: ", str(message.payload.decode("utf-8")))
    s = int(message.payload.decode("utf-8"))
    
broker = "broker.hivemq.com"
# broker = "broker.emqx.io"

port = 1883

client = mqtt.Client(clean_session=True)

client.on_connect = on_connect

client.on_disconnect = on_disconnect

client.on_message = on_message

client.connect(broker, port)
print("[INFO] Connecting to broker")
    
client.subscribe("Toddler/move")

client.publish("Toddler/info","Currently in Facial Recognition Mode...")
    
client.loop_start()

def positionServo (servo, angle):
    os.system("python3 angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

def mapServoPosition (x, y):
#     global panAngle
    global tiltAngle
#     if (x < 220):
#         panAngle += 10
#         if panAngle > 140:
#             panAngle = 140
#         positionServo (panServo, panAngle)
#  
#     if (x > 280):
#         panAngle -= 10
#         if panAngle < 40:
#             panAngle = 40
#         positionServo (panServo, panAngle)

    if (y < 160):
        tiltAngle += 20
        if tiltAngle > 140:
            tiltAngle = 140
        positionServo (tiltServo, tiltAngle)
 
    if (y > 210):
        tiltAngle -= 20
        if tiltAngle < 40:
            tiltAngle = 40
        positionServo (tiltServo, tiltAngle)
        
# global panAngle
# panAngle = 90
global tiltAngle
tiltAngle =80

# positioning Pan/Tilt servos at initial position
# positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

def read_temperature():
        d6t = grove_d6t.GroveD6t()
        status = ("[..INITIATING SENSOR..]")
        temp = 37.5 #fever temperature
        Highest = 0
        tpn, tptat = d6t.readData()

        if tpn == None:
            pass
            return "", ""
                
        else:                      
            for i in tpn:
                if i > Highest:
                    Highest = i
                    data = str(Highest)
                else:
                    pass
              
                        
            chk = len([i for i in tpn if i >= temp])
                    
                    
                    
            if (chk > 0):
                    
                status = ("[FEVER DETECTED!]")
                    
            else:
                    
                status = ("[Normal]")
                        
                return status, data

def recogniser():
    count = 0
    check = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('/home/pi/Toddler-Companion-Bot-main/TEST/trainer/trainer.yml')
    cascadePath = "/home/pi/Toddler-Companion-Bot-main/TEST/haar_cascade_face_detection.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    #indcate id counter
    id = 0
    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Nicholas', 'Barack Obama', 'Lee Hsien Loong', 'Toddler', 'Z'] 
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    prev_frame_time = 0
    new_frame_time = 0
    global s
    while s != 1 :
        
        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
         
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )
        
        new_frame_time = time.time()
        

        
        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                client.publish("Toddler/info","Person recognised: " + str(id)) 
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
                client.publish("Toddler/info","Person not recognised !" + str(id)) 
            
            

                
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            count += 1
            if count == 5 :
                mapServoPosition(x, y)
                status, data = read_temperature()
                client.publish("Toddler/temperature",str(data))
                client.publish("Toddler/tempstr",status) 
                count = 0
                check = 1
        
        
        if len(faces) == 0 and check == 1:
            positionServo (tiltServo, 80)
            check = 0
            

            
        # Calculating the fps 
          
        # fps will be number of frame processed in given time frame 
        # since their will be most of time error of 0.001 second 
        # we will be subtracting it to get more accurate result 
        fps = 1/(new_frame_time-prev_frame_time) 
        prev_frame_time = new_frame_time 
          
        # converting the fps into integer 
        fps = int(fps) 
          
        # converting the fps to string so that we can display it on frame 
        # by using putText function 
        fps = str(fps) 
          
        # puting the FPS count on the frame 
        cv2.putText(img, "FPS: "+ fps, (500, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)
        
        client.publish("Toddler/info","Currently in Facial Recognition Mode...")
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        

    # Do a bit of cleanup
    print("\n[INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':  
    recogniser()
    if s == True:
        client.loop_stop()
        client.publish("Toddler/temperature","")
        client.publish("Toddler/tempstr","") 
        client.publish("Toddler/info","Exiting Facial Recognition Mode...")
        time.sleep(2)
        client.publish("Toddler/info","Loading...")
        client.disconnect()
        os.system("python3 Main-system.py")      