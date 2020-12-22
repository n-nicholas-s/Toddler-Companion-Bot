'''
Object detection and tracking with OpenCV
    ==> Turning a LED on detection and
    ==> Real Time tracking with Pan-Tilt servos 
    Based on original tracking object code developed by Adrian Rosebrock
    Visit original post: https://www.pyimagesearch.com/2016/05/09/opencv-rpi-gpio-and-gpio-zero-on-the-raspberry-pi/
Developed by Marcelo Rovai - MJRoBot.org @ 9Feb2018 
'''

# import the necessary packages
from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

#define Servos GPIOs
panServo = 27
tiltServo = 17

# initialize LED GPIO
redLed = 21

#position servos 
def positionServo (servo, angle):
    os.system("python3 angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 220):
        panAngle += 10
        if panAngle > 140:
            panAngle = 140
        positionServo (panServo, panAngle)
 
    if (x > 280):
        panAngle -= 10
        if panAngle < 40:
            panAngle = 40
        positionServo (panServo, panAngle)

    if (y < 160):
        tiltAngle += 10
        if tiltAngle > 140:
            tiltAngle = 140
        positionServo (tiltServo, tiltAngle)
 
    if (y > 210):
        tiltAngle -= 10
        if tiltAngle < 40:
            tiltAngle = 40
        positionServo (tiltServo, tiltAngle)

print("[INFO] waiting for camera to warmup...")
camera = cv2.VideoCapture(0)
time.sleep(2.0)
    
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)

# define the lower and upper boundaries of the object
# to be tracked in the HSV color space
colorLower = (161, 100, 100)
colorUpper = (181, 255, 255)

# Initialize angle servos at 90-90 position
global panAngle
panAngle = 90
global tiltAngle
tiltAngle =90

count = 0

# positioning Pan/Tilt servos at initial position
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

# loop over the frames from the video stream
while True:
    # grab the next frame from the video stream, Invert 180o, resize the
    # frame, and convert it to the HSV color space
    (grabbed, frame) = camera.read()
    frame = imutils.resize(frame, width=600)
    frame = imutils.rotate(frame, angle=180)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the object color, then perform
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
    if len(cnts) > 1:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            count += 1
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            if count == 25 :
                cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            # position Servo at center of circle
                mapServoPosition(int(x), int(y))
                
                count = 0
            

    

    # if the ball is not detected, turn the LED off

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
 
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff \n")
positionServo (panServo, 90)
positionServo (tiltServo, 90)
cv2.destroyAllWindows()
camera.release()