from django.shortcuts import render
from pyzbar.pyzbar import decode
import cv2


# Create your views here.

def scan_qrcode(request):
    cam = cv2.VideoCapture(0)
    cam.set(5, 640)
    cam.set(5, 480)

    camera = True
    while camera:
        success, frame = cam.read()

        for i in decode(frame):
            print(i.type)
            print(i.data.decode('utf-8'))

            cv2.imshow('QR Code Scanner', frame)
            cv2.waitKey(3)

        cam.release()

    return render(request, 'scanner.html')
