import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
from PIL import Image

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


get_faces('Images/VeriteTerrain')
# get_faces("Images/Base")














