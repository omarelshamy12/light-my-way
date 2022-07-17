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
