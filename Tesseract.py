import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
from PIL import Image

def crop_image(img):
	im = Image.open(img)
	width, height = im.size

	# crop 3 part of images
	startx = 0
	starty = height*0.75
	endx = width*0.5
	endy = height
	cropImageCE = im.crop((int(startx), int(starty), int(endx), int(endy)))

	startx = 0
	starty = 0
	endx = width
	endy = height*0.20
	cropImageTOP = im.crop((int(startx), int(starty), int(endx), int(endy)))

	startx = 0
	starty = height*0.75
	endx = width
	endy = height
	cropImageBOT = im.crop((int(startx), int(starty), int(endx), int(endy)))

	# return the 3 croped images
	return cropImageCE, cropImageTOP, cropImageBOT

def get_text(folder, folder_base):
	outputFolder = folder
	for file in os.listdir(folder_base):
		if file.endswith(".jpg"):
			img = os.path.join(folder_base, file)

			# get croped image  
			cropImageCE, cropImageTOP, cropImageBOT = crop_image(folder_base + "/" + file)

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














