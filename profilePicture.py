#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
from PIL import Image
import numpy as np
import cv2

def crop_image(img):
	im = Image.open(img)
	width, height = im.size

	# crop right part
	startx = width*0.70
	starty = 0
	endx = width
	endy = height
	cropRightPicture = im.crop((int(startx), int(starty), int(endx), int(endy)))

	# crop left part
	startx = 0
	starty = 0
	endx = width*0.30
	endy = height
	cropLeftPicture = im.crop((int(startx), int(starty), int(endx), int(endy)))

	cropRightPicture.save('cropRightPicture.bmp')
	cropLeftPicture.save('cropLeftPicture.bmp')

	# return the 3 croped images
	return cropLeftPicture, cropRightPicture

def get_faces(folder_base):
	for file in os.listdir(folder_base):
		if file.endswith(".jpg"):
			img = os.path.join(folder_base, file)

			# get croped image  
			cropLeftPicture, cropRightPicture = crop_image(folder_base + "/" + file)

			# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
			face_cascade = cv2.CascadeClassifier('opencv/data/haarcascades/haarcascade_frontalface_default.xml')
			eye_cascade = cv2.CascadeClassifier('opencv/data/haarcascades/haarcascade_eye.xml')

			imgRight = cv2.imread('cropRightPicture.bmp')
			imgLeft = cv2.imread('cropLeftPicture.bmp')
			grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)
			grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)

			print face_cascade
			faces = face_cascade.detectMultiScale(grayRight, 1.3, 5)
			print('Faces found: ', len(faces))

			for (x,y,w,h) in faces:
			    img = cv2.rectangle(imgRight,(x,y),(x+w,y+h),(255,0,0),2)
			    roi_gray = grayRight[y:y+h, x:x+w]
			    roi_color = img[y:y+h, x:x+w]
			    eyes = eye_cascade.detectMultiScale(roi_gray)
			    for (ex,ey,ew,eh) in eyes:
			        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

			cv2.imshow('img',imgRight)
			cv2.waitKey(0)
			cv2.destroyAllWindows()

			faces = face_cascade.detectMultiScale(grayLeft, 1.3, 5)
			for (x,y,w,h) in faces:
			    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			    roi_gray = grayLeft[y:y+h, x:x+w]
			    roi_color = img[y:y+h, x:x+w]
			    eyes = eye_cascade.detectMultiScale(roi_gray)
			    for (ex,ey,ew,eh) in eyes:
			        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

			cv2.imshow('img',img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()


get_faces('Images/VeriteTerrain')
# get_faces("Images/Base")














