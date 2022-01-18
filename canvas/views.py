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
    if request.is_ajax and request.method == "POST":
        imgB64 = request.POST['imageBase64']
        imgData = re.search(r'base64,(.*)', imgB64).group(1)
        imgPIL = Image.open(io.BytesIO(base64.b64decode(imgData)))
        imgArray = np.array(imgPIL.convert('L'))
        print(imgArray.shape)
        print(imgArray.dtype)

        HOST, PORT = socket.gethostname(), 1234

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(bytearray(imgArray))

    return render(request, "main.html", {})