from picamera import PiCamera
import time
from currency.currency_function import currency_detection
from num2words import num2words
from subprocess import call
# import pyttsx3
# from tts import Tts
from text_to_speech.tts import *
from PIL import Image, ImageEnhance





def currency_camera(flag_arabic=0):
    # initialize the camera and grab a reference to the raw camera capture
    camera=PiCamera()
#     camera.vflip=True
#     camera.hflip=True
    #rotate 90 degrees clockwise due to our glasses design
    camera.rotation = 90
    #resolution
    camera.resolution=(1920, 1080)
    #contrast and brightness
    camera.contrast = 10
    camera.brightness = 60
    #start camera
    camera.start_preview()

    time.sleep(1)
    path='/home/pi/Desktop/graduation/src/currency.jpg'
    #asking user not to move
    if flag_arabic:
        say_arabic("قم بتنثبيت يدك")
    else:
        say("stabilize your hand")
    #capture image
    camera.capture(path)
    #stop camera
    camera.stop_preview()
    #read the image
    im = Image.open(path)

    #image brightness enhancer
    enhancer = ImageEnhance.Brightness(im)


    factor = 1.2 #brightens the image
    im_output = enhancer.enhance(factor)
    im_output.save(path)
    
    if flag_arabic:
        say_arabic("انتظر قليلا جاري قراءة الصورة")
    else:
        say("please wait photo has been captured and is being processed now")
    #labels with output message
    d= {"5EGP":"five pounds","10EGP":"ten pounds","20EGP":"twenty pounds","50EGP":"fifty pounds","100EGP":"one hundred pounds","200EGP":"two hundred pounds"}
    
    d_arabic= {"5EGP":"خمسة جنيهات","10EGP":"عشرة جنيهات","20EGP":"عشرون جنيه","50EGP":"خمسون جنيه","100EGP":"مائة جنيه","200EGP":"مائتي جنيه"}
    #read image
    try:
        value = currency_detection(path)
        print(value)
        if flag_arabic:
            say_arabic(d_arabic[value])
        else:
            say(d[value])
    #error handling
    except:
        print("error")

