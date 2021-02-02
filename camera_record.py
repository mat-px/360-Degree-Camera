#!/home/pi/.virtualenvs/record-jv0J4ogK/bin/python
import RPi.GPIO as GPIO
import cv2
import time
import glob
import os
from pathlib import Path

# declare reused values
BTN_GPIO_PIN = 5
VID_WIDTH = 640
VID_HEIGHT = 480
DEBOUNCE_TIME = .25
Path("/tmp/video").mkdir(parents=True, exist_ok=True)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #GPIO pin 27 is initially UP

cap1 = cv2.VideoCapture(0) #Define what camera is being captured
cap2 = cv2.VideoCapture(2)
cap1.set(cv2.CAP_PROP_FPS, 25) #Sets recording framerate cap
cap2.set(cv2.CAP_PROP_FPS, 25)

fourcc = cv2.VideoWriter_fourcc(*'XVID') # Codec for AVI file

cam_on = False # don't read from the camera until button state changes

a = 1
while(a == 1):  #main loop
    while not cam_on: # just wait for the next button press and do not record
        if GPIO.input(BTN_GPIO_PIN) == False: #Breaks if button is pressed
            cam_on = True
            time.sleep(DEBOUNCE_TIME)
            break
        
 
    
    # Start at one by default
    previous_instance = 1
    # Get all .avi files in the video directory
    files = glob.glob('/tmp/video/*.avi')
    # If we found any files, get the newest one by time and get the number at the end of it's filenameid
    if len(files) > 0:
        newest = max(files, key=os.path.getctime)
        previous_instance = int(Path(newest).stem.split('_')[-1]) + 1

    # Set new filenames based on previous filenames
    cam1_filename = '/tmp/video/cam_1_' + str(previous_instance) + '.avi'  #Creates individually named files
    cam2_filename = '/tmp/video/cam_2_' + str(previous_instance) + '.avi'
    
    out = cv2.VideoWriter(cam1_filename, fourcc, 10, (VID_WIDTH, VID_HEIGHT))
    out2 = cv2.VideoWriter(cam2_filename, fourcc, 10, (VID_WIDTH, VID_HEIGHT))
    
    while cam_on:  #record frames when camera is supposed to be on
        ret, frame = cap1.read() # reads frames from a camera
        ret, frame2 = cap2.read() # ret checks return at each frame
        out.write(frame) # output the frame
        out2.write(frame2)

        cv2.imshow('One', frame) # Show what is being recorded
        cv2.imshow('Two', frame2)

        cv2.waitKey(1)
        if GPIO.input(BTN_GPIO_PIN) == False: #Breaks if button is pressed
            cam_on = False
            out.release() # After we release our webcam, we also release the output
            out2.release()
            cv2.destroyAllWindows() # De-allocate any associated memory usage
            time.sleep(DEBOUNCE_TIME)
            break

cap1.release()
cap2.release() # Close the window / Release webcam