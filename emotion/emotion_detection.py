from tensorflow.keras import Sequential
from tensorflow.keras.models import load_model
import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
from picamera.array import PiRGBArray
from picamera import PiCamera

# capture image
def capture():
    camera = PiCamera()

    # rotate 90 degrees clockwise due to our glasses design
    camera.rotation = 90
    camera.resolution = (1920, 1080)
    camera.start_preview()
    camera.capture('/home/pi/Desktop/graduation/src/emotion.jpg')
    camera.stop_preview()


# This function is for designing the overlay text on the predicted image boxes.
def text_on_detected_boxes(text, text_x, text_y, image, font_scale=1,

                           font=cv2.FONT_HERSHEY_SIMPLEX,

                           FONT_COLOR=(0, 0, 0),

                           FONT_THICKNESS=2,

                           rectangle_bgr=(0, 255, 0)):

    # get the width and height of the text box

    (text_width, text_height) = cv2.getTextSize(text, font, fontScale=font_scale, thickness=2)[0]

    # Set the Coordinates of the boxes

    box_coords = ((text_x - 10, text_y + 4), (text_x + text_width + 10, text_y - text_height - 5))

    # Draw the detected boxes and labels

    cv2.rectangle(image, box_coords[0], box_coords[1], rectangle_bgr, cv2.FILLED)

    cv2.putText(image, text, (text_x, text_y), font, fontScale=font_scale, color=FONT_COLOR, thickness=FONT_THICKNESS)


# Detection of the emotions on an image:

def face_detector_image(img, face_classifier):
    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Convert the image into GrayScale image

    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if faces is ():
        return (0, 0, 0, 0), np.zeros((48, 48), np.uint8), img

    allfaces = []

    rects = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roi_gray = gray[y:y + h, x:x + w]

        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        allfaces.append(roi_gray)

        rects.append((x, w, y, h))

    return rects, allfaces, img
