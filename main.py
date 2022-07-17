from arabic_ocr_module import arabic_Ocr
from voice import voice_command_arabic,voice_command_english
from object_module import process_image
from currency_module import currency_camera
from english_ocr_module import get_string
from quran import play_quran
from usb import *
import os
from text_to_speech.tts import *
from emotion_module import *

#check if user is using arabic or english
say_arabic("اذا كنت تريد اللغة العربية قل نعم")

#choose language and feature to use
while(True):
    answer = voice_command_arabic()
    if "نعم" in answer:
        say_arabic("تم اختيار اللغة العربية")
        #features
        say_arabic("اختر من الخواص المتاحة قراءة انجليزية,  قراءة بالعربي,  فحص المكان, حالة الاشخاص, قراءة الفلاشة, قراءة العملات, المصحف المسجل,  سماع صوتيات ")
        say_arabic("اختر من الخواص")
        flag_arabic=1
        break 
    else:
        say("you are in english mode")
        #features
        say("choose from: english OCR, arabic OCR, object detection, emotion detection, read USB, currency detection,  listen to quran, play audio files")
        say("choose from features")
        flag_arabic=0
        break
#the main senario of the program
while(True):
    #take the name of the feature from user
    if flag_arabic:
        text = voice_command_arabic()
    else:
        text=voice_command_english()
    #if user wants english OCR  
    if "english" in text.lower() or "انجليزي" in text :
        #ask user not to move
        if flag_arabic:
            say_arabic("قم بتثبيت يدك من فضلك")
        else:
            say("stabilize your hand  please")
        #capture image and read it by ocr module
        ocr=get_string(flag_arab=flag_arabic)
        #tts the text
        say(ocr)
        continue
    #if user wants egyptian currency detection
    elif "currency" in text or "عملات" in text:
        #capture image and read it by currency module
        currency_camera(flag_arabic)
        continue
    #if user wants arabic OCR
    elif "arabic" in text.lower() or "عربي" in text:
        arabic_txt = arabic_Ocr(flag_arabic)
        say_arabic(arabic_txt)
        continue
    #if user wants object detection
    elif "object" in text or "فحص" in text:
        #capture image and read it by object module and tts the results
        objs_uniques=process_image(flag_arabic)
        if flag_arabic:
            for obj in objs_uniques:
                say_arabic(obj)
        else:
            for obj in objs_uniques:
                say(obj) 
        continue
    #if user wants to detect emotion of faces 
    elif "emotion" in text.lower() or "حاله" in text:
        #capture image and read it by emotion module 
        labels=emotionImage(flag_arabic)
        #tts the labels
        for label in labels:
            if flag_arabic:
                say_arabic(label)
            else:
                say(label)
    #if user wants to read USB
    elif "usb" in text.lower() or "فلاشه" in text:
        #check if user wants automatic or search mode
        if flag_arabic:
            say_arabic("اذا كنت تريد استخدام البحث قل بحث و اذا لا قل لا")
            search = voice_command_arabic()
            if "بحث" in search:
                usb_search(flag_arabic)
            else:
                usb(flag_arabic)
        else:
            say("if you want search mode say search else say no")
            search = voice_command_english()
            if "search" in search:
                usb_search(flag_arabic)
            else:
                usb(flag_arabic)
        continue
    #if user wants to listen to quran
    elif "quran" in text.lower() or "المصحف" in text:
        #play the surrah that user wants
        play_quran()
        continue
    #if user wants exit
    elif "end" in text or "انهي" in text:
        break
    #if user answers is not recognized
    else:
        if flag_arabic:
            say_arabic("كلامك غير واضح")
        else:
            say("i cannot understand you, try again")
