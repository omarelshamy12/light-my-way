from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from voice import voice_command_arabic,voice_command_english
from text_to_speech.tts import *
from emotion.emotion_detection import *

def emotionImage(flag_arabic=0):

    #asking user not to move
    if flag_arabic:
        say_arabic("برجاء عدم الحركة جاري التقاط الصورة")
    else:
        say("please don't move, photo is being captured")
    #capture image
    capture()
    #read image
    img = cv2.imread('/home/pi/Desktop/graduation/src/emotion.jpg')
        if flag_arabic:
        say_arabic("انتظر قليلا جاري قراءة الصورة")
    else:
        say("please wait photo has been captured and is being processed now")
         # Load the model
    #build model
    model = Sequential()
    #load emotion classifier
    classifier = load_model('/home/pi/Desktop/graduation/src/emotion/ferjj.h5') # This model has a set of 6 classes

    # We have 6 labels for the model
    #english labels
    class_labels = {0: 'Angry', 1: 'Fear', 2: 'Happy', 3: 'Neutral', 4: 'Sad', 5: 'Surprise'}
    #arabic labels
    arabic = {'Angry':"غاضب", 'Fear':"خائف", 'Happy': "سعيد", 'Neutral':"محايد", 'Sad' : "حزين", 'Surprise':"متفاجيء"}

    # print(class_labels)
    #face detection
    face_classifier = cv2.CascadeClassifier('/home/pi/Desktop/graduation/src/emotion/Haarcascades/haarcascade_frontalface_default.xml')

    #faces in image
    rects, faces, image = face_detector_image(img,face_classifier)

    i = 0
    labels=[]
    #loop through faces
    for face in faces:
    
        roi = face.astype("float") / 255.0
       
        roi = img_to_array(roi)
    
        roi = np. expand_dims(roi, axis=0)

        # make a prediction on the ROI, then lookup the class

        preds = classifier.predict(roi)[0]

        label = class_labels[preds.argmax()]
        if flag_arabic:
            labels.append(arabic[label])
        else:
            labels.append(label)

        label_position = (rects[i][0] + int((rects[i][1] / 2)), abs(rects[i][2] - 10))

        i = + 1

        # Overlay our detected emotion on the picture

        text_on_detected_boxes(label, label_position[0],label_position[1], image)

#     cv2.imshow("Emotion Detector", image)
# 
#     cv2.waitKey(0)
# 
#     cv2.destroyAllWindows()
    #write image
    cv2.imwrite("output.jpg", image)
    #return labels
    return labels
