from voice import voice_command_arabic,voice_command_english
import time
import os
from english_ocr.ocr import *
from flash_memory.getfiles import get_files
import shutil
import docx2txt
import re
from text_to_speech.tts import *
import vlc
import pdfplumber

#function to read text from pdf
def read_pdf(path):
    text=""
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages
        for i,pg in enumerate(pages):
            text += pages[i].extract_text()
    say(text)
#flag_arabic to check if the user is in arabic mode or not


#search mode
def usb_search(flag_arabic=0):
    #get files from usb
    files=get_files()
    images=files["image"]
    music_files=files["music"]
    pdf_files=files["pdf"]
    txt_files=files["txt"]
    doc_files=files["doc"]
    #flag to check if user make more than one process
    flag_end=0
    while(True):
        if flag_arabic ==0 :
            #if user wants to exit
            if flag_end:
                say("to exit say end")
                end=voice_command_english()
                if "end" in end :
                    break
            #taking search keyword from user
            say("say the file name you want in english")
            text=voice_command_english()
            text=text.lower()
            #checks if file is image
            for image in images:
                if text in image.lower():
                    say("image is found and will be read now")
                    #read image by english ocr
                    txt=get_string(1,image)
                    #tts the text
                    say(txt)
                    flag_end=1
                    continue
            #checks if file is pdf
            for pdf in pdf_files:
                if text in pdf.lower():
                    say("pdf is found and will be read now ")
                    #read pdf by tts
                    read_pdf(pdf)
                    flag_end=1
                    continue
            #checks if file is txt
            for txt in txt_files:
                if text in txt.lower():
                    say("text file is found and will be read now")
                    f=open(txt,'r')
                    flag_end=1
                    #read text file by tts
                    say(f.read())
                    continue
            #checks if file is word document
            for doc in doc_files:
                if text in doc.lower():
                    say("word file is found and will be read now")
                    txt=re.sub(' +', ' ', docx2txt.process(doc))
                    txt=txt.split()
                    txt=' '.join(txt)
                    #read word file by tts
                    say(txt)
                    flag_end=1
                    continue
            #checks if file is music
            for music in music_files:
                if text in music.lower():
                    say("sound is found and will be played now")
                    shutil.copy(music,"/home/pi/Desktop/1.mp3")
                    #using vlc library
                    p = vlc.MediaPlayer("/home/pi/Desktop/1.mp3")
                    #play
                    p.play()
                    # time.sleep(30)
                    p.stop()
                    #delete file after playing
                    os.remove("/home/pi/Desktop/1.mp3")
                    flag_end=1
                    continue
            #if file is not found
            say("no search results try again")
                    
        else :
            #if user wants to exit
            if flag_end:
                say_arabic("للانهاء قل انهي")
                end=voice_command_arabic()
                if "نهي" in end :
                    break
            #taking search keyword from user
            say_arabic("اهلا بك في قسم قراءة الفلاشة")
            say_arabic("قل كلمة البحث التي تريدها بالعربي")
            text=voice_command_arabic()
            #checks if file is image
            for image in images:
                if text in image.lower():
                    say_arabic("تم العثور على الصورة وسيتم القراءة الأن")
                    #read image by  ocr
                    txt=get_string(1,image,flag_arabic=1)
                    #tts the text
                    say_arabic(txt)
                    flag_end=1
                    continue
            #checks if file is pdf
            for pdf in pdf_files:
                if text in pdf.lower():
                    say_arabic("تم العثور على الملف المكتوب وسيتم قراءته الأن")
                    #read pdf by tts
                    read_pdf(pdf)
                    flag_end=1
                    continue
            #checks if file is txt
            for txt in txt_files:
                if text in txt.lower():
                    say_arabic("تم العثور على الملف المكتوب وسيتم قراءته الأن")
                    f=open(txt,'r')
                    flag_end=1
                    #read text file by tts
                    say_arabic(f.read())
                    continue
            #checks if file is word document
            for doc in doc_files:
                if text in doc.lower():
                    say_arabic("تم العثور على الملف المكتوب وسيتم قراءته الأن")
                    txt=re.sub(' +', ' ', docx2txt.process(doc))
                    txt=txt.split()
                    txt=' '.join(txt)
                    #read word file by tts
                    say_arabic(txt)
                    flag_end=1
                    continue
            #checks if file is music
            for music in music_files:
                if text in music.lower():
                    say_arabic("تم العثور على الملف وسيتم الاستماع الأن")
                    shutil.copy(audio,"/home/pi/Desktop/1.mp3")
                    #using vlc library
                    p = vlc.MediaPlayer("/home/pi/Desktop/1.mp3")
                    #play
                    p.play()
                    time.sleep(30)
                    p.stop()
                    #delete file after playing
                    os.remove("/home/pi/Desktop/1.mp3")
                    flag_end=1
                    continue
            if flag_end == 0 :
                say_arabic("لا يوجد ملفات بهذا الاسم")
#auto mode
def usb(flag_arabic=0):
        #get all files in the flash memory
        files=get_files()
        #flag to check if user make more than one process
        flag_end=0
        
        while(True):
            if flag_arabic:
                #welcome message
                say_arabic("اهلا بك في قسم قراءة الفلاشة اختر من ")
                #if user wants to exit
                if flag_end:
                    say_arabic("للانهاء قل انهي")
                    end=voice_command_arabic()
                    if "نهي" in end :
                        break
                else:
                    say_arabic("لو كنت تريد قراءة الصور قل صورة")
                    say_arabic("لو كنت تريد السماع الى الاصوتيات قل سماع")
                    say_arabic("لو كنت تريد قراءة ملف مكتوب قل ملف")
                #taking type of file from user    
                text=voice_command_arabic()
                #checks if file is pdf or word or txt
                if "ملف" in text:
                    say_arabic("اختار صيغة الملف")
                    say("PDF word text")
                    #taking type of file from user
                    text=voice_command_english()
            if flag_arabic == 0:
                #welcome message
                say("welcome to flash drive module choose a feature")
                #if user wants to exit
                if flag_end:
                    say("to exit say end")
                    end=voice_command_english()
                    if "end" in end :
                        break
                else:
                    
                    say("say ocr if you want to use ocr on image")
                    say("say music if you want to play music files")
                    say("say pdf if you want to read pdf files")
                    say("say text if you want to read text files")
                    say("say word if you want to read doc files")
                #taking type of file from user
                text=voice_command_english()
            #if you want to read text in images
            print(text)
            #checks if file is image
            if "ocr" in text.lower() or "صور"in text:
                images=files["image"]
                for image in images:
                    if flag_arabic:
                        say_arabic("اسم الملف هو")
                        say(image.split('/')[-1].split('.')[0])
                        say_arabic("للقراءة قل نعم")
                        #read answer from user
                        read=voice_command_arabic()
                        if "نعم" in read:
                            #read image by ocr
                            txt=get_string(1,image)
                            #tts the text
                            say(txt)
                        else:
                            continue
                       
                        
                    else:
                        say("file name is"+image.split('/')[-1].split('.')[0])
                        say("say ok to read")
                        #read answer from user
                        read=voice_command_english()
                        if "ok" in read:
                            #read image by ocr
                            txt=get_string(1,image)
                            #tts the text   
                            say(txt)
                        else:
                            continue
                flag_end=1
                continue

            #checks if file is music
            if "music" in text or "سماع"in text:
                music_files=files["music"]
                
                for audio in music_files:
                    if flag_arabic:
                        say_arabic("اسم الملف هو")
                        say(audio.split('/')[-1].split('.')[0])
                        say_arabic("للاستماع اليه قل نعم")
                        read=voice_command_arabic()
                        if "نعم" in read:
                            #copying file from usb 
                            shutil.copy(audio,"/home/pi/Desktop/1.mp3")
                            #play mp3
                            #using vlc library
                            p = vlc.MediaPlayer("/home/pi/Desktop/1.mp3")
                            #play
                            p.play()
                            time.sleep(30)
                            p.stop()
                            #delete file after playing
                            os.remove("/home/pi/Desktop/1.mp3")
                        else:
                            continue
            #         print(audio)
            #
                    else:
                            say("file name is"+audio.split('/')[-1].split('.')[0])
                            say("say play to play")
                            read=voice_command_english()
                            if "play" in read:
                                #copying file from usb 
                                shutil.copy(audio,"/home/pi/Desktop/1.mp3")
                                
                                #using vlc library
                                p = vlc.MediaPlayer("/home/pi/Desktop/1.mp3")
                                #play
                                p.play()
                                time.sleep(30)
                                p.stop()
                                #delete file after playing
                                os.remove("/home/pi/Desktop/1.mp3")
                            else:
                                continue
                    
                flag_end=1
                continue
            #checks if file is pdf
            if "pdf" in text:
                pdf_files=files["pdf"]
                for pdf in pdf_files:
                    if flag_arabic:
                        say_arabic("اسم الملف هو")
                        say(pdf.split('/')[-1].split('.')[0])
                        say_arabic("للقراءة قل نعم")
                        #read answer from user
                        read=voice_command_arabic()
                        if "نعم" in read:
                            #read pdf file
                            read_pdf(pdf)
                        else:
                            continue
        
                    else:
                            say("file name is"+pdf.split('/')[-1].split('.')[0])
                            say("say ok to read")
                            #read answer from user
                            read=voice_command_english()
                            if "ok" in read:
                                #read pdf file
                              read_pdf(pdf)
                            else:
                                continue
                    
                flag_end=1

                continue   
            #checks if file is txt
            if "text" in text:
                txt_files=files["txt"]
                for txt in txt_files:
            #         print(txt)
                    
                    if flag_arabic:
                        say_arabic("اسم الملف هو")
                        say(txt.split('/')[-1].split('.')[0])
                        say_arabic("للقراءة قل نعم")
                        #read answer from user
                        read=voice_command_arabic()
                        if "نعم" in read:
                            f=open(txt,'r')
                            #read text file
                            say(f.read())
                        else:
                            continue
            #         print(audio)
            #
                    else:
                            say("file name is"+txt.split('/')[-1].split('.')[0])
                            say("say ok to read")
                            #read answer from user
                            read=voice_command_english()
                            if "ok" in read:
                              f=open(txt,'r')
                              #read text file
                              say(f.read())
                            else:
                                continue
                flag_end=1
                continue
            #checks if file is doc
            if "word"  in text:
                doc_files=files["doc"]
                for doc in doc_files:
                    if flag_arabic:
                        say_arabic("اسم الملف هو")
                        say(doc.split('/')[-1].split('.')[0])
                        say_arabic("للقراءة قل نعم")
                        #read answer from user
                        read=voice_command_arabic()
                        if "نعم" in read:
                                txt=re.sub(' +', ' ', docx2txt.process(doc))
                        #         txt=txt.replace('\n',"")
                        #         Tts(txt)
                                txt=txt.split()
                                txt=' '.join(txt)
                        #         print(txt)
                                say(txt)

                        else:
                            continue
            #         print(audio)
            #
                    else:
                            say("file name is"+doc.split('/')[-1].split('.')[0])
                            say("say ok to read")
                            #read answer from user
                            read=voice_command_english()
                            if "ok" in read:
                                          #         print(txt)
                                txt=re.sub(' +', ' ', docx2txt.process(doc))
                        #         txt=txt.replace('\n',"")
                        #         Tts(txt)
                                txt=txt.split()
                                txt=' '.join(txt)
                        #         print(txt)
                                #read text file
                                say(txt)
                            else:
                                continue

                flag_end=1
                continue
        



