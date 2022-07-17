import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from Object_Detection.object import *
from text_to_speech.tts import *


def process_image(flag_arabic=0):
    # initialize the camera and grab a reference to the raw camera capture
    camera=PiCamera()

    #rotate 90 degrees clockwise due to our glasses design
    camera.rotation=90
    #resolution
    camera.resolution=(1920, 1080)
    #start camera
    camera.start_preview()
    #asking user not to move
    if flag_arabic:
        say_arabic("لا تتحرك جاري التقاط الصورة")
    else:
        say("don't move photo is being captured")
    #give time for camera to start
    time.sleep(1)
    #grab image
    camera.capture('/home/pi/Desktop/graduation/src/Object_Detection/object.jpg')
    #stop camera
    camera.stop_preview()
    #close camera
    img=cv2.imread('/home/pi/Desktop/graduation/src/Object_Detection/object.jpg')
    #return results from object detection
    result, objectInfo ,objs= getObjects(img,0.6,0.2,flag_arabic=flag_arabic)
    #write results to file
    cv2.imwrite("/home/pi/Desktop/graduation/src/Object_Detection/Output.jpg",result)
    
#     print(objs)
    #lists for objects
    objs_unique=[]
    objs_unique_num=[]
    objs_uniques=[]
#     print(objs)
    #loop through objects
    for obj in objs:

        if flag_arabic:
            if objs.count(obj)>1 and obj not in objs_unique:
                objs_unique.append(obj)
                objs_unique_num.append(str(objs.count(obj))+" "+obj)
                objs_uniques.append("اكثر من "+obj)
            elif objs.count(obj)==1 and obj not in objs_unique:
                objs_unique.append(obj)
                objs_unique_num.append(str(objs.count(obj))+" "+obj)
                objs_uniques.append(obj)
            
        else:
            if objs.count(obj)>1 and obj not in objs_unique:
                objs_unique.append(obj)
                objs_unique_num.append(str(objs.count(obj))+" "+obj)
                objs_uniques.append(obj+"s")
            elif objs.count(obj)==1 and obj not in objs_unique:
                objs_unique.append(obj)
                objs_unique_num.append(str(objs.count(obj))+" "+obj)
                objs_uniques.append(obj)
    #return objects
    return objs_uniques
print(process_image(flag_arabic=0))
