import cv2
import numpy as np

# Retourne une image binariser - methode utilisee : Otsu
def getNBImage(img):
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img = img.astype(np.uint8)
	ret, thresh = cv2.threshold(img,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	NBimage = np.invert(thresh)
	return NBimage


img = cv2.imread('Images/Base/CE3.jpg')
kernel = np.ones((5,5), np.uint8)

# img_erosion = cv2.erode(img, kernel, iterations=1)
img_dilation = cv2.dilate(img, kernel, iterations=1)
img_erosion = cv2.erode(img_dilation, kernel, iterations=1)


cv2.imshow('Input', img)
cv2.imshow('Erosion', img_erosion)
# cv2.imshow('Dilation', img_dilation)
cv2.waitKey(0)

# import cv2
# import numpy as np
# import os
# import sys
# from PIL import Image
# from scipy import misc
# import matplotlib.pyplot as plt
# from scipy.ndimage import gaussian_filter


# imageFile = './Images/Base/autres2.jpg'


# # *** Old method  ***
# filterMatrics = np.ones((3,3), np.float32)/9

# img = Image.open('Images/Base/CE2.jpg').convert('L')
# img.save('reyscale.jpg')


# # Pre-processing
# originalImg = cv2.imread(imageFile)
# afterImg = cv2.filter2D(img, -1, filterMatrics)
# afterImg.save('outputImg.jpg')


