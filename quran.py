from text_to_speech.tts import *
from voice import voice_command_arabic,voice_command_english
import os
import  vlc
import time


def play_quran():
    #reading names of suwar of quran
    #encoding='utf-8' to be able read arabic
    file = open("Quran.txt","r",encoding='utf-8')
    #read line by line
    quran = file.readlines()
    q=[]
    #appending in a list q
    for i in range(len(quran)):
        q.append(quran[i].replace("سورة","").replace("ة","ه").replace("\n","").strip())
    d={}
#     print(q)
    #generating names of mp3 files
    for i in range(114):
        if i<9:
            d[q[i]]="00"+str(i+1)
        elif i<99:
            d[q[i]]="0"+str(i+1)
        else:
            d[q[i]]=str(i+1)
    #001.mp3 is the first sura of quran
    # d["الفاتحة"]="001"
    #asking user to tell the surah name
    say_arabic("قل اسم السورة")
    #getting surrah name
    text = voice_command_arabic()
    # print(text)
    #accesing the dictionary by name to form the path to mp3 of surrah
    for i in d.keys():
        if i == text:
    #         print("yes")
    #         print(i)
            #path of surrah
            surah="/home/pi/Desktop/quran/"+d[i]+".mp3"
            #using vlc library
            p = vlc.MediaPlayer(surah)
            #play
            p.play()
            time.sleep(30)
            p.stop()
        else:
            say_arabic("لا يوجد سورة بهذا الاسم")
        
# play_quran()