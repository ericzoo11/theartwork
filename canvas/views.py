from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
import numpy as np
import base64
import re
from PIL import Image, ImageOps
import io
import socket
import sys
import numpy as np
import cv2
import math

def getContours(image):
    images = np.array(image)
    canny_image = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    edges_canny =  cv2.Canny(canny_image, 7, 51)
    contours, heierarchy = cv2.findContours(edges_canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoured_image = canny_image
    #print(contours[5])
    output = open("test.txt", 'w')
    count = 0
    for contour in contours:
        for con in contour:
            np.savetxt(output, con,fmt='%d')
        output.write('----------\n')
        count+=1
    output.close()

def updateCurrent(image):
    path = static("images/current.png")
    
    currentImage = Image.open(path[1:]).convert('RGB')
    width, height = currentImage.size

    newImageResize = image.resize((width, height), Image.LANCZOS).convert('RGB')
    newImageResize = Image.composite(currentImage, newImageResize, newImageResize.convert('L'))
    
    newImageResize.save(path[1:])
    
# Create your views here.
def mainPage(request):
    #resetCurrent()
    return render(request, "main.html", {})

@csrf_exempt
def sendImage(request):
    if request.method == "POST":
        imgB64 = request.POST['imageBase64']
        imgData = re.search(r'base64,(.*)', imgB64).group(1)
        imgPIL = Image.open(io.BytesIO(base64.b64decode(imgData)))
        imgArray = np.array(imgPIL.convert('L'))
        getContours(imgPIL)
        updateCurrent(imgPIL.copy())
        width = imgArray.shape[1]
        height = imgArray.shape[0]
        #dims = np.array([width, height]).astype('uint16')

        print(imgArray)
        print(width, height, imgArray.dtype)        
        
        HOST, PORT = socket.gethostname(), 1234        ##Test Port
        #HOST, PORT = '192.168.0.123', 13000
        newline = "\n"
        file = open("test.txt", "r")
        data = file.read()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(str(width).encode("utf-8"))
        s.send(newline.encode("utf-8"))
        s.send(str(height).encode("utf-8"))
        s.send(newline.encode("utf-8"))
        s.send(data.encode("utf-8"))

        return render(request, "main.html", {})

@csrf_exempt
def resetCurrent(request):
    if request.method == "POST":
        current = static("images/current.png")
        reset = static("images/Blank.png")
            
        blankImage = Image.open(reset[1:]).convert('RGB')
            
        blankImage.save(current[1:])
        return render(request, "main.html", {})