import re
import os
import sys

pattern = re.compile("carte")

folderName = sys.argv[1]
filesList = os.listdir(folderName)

# All the file 

for filename in filesList:
	if filename.endswith(".txt"):
		print(os.path.join(folderName,filename))
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as filename:
			currentText = filename.read()
			if re.search(r'carte d+\W+assurance maladie', currentText):
				print(currentFile +" est une carte vitale")
			if re.search(r'INE', currentText):
				print(currentFile +" est une carte etudiante")
		