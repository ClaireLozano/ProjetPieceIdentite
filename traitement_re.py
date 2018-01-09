import re
import os
import sys

# Create dictionnary
dictionnaryCE = {}
dictionnaryID = {}
dictionnaryPASS = {}

pattern = re.compile("carte")
folderName = sys.argv[1]
filesList = os.listdir(folderName)

# All the file 
for filename in filesList:

	# Analyse if document is "carte etudiante"
	if filename.endswith("CE.txt"):
		if filename[:-6] not in dictionnaryCE:
			dictionnaryCE[filename[:-6]] = 0
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as file:
			valueCE = dictionnaryCE.get(filename[:-6])
			currentText = file.read()
			if re.search(r'[0-9]{10}', currentText):
				valueCE += 0.1
				dictionnaryCE[filename[:-6]] = valueCE
			if re.search(r'[0-9]{6}', currentText):
				valueCE += 0.1
				dictionnaryCE[filename[:-6]] = valueCE
			if re.search(r'(IilL|)?NE', currentText):
				valueCE += 0.4
				dictionnaryCE[filename[:-6]] = valueCE
			if re.search(r'tudiant', currentText):
				valueCE += 0.4
				dictionnaryCE[filename[:-6]] = valueCE

	# Analyse if document is "passeport" or "carte d'identite"
	elif filename.endswith("TOP.txt"):
		if filename[:-7] not in dictionnaryID:
			dictionnaryID[filename[:-7]] = 0
		if filename[:-7] not in dictionnaryPASS:
			dictionnaryPASS[filename[:-7]] = 0
		currentFile = os.path.join(folderName,filename)
		with open(currentFile, 'r') as file:
			valuePASS = dictionnaryPASS[filename[:-7]]
			valueID = dictionnaryID[filename[:-7]]
			currentText = file.read()
			if re.search(r'passeport', currentText):
				valuePASS += 0.5
				dictionnaryPASS[filename[:-7]] = valuePASS
			if re.search(r'publique francaise', currentText):
				valueID += 0.2
				dictionnaryID[filename[:-7]] = valueID
				valuePASS += 0.2
				dictionnaryPASS[filename[:-7]] = valuePASS
			if re.search(r'Carte', currentText):
				valueID += 0.2
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'Nationnale', currentText):
				valueID += 0.3
				dictionnaryID[filename[:-7]] = valueID
			if re.search(r'Identit', currentText):
				valueID += 0.4
				dictionnaryID[filename[:-7]] = valueID
		

# Print result
print ""
print ""
print "les cartes etudiantes sont :"
for CE in dictionnaryCE:
	if dictionnaryCE[CE] > 0.75:
		print CE + " a : " + str(dictionnaryCE[CE])

print ""
print "les cartes d'identite sont :"
for ID in dictionnaryID:
	if dictionnaryID[ID] > 0.75:
		print ID + " a : " + str(dictionnaryID[ID])

print ""
print "les passeports sont :"
for PASS in dictionnaryPASS:
	if dictionnaryPASS[PASS] > 0.75:
		print PASS + " a : " + str(dictionnaryPASS[PASS])
print ""
print ""







# python traitement_re.py Images/outputFolder/