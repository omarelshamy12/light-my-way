import numpy as np
import cv2
import os
import pytesseract
from picamera import PiCamera
from english_ocr.ocr import *
from text_to_speech.tts import *


def get_string(usb=0, image='',flag_arab=0):
    if usb:
        # reading image
        img = cv2.imread(image)
    else:
        # intialize the pi camera
        camera = PiCamera()
        
        #rotate 90 degrees clockwise due to our glasses design
        camera.rotation=90

        # vertical and horizontal flip
#         camera.vflip = True
#         camera.hflip = True

        # setting up the resolution
        camera.resolution = (1920, 1080)

        # start the camera
        camera.start_preview()
        if flag_arab:
            say_arabic("برجاء عدم التحرك يتم التقاط الصورة الان")
        else:
            say("don't move photo is being captured")
        # capture the photo and giving the output path
        camera.capture('/home/pi/Desktop/graduation/src/ocr_english.jpg')

        # stop the camera
        camera.stop_preview()

        # Read image using opencv
        img = cv2.imread('/home/pi/Desktop/graduation/src/ocr_english.jpg')
  

    if flag_arab:
        say_arabic("تم اخذ الصورة والأن تتم عملية القراءة")
    else:
        say("photo has been captured and is being processed now")
    # Extract the file name without the file extension
    file_name = os.path.basename('/home/pi/Desktop/graduation/src/ocr_english.jpg').split('.')[0]
    file_name = file_name.split()[0]
    # Create a directory for outputs
    output_path = os.path.join('output_path', "ocr")
    # create the directory if not present
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    # image preprocessing
    image = image_enhancement(img)
    # Save the filtered image in the output directory
    save_path = os.path.join(output_path, file_name + "filter___" + str('as') + ".png")
    cv2.imwrite(save_path, image)
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(image, lang="eng")
    txt = result.split()
    txt = ' '.join(txt)
    txt = txt.replace("", '')
    return txt