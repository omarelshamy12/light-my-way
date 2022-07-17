from gtts import gTTS
import os


# The text that you want to convert to audio
def say(mytext):
    # Language in which you want to convert
    language = 'en'

    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    myobj.save("audio.mp3")

    # Playing the converted file
    os.system("mpg321 audio.mp3")


def say_arabic(mytext):
    # Language in which you want to convert
    language = "ar"

    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Saving the converted audio in a mp3 file 
    myobj.save("arabic.mp3")
    # Playing the converted file
    os.system("mpg321 arabic.mp3")
