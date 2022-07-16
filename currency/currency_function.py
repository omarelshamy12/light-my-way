import os
import cv2
import numpy as np
import sys
import glob
import importlib.util


def currency_detection(path):
    MODEL_NAME = '/home/pi/yolov4 raspberry/TFLite_Yolov4_and_SSD'
    # TFLite model path of our trained model
    GRAPH_NAME = 'detect.tflite'
    # labels path
    LABELMAP_NAME = 'labelmap.txt'
    #minimum confidence value to filter weak detections
    min_conf_threshold = 0.2
    #path to input image
    IM_NAME = path

    # Import TensorFlow libraries
    # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow

    pkg = importlib.util.find_spec('tflite_runtime')
    if pkg:
        from tflite_runtime.interpreter import Interpreter

    else:
        from tensorflow.lite.python.interpreter import Interpreter

    # Get path to current working directory
    CWD_PATH = os.getcwd()

    # Path to .tflite file, which contains the model that is used for object detection
    PATH_TO_CKPT = os.path.join(CWD_PATH, MODEL_NAME, GRAPH_NAME)

    # Path to label map file
    PATH_TO_LABELS = os.path.join(CWD_PATH, MODEL_NAME, LABELMAP_NAME)

    # Load the label map
    with open(PATH_TO_LABELS, 'r') as f:
        labels = [line.strip() for line in f.readlines()]

    # Have to do a weird fix for label map if using the COCO "starter model" from
    # https://www.tensorflow.org/lite/models/object_detection/overview
    # First label is '???', which has to be removed.
    if labels[0] == '???':
        del (labels[0])

    # Load the Tensorflow Lite model and allocate tensors.
    interpreter = Interpreter(model_path=PATH_TO_CKPT)
    interpreter.allocate_tensors()

    # Get model details
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    size = input_details[0]['shape'][1]
    #color for the six classes
    colors = [(0, 255, 0), (0, 0, 255), (255, 0, 0), (255, 128, 0), (0, 128, 255), (128, 0, 255)]

    # Loop over every image and perform detection
    image = cv2.imread(IM_NAME)
    #read image into rgb format instead of bgr
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #get original image height and width
    imH, imW, _ = image.shape
    #resize image to match the size of the model input
    image_resized = cv2.resize(image_rgb, (size, size))
    #normalize pixel values to values between [0,1]
    image_normalized = image_resized / 255.
    #add a dimension to the image (batch, height, width, channels)
    input_data = np.expand_dims(image_normalized, axis=0)
    #convert input data to a numpy array of type float32 as rasberry pi is not able to process float64
    input_data = np.asarray(input_data).astype(np.float32)
    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Retrieve detection results
    classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class index of detected objects
    l = []
    #loop over all detected objects
    #classes is a list of class indices corresponding to the detected objects where each element in the list is an array of class indices for each detected object
    for i in range(len(classes)):
        #argmax returns the index of the maximum value in the list 
        max_index = np.argmax(classes[i])
        #get the confidence of the object detected
        max_value = classes[i][max_index]
        #if the confidence is greater than the minimum confidence threshold
        if (max_value > min_conf_threshold) and (max_value <= 1.0):
            #get the bounding box of the object detected
            col = colors[max_index % 6]
            #get the name of the object detected from the label map
            object_name = labels[max_index]
            label = '%s: %d%%' % (object_name, int(classes[i][max_index] * 100))  # Example: 'person: 72%'
            l.append(label)
    #lists for names and confidence values of the detected objects
    pred_name = []
    pred_percent = []
    #loop over all final detections
    for c in l:
        #split the label into name and confidence value
        name = c.split(": ")[0]
        percent = int(c.split(": ")[1][:-1])
        #append the name and confidence value to the lists
        pred_name.append(name)
        pred_percent.append(percent)
    #get the name of the object with the highest confidence value in the whole image as we decided to return only one object as the blind will hold only one object at a time
    max_value = max(pred_percent)
    max_index = pred_percent.index(max_value)
    cv2.destroyAllWindows()
    #return the name of the object with the highest confidence value
    return pred_name[max_index]


