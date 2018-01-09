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
<<<<<<< HEAD
			if re.search(r'INE', currentText) and re.search(r'tudiant', currentText):
				print(currentFile +" est une carte etudiante")
=======
			pourcent = 0
			if re.search(r'[0-9]{10}', currentText):
				pourcent += 0.1
			if re.search(r'[0-9]{6}', currentText):
				pourcent += 0.1
			if re.search(r'(IilL|)?NE', currentText):
				pourcent += 0.4
			if re.search(r'tudiant', currentText):
				pourcent += 0.4
			if pourcent > 0.75:	
				print(currentFile + " est une carte etudiante avec : " + str(pourcent))

	# Analyse if document is "passeport" or "carte d'identite"
	elif filename.endswith("TOP.txt") or filename.endswith("BOT.txt"):
		print(os.path.join(folderName,filename))
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as filename:
			currentText = filename.read()
			pourcentPasseport = 0
			pourcentID = 0
			if re.search(r'passeport', currentText):
				pourcentPasseport += 0.5
			if re.search(r'publique francaise', currentText):
				pourcentPasseport += 0.2
				pourcentID += 0.2
			if re.search(r'Carte', currentText):
				pourcentID += 0.2
			if re.search(r'Nationnale', currentText):
				pourcentID += 0.3
			if re.search(r'Identit', currentText):
				pourcentID += 0.4
			print currentText
			if pourcentPasseport > 0.75:	
				print(currentFile + " est un passeport : " + str(pourcentPasseport))
			if pourcentID > 0.75:	
				print(currentFile + " est une carte d'identite : " + str(pourcentID))
>>>>>>> da56debc220c5d0a7771abefda198de9b136e18b
		
# python traitement_re.py Images/outputFolder/