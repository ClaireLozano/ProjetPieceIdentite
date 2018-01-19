#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import re
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
import numpy as np
import cv2
import pprint
import operator

from PIL import Image


# Découpage de l'image de façon à récupérer les photos d'identités
def crop_image(img):
	im = Image.open(img)
	width, height = im.size

	# Découpage de la zone de la photo d'identité sur les cartes étudiantes
	startx = width*0.70
	starty = 0
	endx = width
	endy = height*0.5
	cropRightPicture = im.crop((int(startx), int(starty), int(endx), int(endy)))

	# Découpage de la zone de la photo d'identité sur les passeports et les cartes d'identités
	startx = 0
	starty = 0
	endx = width*0.30
	endy = height
	cropLeftPicture = im.crop((int(startx), int(starty), int(endx), int(endy)))

	# Sauvegarde des photos
	cropRightPicture.save('cropRightPicture.bmp')
	cropLeftPicture.save('cropLeftPicture.bmp')

	# Retourne les deux photos
	return cropLeftPicture, cropRightPicture


# Analyse des photos et retourne l'emplacement du visage trouvé
def get_faces(folderName, filename):
	# Ouverture de la pièce d'identité
	img = os.path.join(folderName, filename)

	# Découpage de l'image
	cropLeftPicture, cropRightPicture = crop_image(folderName + "/" + filename)

	# Ouverture des image découper et les passer en niveau de gris
	face_cascade = cv2.CascadeClassifier('opencv/data/haarcascades/haarcascade_frontalface_default.xml')
	imgRight = cv2.imread('cropRightPicture.bmp')
	imgLeft = cv2.imread('cropLeftPicture.bmp')
	grayRight = cv2.cvtColor(imgRight, cv2.COLOR_BGR2GRAY)
	grayLeft = cv2.cvtColor(imgLeft, cv2.COLOR_BGR2GRAY)

	# Trouver les visage 
	facesRight = face_cascade.detectMultiScale(grayRight, 1.3, 5)
	facesLeft = face_cascade.detectMultiScale(grayLeft, 1.3, 5)

	return facesRight, facesLeft


# Analyse les fichier texte ainsi que les photos
# Retourne trois dictionnaires
def Analyse(folderName):

	# Création du dictionnaire
	dictionnaryCE = {}
	dictionnaryID = {}
	dictionnaryPASS = {}

	pattern = re.compile("carte")
	filesList = os.listdir(folderName)

	# Analyse du texte
	for filename in filesList:

		# Si la zone découper et la zone de carte d'étudiant
		# On regarde à l'aide d'expression régulière si on retrouve certain mots clés
		if filename.endswith("CE.txt"):
			if filename[:-6] not in dictionnaryCE:
				dictionnaryCE[filename[:-6]] = {'pourcentage': 0, 'liste': []} 
				dictionnaryPASS[filename[:-6]] = {'pourcentage': 0, 'liste': []} 
				dictionnaryID[filename[:-6]] = {'pourcentage': 0, 'liste': []} 
			currentFile = os.path.join(folderName,filename)
			with open(currentFile, 'r') as file:
				valueCE = dictionnaryCE[filename[:-6]]["pourcentage"]
				valueID = dictionnaryID[filename[:-6]]["pourcentage"]
				valuePASS = dictionnaryPASS[filename[:-6]]["pourcentage"]
				listCE = dictionnaryCE[filename[:-6]]["liste"]
				currentText = file.read()
				if re.search(r'[il|]ne', currentText, flags=re.IGNORECASE):
					valueCE += 0.2
					valuePASS -= 0.2
					valueID -= 0.2
					listCE.append('INE')
				if re.search(r'[eé]tud[il|]ant', currentText, flags=re.IGNORECASE):
					valueCE += 0.4
					valuePASS -= 0.5
					valueID -= 0.5
					listCE.append('etudiant')
				dictionnaryCE[filename[:-6]]["pourcentage"] = valueCE
				dictionnaryID[filename[:-6]]["pourcentage"] = valueID
				dictionnaryPASS[filename[:-6]]["pourcentage"] = valuePASS
				dictionnaryCE[filename[:-6]]["liste"] = listCE
				file.close()

		# Si la zone découper et la zone de carte d'identité et passeport (partie du haut)
		# On regarde à l'aide d'expression régulière si on retrouve certain mots clés	
		elif filename.endswith("TOP.txt"):
			if filename[:-7] not in dictionnaryID:
				dictionnaryID[filename[:-7]] = {'pourcentage': 0, 'liste': []} 
			if filename[:-7] not in dictionnaryPASS:
				dictionnaryPASS[filename[:-7]] = {'pourcentage': 0, 'liste': []} 
			currentFile = os.path.join(folderName,filename)
			with open(currentFile, 'r') as file:
				valuePASS = dictionnaryPASS[filename[:-7]]["pourcentage"]
				valueID = dictionnaryID[filename[:-7]]["pourcentage"]
				listID = dictionnaryID[filename[:-7]]["liste"]
				listPASS = dictionnaryPASS[filename[:-7]]["liste"]
				currentText = file.read()
				if re.search(r'pass[e]?port', currentText, flags=re.IGNORECASE):
					valuePASS += 0.4
					valueID -= 0.4
					listPASS.append('passeport')
				if re.search(r'r[eéè]publ[il|]que fran[çc]a[il|]se', currentText, flags=re.IGNORECASE):
					valueID += 0.1
					valuePASS += 0.2
					listID.append('république française')
					listPASS.append('république française')
				if re.search(r'carte', currentText, flags=re.IGNORECASE):
					valueID += 0.2
					valuePASS -= 0.4
					listID.append('carte')
				if re.search(r'nat[il|]onnale', currentText, flags=re.IGNORECASE):
					valueID += 0.1
					listID.append('nationnal')
				if re.search(r'[il|]dent[il|]t[eé]', currentText, flags=re.IGNORECASE):
					valueID += 0.2
					valuePASS -= 0.7
					listID.append('identité')
				dictionnaryID[filename[:-7]]["pourcentage"] = valueID
				dictionnaryPASS[filename[:-7]]["pourcentage"] = valuePASS
				dictionnaryID[filename[:-7]]["liste"] = listID
				dictionnaryPASS[filename[:-7]]["liste"] = listPASS
				file.close()


		# Si la zone découper et la zone de carte d'identité et passeport (partie du bas)
		# On regarde à l'aide d'expression régulière si on retrouve certain mots clés	
		elif filename.endswith("BOT.txt"):
			if filename[:-7] not in dictionnaryID:
				dictionnaryID[filename[:-7]] = {'pourcentage': 0, 'liste': []} 
			if filename[:-7] not in dictionnaryPASS:
				dictionnaryPASS[filename[:-7]] = {'pourcentage': 0, 'liste': []} 
			currentFile = os.path.join(folderName,filename)
			with open(currentFile, 'r') as file:
				valuePASS = dictionnaryPASS[filename[:-7]]["pourcentage"]
				valueID = dictionnaryID[filename[:-7]]["pourcentage"]
				listID = dictionnaryID[filename[:-7]]["liste"]
				listPASS = dictionnaryPASS[filename[:-7]]["liste"]
				currentText = file.read()
				if re.search(r'[il|]dfra', currentText, flags=re.IGNORECASE):
					valuePASS += 0.1
					valueID += 0.1
					listID.append('idfra')
					listPASS.append('idfra')
				if re.search(r'<<<', currentText, flags=re.IGNORECASE):
					valuePASS += 0.1
					valueID += 0.1
					listID.append('<<<')
					listPASS.append('<<<')
				dictionnaryID[filename[:-7]]["pourcentage"] = valueID
				dictionnaryPASS[filename[:-7]]["pourcentage"] = valuePASS
				dictionnaryID[filename[:-7]]["liste"] = listID
				dictionnaryPASS[filename[:-7]]["liste"] = listPASS
				file.close()

	# Récupération de la liste d'image
	ImageBase = "Images/Base"
	filesList = os.listdir(ImageBase)

	# Analyse des photos d'identités
	for filename in filesList:

		facesRight, facesLeft = get_faces(ImageBase, filename)	

		if len(facesLeft) > 0:
			if filename not in dictionnaryPASS:
				dictionnaryPASS[filename] = {'pourcentage': 0, 'liste': []} 
			if filename not in dictionnaryID:
				dictionnaryID[filename] = {'pourcentage': 0, 'liste': []} 
			valuePASS = dictionnaryPASS[filename]["pourcentage"]
			valueID = dictionnaryID[filename]["pourcentage"]
			listID = dictionnaryID[filename]["liste"]
			listPASS = dictionnaryPASS[filename]["liste"]
			valueID += 0.2
			valuePASS += 0.2
			listID.append("photo")
			listPASS.append("photo")
			dictionnaryID[filename]["pourcentage"] = valueID
			dictionnaryPASS[filename]["pourcentage"] = valuePASS
			dictionnaryID[filename]["liste"] = listID
			dictionnaryPASS[filename]["liste"] = listPASS

		if len(facesRight) > 0:
			if filename not in dictionnaryCE:
				dictionnaryCE[filename] = {'pourcentage': 0, 'liste': []} 
			listCE = dictionnaryCE[filename]["liste"]
			valueCE = dictionnaryCE[filename]["pourcentage"]
			valueCE += 0.4
			listCE.append("photo CE")
			dictionnaryCE[filename]["pourcentage"] = valueCE
			dictionnaryCE[filename]["liste"] = listCE
	return dictionnaryCE, dictionnaryID, dictionnaryPASS




# ================================================

folderName = "Images/outputFolder"
dictionnaryCE, dictionnaryID, dictionnaryPASS = Analyse(folderName)

os.remove('cropRightPicture.bmp')
os.remove('cropLeftPicture.bmp')


# Affichage du résultat
print ""
print ""
print ""
print ""
print ""
print "=========================="
print "les cartes etudiantes sont :"
print "=========================="
print ""
for key, value in sorted(dictionnaryCE.iteritems(), key=operator.itemgetter(0), reverse=True):
	if value["pourcentage"] >= 0:
		print key + " a : " + str(value["pourcentage"]*100) + "%"
		print "Liste des éléments trouvés : " + str(value["liste"]) 

print ""
print ""
print "=========================="
print "les cartes d'identite sont :"
print "=========================="
print ""
for key, value in sorted(dictionnaryID.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	if value["pourcentage"] >= 0:
		print key + " a : " + str(value["pourcentage"]*100) + "%"
		print "Liste des éléments trouvés : " + str(value["liste"]) 

print ""
print ""
print "=========================="
print "les passeports sont :"
print "=========================="
print ""
for key, value in sorted(dictionnaryPASS.iteritems(), key=lambda (k,v): (v,k), reverse=True):
	if value["pourcentage"] >= 0:
		print key + " a : " + str(value["pourcentage"]*100) + "%"
		print "Liste des éléments trouvés : " + str(value["liste"]) 
print ""
print ""

