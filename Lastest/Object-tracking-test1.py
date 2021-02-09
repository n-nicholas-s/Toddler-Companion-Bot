# import the necessary packages
import paho.mqtt.client as mqtt
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import os
from threading import Thread


tiltServo = 17

prev = None

w = 700

r = 30

s = None

def positionServo (servo, angle):
    os.system("python3 angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))
    
def mapServoPosition (x, y):

    global tiltAngle

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
        

global tiltAngle
tiltAngle =80

# positioning Pan/Tilt servos at initial position
# positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

#Object Coordinates
def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordinates at \
    X0 = {0} and Y0 =  {1}".format(x, y))
       

def motorMovement (movement): 
    global prev
    
    if prev == movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(1))
    elif prev != movement:
        os.system("python3 motorplate-test.py " + str(movement) + " " + str(0))

    prev = movement
  
def motorMove ():
    global x, move, w
    
    error = w/2- x

    if (x <= w/2 - r):
        move = 4
        motorMovement (move)
 
    if (x >= w/2 + r):
        move = 6
        motorMovement (move)
        
    if(x > w/2 - r and x < w/2 + r):
        move = 0
        motorMovement (move)
        print("[INFO] Robot is Centred on the Object")

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

client.publish("Toddler/info","Currently in Object Tracking Mode...")
    
client.loop_start()


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())



def tracker():
    global x , s
    # define the lower and upper boundaries of the "red object"
    # (or "ball") in the HSV color space, then initialize the
    # list of tracked points
    colorLower = (161, 100, 100)
    colorUpper = (181, 255, 255)
    pts = deque(maxlen=args["buffer"])

    prev_frame_time = 0

    new_frame_time = 0

    count = 0
    
    check = 0


    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] waiting for camera to warmup...")
    camera = cv2.VideoCapture(0)
    time.sleep(2.0)
        
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)

    # keep looping
    while s != 1:
        # grab the current frame
        (grabbed, frame) = camera.read()
     
        # if we are viewing a video and we did not grab a frame,
        # then we have reached the end of the video
        if args.get("video") and not grabbed:
            break
     
        # resize the frame, inverted ("vertical flip" w/ 180degrees),
        # blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width= w)
        frame = imutils.rotate(frame, angle=0)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
        # construct a mask for the color "red", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, colorLower, colorUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
     
        # only proceed if at least one contour was found
        if len(cnts) > 2:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid

            
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
            #print(radius)
            # draw the circle and centroid on the frame,
                # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)


            
     
            # only proceed if the radius meets a minimum size
            if radius >= 80 and radius < 280:   #Left and Right
                count += 1
                
                if count == 15 :
                    mapObjectPosition(int(x), int(y))
                    thread = Thread(target = motorMove)
                    thread.start()
                    mapServoPosition(x, y)
                    check = 1
                    count = 0
                    info = "[INFO] Robot Detect Object"
                    client.publish("Toddler/info",info)
                    
            if radius < 80 and radius > 40:   #Forward
                count += 1
                if count == 15 :
                    mapObjectPosition(int(x), int(y))
                    move = 8
                    motorMovement (move)
                    mapServoPosition(x, y)
                    check = 1
                    count = 0
                    info = "[INFO] Robot Detect Object"
                    client.publish("Toddler/info",info)
            
            if radius > 280:      #Backward
                count += 1
                if count == 15 :
                    mapObjectPosition(int(x), int(y))
                    move = 2
                    motorMovement (move)
                    mapServoPosition(x, y)
                    check = 1
                    count = 0
                    info = "[INFO] Robot Detect Object"
                    client.publish("Toddler/info",info)
            if radius < 40:
                count += 1
                if count == 15 :
                    move = 0
                    motorMovement(move)
                    if check == 1:
                        positionServo (tiltServo, 80)
                        check = 0
                    info = "[INFO] Robot Cannot Detect Object"
                    client.publish("Toddler/info",info)
 
                    count = 0
                    
        elif len(cnts) < 2:
            count += 1
            if count == 15 :
                info = "[INFO] Robot Cannot Detect Object"
                client.publish("Toddler/info",info)
                move = 0
                motorMovement(move)
                if check == 1:
                    positionServo (tiltServo, 80)
                    check = 0
                count = 0
                

     
        # update the points queue
        pts.appendleft(center)
        
            # loop over the set of tracked points
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue
     
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            
        new_frame_time = time.time() 
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
        cv2.putText(frame, "FPS: "+ fps, (600, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)
     
        # show the frame to our screen
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)
        

        key = cv2.waitKey(1) & 0xFF
        
     
        # if the 'q' key is pressed, stop the loop
        if key == ord("q"):
            break
        


    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':  
    tracker()
    if s == True:
        client.loop_stop()
        client.publish("Toddler/info","Exiting Object Tracking Mode...")
        time.sleep(2)
        client.publish("Toddler/info","Loading...")
        client.disconnect()
        os.system("python3 Main-system.py")            
