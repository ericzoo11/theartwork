from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import base64
import re
from PIL import Image
import io
import socket
import sys

# Create your views here.
def mainPage(request):
    return render(request, "main.html", {})

@csrf_exempt
def sendImage(request):
    if request.method == "POST":
        imgB64 = request.POST['imageBase64']
        imgData = re.search(r'base64,(.*)', imgB64).group(1)
        imgPIL = Image.open(io.BytesIO(base64.b64decode(imgData)))
        imgArray = np.array(imgPIL.convert('L'))
        
        width = imgArray.shape[1]
        height = imgArray.shape[0]
        dims = np.array([width, height]).astype('uint16')

        print(imgArray)
        print(width, height, imgArray.dtype)        
        
        #HOST, PORT = socket.gethostname(), 1234        ##Test Port
        HOST, PORT = '192.168.0.123', 13000

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(dims.astype(np.int).tobytes(order='C'))
        s.send(imgArray.astype(np.int).tobytes(order='C'))

    return render(request, "main.html", {})
