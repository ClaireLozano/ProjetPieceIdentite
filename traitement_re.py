#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import re
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
	endy = height*0.5
	cropRightPicture = im.crop((int(startx), int(starty), int(endx), int(endy)))

	# crop left part
	startx = 0
	starty = 0
	endx = width*0.30
	endy = height
	cropLeftPicture = im.crop((int(startx), int(starty), int(endx), int(endy)))

	cropRightPicture.save('cropRightPicture.bmp')
	cropLeftPicture.save('cropLeftPicture.bmp')

	# return the 2 croped profile pictures
	return cropLeftPicture, cropRightPicture


def get_faces(folderName, filename):
	# get file
	img = os.path.join(folderName, filename)

	# get croped image  
	cropLeftPicture, cropRightPicture = crop_image(folderName + "/" + filename)

	# get xml && read images && gray images
	face_cascade = cv2.CascadeClassifier('opencv/data/haarcascades/haarcascade_frontalface_default.xml')
	imgRight = cv2.imread('cropRightPicture.bmp')
	imgLeft = cv2.imread('cropLeftPicture.bmp')
	grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)
	grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)

	# get faces
	facesRight = face_cascade.detectMultiScale(grayRight, 1.3, 5)
	facesLeft = face_cascade.detectMultiScale(grayLeft, 1.3, 5)

	return facesRight, facesLeft


# Create dictionnary
dictionnaryCE = {}
dictionnaryID = {}
dictionnaryPASS = {}

pattern = re.compile("carte")
folderName = sys.argv[1]
filesList = os.listdir(folderName)

# All the file 
for filename in filesList:

	# Analyse if document is "carte etudiante"
	if filename.endswith("CE.txt"):
		if filename[:-6] not in dictionnaryCE:
			dictionnaryCE[filename[:-6]] = 0
			dictionnaryPASS[filename[:-6]] = 0
			dictionnaryID[filename[:-6]] = 0
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as file:
			valueCE = dictionnaryCE.get(filename[:-6])
			currentText = file.read()
			if re.search(r'[il|]ne', currentText, flags=re.IGNORECASE):
				valueCE += 0.4
				valuePASS -= 0.5
				valueID -= 0.5
				dictionnaryCE[filename[:-6]] = valueCE
				dictionnaryID[filename[:-6]] = valueID
				dictionnaryPASS[filename[:-6]] = valuePASS
			if re.search(r'[eé]tud[il|]ant', currentText, flags=re.IGNORECASE):
				valueCE += 0.4
				valuePASS -= 0.4
				valueID -= 0.4
				dictionnaryCE[filename[:-6]] = valueCE
				dictionnaryID[filename[:-6]] = valueID
				dictionnaryPASS[filename[:-6]] = valuePASS

	# Analyse if document is "passeport" or "carte d'identite"
	elif filename.endswith("TOP.txt"):
		if filename[:-7] not in dictionnaryID:
			dictionnaryID[filename[:-7]] = 0
		if filename[:-7] not in dictionnaryPASS:
			dictionnaryPASS[filename[:-7]] = 0
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as file:
			valuePASS = dictionnaryPASS[filename[:-7]]
			valueID = dictionnaryID[filename[:-7]]
			currentText = file.read()
			if re.search(r'passeport', currentText, flags=re.IGNORECASE):
				valuePASS += 0.7
				valueID -= 0.8
				dictionnaryPASS[filename[:-7]] = valuePASS
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'passport', currentText, flags=re.IGNORECASE):
				valuePASS += 0.7
				valueID -= 0.8
				dictionnaryPASS[filename[:-7]] = valuePASS
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'r[eéè]publ[il|]que fran[çc]a[il|]se', currentText, flags=re.IGNORECASE):
				valueID += 0.2
				valuePASS += 0.2
				dictionnaryID[filename[:-7]] = valueID
				dictionnaryPASS[filename[:-7]] = valuePASS
			if re.search(r'carte', currentText, flags=re.IGNORECASE):
				valueID += 0.2
				valuePASS -= 0.4
				dictionnaryPASS[filename[:-7]] = valuePASS
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'nat[il|]onnale', currentText, flags=re.IGNORECASE):
				valueID += 0.3
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'[il|]dent[il|]t[eé]', currentText, flags=re.IGNORECASE):
				valueID += 0.4
				valuePASS -= 0.7
				dictionnaryID[filename[:-7]] = valueID
				dictionnaryPASS[filename[:-7]] = valuePASS


	# Analyse if document is "passeport" or "carte d'identite"
	elif filename.endswith("BOT.txt"):
		if filename[:-7] not in dictionnaryID:
			dictionnaryID[filename[:-7]] = 0
		if filename[:-7] not in dictionnaryPASS:
			dictionnaryPASS[filename[:-7]] = 0
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as file:
			valuePASS = dictionnaryPASS[filename[:-7]]
			valueID = dictionnaryID[filename[:-7]]
			currentText = file.read()
			if re.search(r'[il|]dfra', currentText, flags=re.IGNORECASE):
				valuePASS += 0.2
				valueID += 0.2
				dictionnaryPASS[filename[:-7]] = valuePASS
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'<<<<<<<', currentText, flags=re.IGNORECASE):
				valuePASS += 0.2
				valueID += 0.2
				dictionnaryPASS[filename[:-7]] = valuePASS
				dictionnaryID[filename[:-7]] = valueID


ImageBase = "Images/Base"
filesList = os.listdir(ImageBase)

# All the file 
for filename in filesList:
	# get faces
	facesRight, facesLeft = get_faces(ImageBase, filename)	

	if len(facesLeft) > 0:
		if filename not in dictionnaryPASS:
			dictionnaryPASS[filename] = 0
		if filename not in dictionnaryID:
			dictionnaryID[filename] = 0
		valuePASS = dictionnaryPASS[filename]
		valueID = dictionnaryID[filename]
		valueID += 0.4
		valuePASS += 0.4
		dictionnaryID[filename] = valueID
		dictionnaryPASS[filename] = valuePASS

	if len(facesRight) > 0:
		if filename not in dictionnaryCE:
			dictionnaryCE[filename] = 0
		valueCE = dictionnaryCE[filename]
		valueCE += 0.5
		dictionnaryCE[filename] = valueCE

# Print result
print ""
print ""
print "les cartes etudiantes sont :"
for key, value in sorted(dictionnaryCE.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	if value >= 0:
		print key + " a : " + str(value*100) + "%"

print ""
print "les cartes d'identite sont :"
for key, value in sorted(dictionnaryID.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	if value >= 0:
		print key + " a : " + str(value*100) + "%"

print ""
print "les passeports sont :"
for key, value in sorted(dictionnaryPASS.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	if value >= 0:
		print key + " a : " + str(value*100) + "%"
print ""
print ""

# python traitement_re.py Images/outputFolder/
