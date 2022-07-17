import speech_recognition as sr
from text_to_speech.tts import *

def voice_command_arabic():
    #ask user to speak
    say_arabic("تكلم")
    #init recognizer
    r = sr.Recognizer()
    #listen to source
    with sr.Microphone() as source:
        audio = r.listen(source)
        #in case of error will not change
        text="فشل"
        #try to recognize
        try:
                
            text = r.recognize_google(audio,language="ar-EG")
            #ask user to stop 
            say_arabic("توقف")
             
        except:
            #ask user to try again
            say_arabic("حاول مجددا من فضلك")
            pass
        #print recognized text
        print(text)
        #return recognized text
        return text     
def voice_command_english():
    #ask user to speak
    say("start")
    #init recognizer
    r = sr.Recognizer()
    #listen to source
    with sr.Microphone() as source:
        
        audio = r.listen(source)
        #in case of error will not change
        text="error"
        #try to recognize
        try:
              
            text = r.recognize_google(audio)
            #ask user to stop
            say("end")
             
        except:
            #ask user to try again
            say("try again please")
            pass
        #print recognized text
        print(text)
        return text
