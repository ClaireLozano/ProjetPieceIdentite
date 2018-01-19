#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import scipy.misc
import cv2

from PIL import Image

# Retourne une image binariser 
def getNBImage(img):

	# Transformation d'une image couleur en une image en noir et blanc
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = img.astype(numpy.uint8)

	# Réduction du bruit
	dst = cv2.fastNlMeansDenoising(img,None, 8, 7, 21)

	# Binarasation de l'image image 
	# Méthode utilisée : otsu
	ret, thresh = cv2.threshold(dst,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	return numpy.invert(thresh)


# Découpe une image et renvoie trois morceaux de l'image placée en paramêtre
def crop_image(im):
	width, height = im.size

	# Partie en bas à gauche au niveau des informations de la carte étudiante
	startx = 0
	starty = height*0.75
	endx = width*0.5
	endy = height
	cropImageCE = getNBImage(numpy.asarray(im.crop((int(startx), int(starty), int(endx), int(endy)))))

	# Partie du haut qui permettra de définir c'est c'est une carte d'identité ou un passeport
	startx = 0
	starty = 0
	endx = width
	endy = height*0.30
	cropImageTOP = getNBImage(numpy.asarray(im.crop((int(startx), int(starty), int(endx), int(endy)))))
	
	# Partie du bas qui permettra de définir c'est c'est une carte d'identité ou un passeport
	startx = 0
	starty = height*0.75
	endx = width
	endy = height
	cropImageBOT = getNBImage(numpy.asarray(im.crop((int(startx), int(starty), int(endx), int(endy)))))

	return cropImageCE, cropImageTOP, cropImageBOT


# Fonction de récupération et sauvegarde du texte retrouvé par l'ocr (tesseract)
def get_text(folder, folder_base):
	outputFolder = folder
	for file in os.listdir(folder_base):
		if file.endswith(".jpg"):
			img = os.path.join(folder_base, file)
			im = Image.open(folder_base + "/" + file)
			
			# Découper l'image en trois morceaux  
			cropImageCE, cropImageTOP, cropImageBOT = crop_image(im)

			# Sauvegarder et ouverture des images
			scipy.misc.imsave('cropCE.jpg', cropImageCE)
			scipy.misc.imsave('cropTOP.jpg', cropImageTOP)
			scipy.misc.imsave('cropBOT.jpg', cropImageBOT)
			imgCE = os.path.join('cropCE.jpg')
			imgTOP = os.path.join('cropTOP.jpg')
			imgBOT = os.path.join('cropBOT.jpg')

			# Passage de l'ocr tesseract sur les images
			os.system('tesseract ' + imgCE + ' ' + outputFolder + file + "CE")
			os.system('tesseract ' + imgTOP + ' ' + outputFolder + file + "TOP")
			os.system('tesseract ' + imgBOT + ' ' + outputFolder + file + "BOT")

get_text('Images/outputFolder/', "Images/Base")

# Suppression de fichier inutile
os.remove("cropCE.jpg")
os.remove("cropTOP.jpg")
os.remove("cropBOT.jpg")
