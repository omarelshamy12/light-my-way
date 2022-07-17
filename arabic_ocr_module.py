from text_to_speech.tts import *
from Arabic_ocr.arabic_ocr import *

def arabic_Ocr(flag_arabic=0):
    #asking user not to move
    if flag_arabic:
        say_arabic("قم بتنثبيت يدك")
    else:
        say("stabilize your hand")
    #capture image
    capture()
    if flag_arabic:
        say_arabic("تم اخذ الصورة انتظر")
    else:
        say("photo has been captured please wait")
        
    #convert image to png as api only works with png
    convert_to_png('/home/pi/Desktop/graduation/src/Arabic_ocr/ocr.png')
    #getting bearer token by mail and key
    bearer=login("*******@gmail.com","*************")
    #getting text from image
    text=proccess("ocr.png",bearer)
    #printing text
    if text == "":
        text="لقد فشلت القراءة"
    print(text)
    return text

      
