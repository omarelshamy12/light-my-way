import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
thres = 0.45 # Threshold to detect object


def getObjects(img, thres, nms, draw=True, objects=[],flag_arabic=0):
    classNames = []
    if flag_arabic:
        #arabic labels
        classFile="/home/pi/Desktop/graduation/src/Object_Detection/coco_arabic.names"
        with open(classFile,"rt") as f:
            classNames = f.read().rstrip("\n").split("\n")
    else:
        #english labels
        classFile = "/home/pi/Desktop/Object_Detection_Files/coco.names"
        with open(classFile,"rt") as f:
            classNames = f.read().rstrip("\n").split("\n")
    
#     print(classNames)
    # Load the model
    configPath = "/home/pi/Desktop/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
    weightsPath = "/home/pi/Desktop/Object_Detection_Files/frozen_inference_graph.pb"
    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    # Set the input parameters to the network
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)
    # Run the network
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    #print(classIds,bbox)
    # Draw the bounding boxes and labels of the detected objects
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    objs=[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                objs.append(className)
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo,objs

# print(process_image(flag_arabic=0))
