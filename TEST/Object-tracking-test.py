# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import os
from threading import Thread

global move, t
move = 0
t = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

#Object Coordinates
def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordinates at \
    X0 = {0} and Y0 =  {1}".format(x, y))

def motorMovement (movement):
    if movement == 4:
        print("[INFO] Robot moving LEFT")
        
    elif movement == 6:
        print("[INFO] Robot moving RIGHT")
        
    elif movement == 8:
        print("[INFO] Robot moving FORWARD")
        
    elif movement == 2:
        print("[INFO] Robot moving BACKWARD")
        
    os.system("python3 motorplate-test.py " + str(movement))
      
# position robot to present object at center of the frame   
def motorMove ():
    global x, move
    
    error = 350 - x

    if (x <= 325):
        move = 4
        motorMovement (move)
 
    if (x >= 375):
        move = 6
        motorMovement (move)
        
    if(x > 325 and x < 375):
        move = 0
        motorMovement (move)


        




# define the lower and upper boundaries of the "red object"
# (or "ball") in the HSV color space, then initialize the
# list of tracked points
colorLower = (161, 100, 100)
colorUpper = (181, 255, 255)
pts = deque(maxlen=args["buffer"])

prev_frame_time = 0

new_frame_time = 0

count = 0


# initialize the video stream and allow the camera sensor to warmup
print("[INFO] waiting for camera to warmup...")
camera = cv2.VideoCapture(0)
time.sleep(2.0)
    
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()
 
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, inverted ("vertical flip" w/ 180degrees),
    # blur it, and convert it to the HSV color space
    frame = imutils.resize(frame, width=700)
    frame = imutils.rotate(frame, angle=180)
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
        if radius >= 80 and radius < 180:   
            count += 1
            
            if count == 25 :
                mapObjectPosition(int(x), int(y))
                thread = Thread(target = motorMove)
                thread.start()
                count = 0
                
        if radius < 80 and radius > 40:
            count += 1
            if count == 25 :
                mapObjectPosition(int(x), int(y))
                move = 8
                motorMovement (move)
                count = 0
        
        if radius > 280:      
            count += 1
            if count == 25 :
                mapObjectPosition(int(x), int(y))
                move = 2
                motorMovement (move)
                count = 0
        if radius < 40 :
            count += 1
            if count == 25 :
                move = 0
                motorMovement(move)
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
    cv2.putText(frame, "FPS: "+ fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 255, 0), 3, cv2.LINE_AA)
 
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