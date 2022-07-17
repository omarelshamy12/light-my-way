import requests
import json
import urllib.request
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import pdfplumber


def capture():
    # initialize the camera and grab a reference to the raw camera capture
    camera=PiCamera()
    #camera.vflip=True
    #camera.hflip=True
    #rotate 90 degrees clockwise due to our glasses design
    camera.rotation=90
    #resolution
    camera.resolution=(1920, 1080)
    #start camera
    camera.start_preview()
    #time.sleep(1)
    #capture image
    camera.capture('/home/pi/Desktop/graduation/src/ocr_arabic.jpg')
    #stop camera
    camera.stop_preview()
    


def convert_to_png(path):
    #convert to png
    im1 = Image.open(path)
    im1.save("ocr.png")

def download_file(download_url, filename):
    # Open the url
    response = urllib.request.urlopen(download_url)
    # Open our local file for writing    
    file = open(filename + ".pdf", 'wb')
    # Write to our local file
    file.write(response.read())
    # Close our file
    file.close()
    
##### LOGIN #####
def login(email,key):
    #url of login api
    url = "https://prx.sotoor.ai/api/login"
    #payload
    querystring = {"Email":email,"ApiKey":key}
    #headers
    response = requests.request("POST", url, params=querystring)
    print(response)
    #convert to json
    dic=json.loads(str(response.text))
    #get token
    bearer="Bearer "+dic["Token"]
    #url of remaining pages api
    url = "https://prx.sotoor.ai/api/get-remaining-pages"
    #headers
    headers = {
    'content-type': "application/json", 'authorization': bearer,

    }
    
    #response
    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return bearer

def proccess(path,bearer):
    #url of proccess api
    url = "https://prx.sotoor.ai/api/recognize-file"
    #payload
    payload={'input-type': 'png','Output-format':'pdf-inpainted'}
    #files
    files=[
    ('file',('filename.png',open(path,'rb'),'image/png'))
    ]
    
    #headers
    headers = {
    'authorization': bearer
    }
    
    #response
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    #convert to json
    dic=json.loads(str(response.text)[1:-1])
    #get PDF link to download
    link_of_pdf=dic["text"][0]["output_file"]
    print(link_of_pdf)
    #download PDF
    download_file(link_of_pdf,"output")
    text=''
    
    #read PDF by pdfplumber to extract text from it to be passed to tts
    with pdfplumber.open("/home/pi/Downloads/arabic_ocr.pdf") as pdf:
        pages = pdf.pages
        for i,pg in enumerate(pages):
            text += pages[i].extract_text()
    for i in range(0,pdfReader.numPages):
        # creating a page object
        pageObj = pdfReader.getPage(i)
        # extracting text from page
        text=text+pageObj.extractText()
    return text
