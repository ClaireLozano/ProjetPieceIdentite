import cv2
import numpy as np
import os
import sys


imageFile = 'Images/Base/CE2.jpeg'

print("Execute Gaussian Filtering on folder: ")

# filterMatrics = np.ones((5,5), np.float32)/25
# images = util.getFilesFromDirectory(args[1])
# nbTotalImages = len(images)

# # For each images 
# for idx, img in enumerate(images):
# 	# Show info
# 	print("Image", idx+1, "/", nbTotalImages)
	
# 	# Get output image target path + img infos (name + ext)
# 	targetPath = util.getDatabaseOutputPath(img, 'gaussian-filtering')
# 	imgPath, imgExt = os.path.splitext(img)
# 	imgName = imgPath.split("/")[-1]

# 	# Pre-processing
# 	originalImg = cv2.imread(img)
# 	afterImg = cv2.filter2D(originalImg, -1, filterMatrics)
# 	util.writeFile(afterImg, imgName, targetPath, imgExt)


