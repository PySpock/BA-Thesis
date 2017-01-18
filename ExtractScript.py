import os
import datetime as dt


def escCharCleanup(strList):
	# Returns eine String-List ohne /n-Escape-Char, wenn der an letzer Stelle eines Elements steht
	noEscData = [entry[:-1] if entry[-1:] == '\n' else entry[:] for entry in strList]
	return noEscData

def clearHeader(strList, delimiterLine):
	# Returns Liste ohne unwichtige Header-Elemente bis einschließlich delimiter-Zeile
	noHeaderData = []
	for entry in reversed(strList):
		if entry == delimiterLine:
			break
		noHeaderData.append(entry)
	return list(reversed(noHeaderData))

def splitData(strList, splitChar):
	# Splittet die Elemente der übergebenen List am splitChar, Rückgabe von Key & Value als separate Liste
	keyList = []
	valList = []
	for element in strList:
		keyList.append(element.split(splitChar)[0])
		valList.append(float(element.split(splitChar)[1]))
	return keyList, valList

def getint(name):
	# Extrahiert aus spezieller Stringformatierung "XXX_XXX_4.txt" die Zahl zw.
	# zweitem Unterstrich und Endung .txt, also hier "4"
	basename = name.split('.')[0]
	num = basename.split('_')[2]
	return int(num)

def getFiles(startString):
	# Returnt Liste mit Dateinamen aus aktuellem Verzeichnis, die mit dem übergebenen String beginnen
	txt_file_list = []
	for filename in os.listdir(os.getcwd()):
		if filename[0:len(startString)] == startString:
			txt_file_list.append(filename)
	txt_file_list.sort(key = getint)
	return txt_file_list

def writeFile(name, keys, vals):
	file = open(name + '.txt', 'w')
	for key in keys:
		file.write(key + '\n')

	delimiter = '-----'
	file.write(delimiter + '\n')
	width = len(vals[0])
	height = len(vals)

	for valkey in range(width):
		for valrun in range(height):
			file.write(str(vals[valrun][valkey]) + ',')
		file.write('\n')
	file.close()


print("Stebix Python Script Version 0.1")
print(' ')
print(' ')
print('Creation Date 2017-01-06')
print('Current date: ', dt.date.today())
print(' ')
print('Listing txt-content of current working directory ', os.getcwd(), ' ...')
print(' ')

exTXT = False
for entry in os.listdir(os.getcwd()):
	if entry[-4:] == '.txt':
		print(entry)
		exTXT = True
if exTXT == False:
	print('No existing TXT-Files in this directory!') 


data_files = getFiles('Sim_Info')
mf_keys = []
mf_vals = []
for filename in data_files:
	file = open(filename, 'r')
	# Inhalt des Files wird als Liste eingelesen, Element von content entspricht einer Zeile
	sf_content = list(file)
	sf_cleanData = clearHeader(escCharCleanup(sf_content), ' -----')
	keys, vals = splitData(sf_cleanData, '=')
	mf_keys = keys
	mf_vals.append(vals)

print(' ')
print(' ')
print('Please input the name for the results file: ')
name = input()
print('Creating result file ' + str(name) + '.txt ...')
writeFile(name, mf_keys, mf_vals)
print('Done, press Enter to exit')
dummy = input()