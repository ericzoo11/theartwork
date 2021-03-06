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
import sys

def getContours(image):
    images = np.array(image)
    images = cv2.resize(images, (2550, 3300), cv2.INTER_CUBIC)
    gray_image = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)
    ret, bw_image =  cv2.threshold(gray_image, 50, 255, cv2.THRESH_BINARY)
    contours, heierarchy = cv2.findContours(bw_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoured_image = bw_image
    output = open("test.txt", 'w')
    count = 0
    for contour in contours[1:]:
        for con in contour:
            np.savetxt(output, con,fmt='%d')
        output.write('----------\n')
        count+=1
    output.write('eeeeeeeeee\n')
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
        paddedImg = ImageOps.expand(imgPIL, border = 10, fill=(255,255,255))
        flippedImg = paddedImg.transpose(Image.FLIP_LEFT_RIGHT)
        imgArray = np.array(imgPIL.convert('L'))
        getContours(flippedImg)
        width = "2550"
        height = "3300"
        #dims = np.array([width, height]).astype('uint16')
        
        print(imgArray)
        print(width, height, imgArray.dtype)        
        
        #HOST, PORT = socket.gethostname(), 1234        ##Test Port
        HOST, PORT = '192.168.50.123', 13000
        newline = "\n"
        file = open("test.txt", "r")
        data = file.read()
        extrema = imgPIL.convert("L").getextrema()
        if(not extrema[0] == 255):
            updateCurrent(imgPIL.copy())
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send(width.encode("utf-8"))
            s.send(newline.encode("utf-8"))
            s.send(height.encode("utf-8"))
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
