import numpy as np
import cv2
import tensorflow as tf
import time
import imutils
import paho.mqtt.client as mqtt
import os

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

client.publish("Toddler/info","Currently in Emotion Recognition Mode...")

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
    

def recogniser():
    global s
    count = 0
    check = 0
        
    prev_frame_time = 0

    new_frame_time = 0



    face_detection = cv2.CascadeClassifier('haar_cascade_face_detection.xml')



    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    settings = {
        'scaleFactor': 1.3, 
        'minNeighbors': 5, 
        'minSize': (50, 50)
    }

    labels = ["Neutral","Happy","Sad","Surprise","Angry"]

    model = tf.keras.models.load_model('expression.model') #75% accuracy

    while s != 1:
        ret, img = camera.read()
        img = imutils.rotate(img, angle=0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected = face_detection.detectMultiScale(gray, **settings)
        new_frame_time = time.time() 
      
        
        
        for x, y, w, h in detected:
            cv2.rectangle(img, (x, y), (x+w, y+h), (245, 135, 66), 2)
            cv2.rectangle(img, (x, y), (x+w//3, y+20), (245, 135, 66), -1)
            face = gray[y+5:y+h-5, x+20:x+w-20]
            face = cv2.resize(face, (48,48)) 
            face = face/255.0
            
            predictions = model.predict(np.array([face.reshape((48,48,1))])).argmax()
            state = labels[predictions]
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img,state,(x+10,y+15), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
            
            count += 1
            if count == 15 :
                mapServoPosition(x, y)
                count = 0
                check = 1
                
        if len(detected) == 0 and check == 1:
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
            
        cv2.imshow('Facial Expression', img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if cv2.waitKey(5) != -1:
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':  
    recogniser()
    if s == True:
        client.loop_stop()
        client.publish("Toddler/info","Exiting Emotion Recognition Mode...")
        time.sleep(2)
        client.publish("Toddler/info","Loading...")
        client.disconnect()
        os.system("python3 Main-system.py")            





    
        

