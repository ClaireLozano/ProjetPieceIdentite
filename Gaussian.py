import cv2
import numpy as np
import os
import sys
from PIL import Image
from scipy import misc
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


imageFile = './Images/Base/autres2.jpg'


# *** Old method  ***
filterMatrics = np.ones((3,3), np.float32)/9

img = Image.open('Images/Base/CE2.jpg').convert('L')
img.save('reyscale.jpg')


# Pre-processing
originalImg = cv2.imread(imageFile)
afterImg = cv2.filter2D(img, -1, filterMatrics)
afterImg.save('outputImg.jpg')


