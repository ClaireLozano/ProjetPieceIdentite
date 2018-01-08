import re
import os
import sys

pattern = re.compile("carte")

folderName = sys.argv[1]
filesList = os.listdir(folderName)

# All the file 

for filename in filesList:
	# Analyse if document is "carte etudiante"
	if filename.endswith("CE.txt"):
		print(os.path.join(folderName,filename))
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as filename:
			currentText = filename.read()
			print currentText
			if re.search(r'INE', currentText) and re.search(r'tudiant', currentText):
				print(currentFile +" est une carte etudiante")
		
# python traitement_re.py Images/outputFolder/