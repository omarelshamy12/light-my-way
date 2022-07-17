import subprocess as sp
import os
import glob

def get_files():
    #get name of the folder of usb flash drive by listing /media/pi
    #usf flash drives in raspberry pi are always in directory " /media/pi"
    dir_path = "/media/pi/"+sp.getoutput('ls /media/pi')
#     print(dir_path)

    #making lists for valid extensions
    valid_images = ['.jfif','.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm']
    valid_audio=[".m4a",".mp3", ".wav", ".au", ".ogg"]
    valid_doc=[".doc",".docx"]
    # list to store files
    txt = [] 
    music=[]
    pdf=[]
    images=[]
    doc=[]
    # Iterate on usb folder files
    for file in os.listdir(dir_path):
        # check only text files
        if file.endswith('.txt'):
            txt.append(dir_path+"/"+file)
            continue
        # check only audio files
        for i in valid_audio:
            if file.endswith(i):
                music.append(dir_path+"/"+file)
                continue
        # check only pdf files
        if file.endswith('.pdf'):
            pdf.append(dir_path+"/"+file)
            continue
        # check only image files
        for i in valid_images:
            if file.endswith(i):
                images.append(dir_path+"/"+file)
                continue
        # check only doc files
        for i in valid_doc:
            if file.endswith(i):
                doc.append(dir_path+"/"+file)
                continue
    #making a dictionary for all reulting files to be more accessible
    files={"txt":txt,"image":images,"pdf":pdf,"music":music,"doc":doc}
    #returning dictionary
    return files

