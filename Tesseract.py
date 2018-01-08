import os
import sys

outputFolder = 'Images/outputFolder/'
for file in os.listdir("Images/Base"):
    if file.endswith(".jpg"):
        img = os.path.join("Images/Base", file)
        os.system('tesseract ' + img + ' '+ outputFolder + file)