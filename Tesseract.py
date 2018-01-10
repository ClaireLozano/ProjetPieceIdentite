#!/usr/bin/python
# -*- coding: latin-1 -*-

import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy
import scipy.misc
from PIL import Image
import cv2

# Retourne une image binariser 
def getNBImage(img):

	# gray
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = img.astype(numpy.uint8)

	# denoised
	dst = cv2.fastNlMeansDenoising(img,None, 8, 7, 21)

	# egalized histogram
	# equ = cv2.equalizeHist(dst)
	# res = numpy.hstack((dst,equ)) #stacking images side-by-side

	# binarasation image : otsu
	ret, thresh = cv2.threshold(dst,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	NBimage = numpy.invert(thresh)
	return NBimage

def crop_image(im):
	width, height = im.size

	# crop 3 part of images
	startx = 0
	starty = height*0.75
	endx = width*0.5
	endy = height
	cropImageCE = im.crop((int(startx), int(starty), int(endx), int(endy)))
	a = numpy.asarray(cropImageCE)
	cropImageCE = getNBImage(a)

	startx = 0
	starty = 0
	endx = width
	endy = height*0.30
	cropImageTOP = im.crop((int(startx), int(starty), int(endx), int(endy)))
	a = numpy.asarray(cropImageTOP)
	cropImageTOP = getNBImage(a)
	
	startx = 0
	starty = height*0.75
	endx = width
	endy = height
	cropImageBOT = im.crop((int(startx), int(starty), int(endx), int(endy)))
	a = numpy.asarray(cropImageBOT)
	cropImageBOT = getNBImage(a)

	# return the 3 croped images
	return cropImageCE, cropImageTOP, cropImageBOT

def get_text(folder, folder_base):
	outputFolder = folder
	for file in os.listdir(folder_base):
		if file.endswith(".jpg"):
			img = os.path.join(folder_base, file)
			im = Image.open(folder_base + "/" + file)
			
			# get croped image  
			cropImageCE, cropImageTOP, cropImageBOT = crop_image(im)

			# save and open croped image
			scipy.misc.imsave('cropCE.jpg', cropImageCE)
			scipy.misc.imsave('cropTOP.jpg', cropImageTOP)
			scipy.misc.imsave('cropBOT.jpg', cropImageBOT)

			imgCE = os.path.join('cropCE.jpg')
			imgTOP = os.path.join('cropTOP.jpg')
			imgBOT = os.path.join('cropBOT.jpg')

			# use tesseract
			os.system('tesseract ' + imgCE + ' ' + outputFolder + file + "CE")
			os.system('tesseract ' + imgTOP + ' ' + outputFolder + file + "TOP")
			os.system('tesseract ' + imgBOT + ' ' + outputFolder + file + "BOT")

get_text('Images/outputFolder/', "Images/Base")
