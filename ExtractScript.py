import os
import datetime as dt


def escCharCleanup(strList):
	# Returns die strList /n-Escape-Char, wenn der an erst . od. letz. Stelle eines Elements steht
	cleanData = [entry.strip() for entry in strList]
	return cleanData

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
		try:
			keyList.append(element.split(splitChar)[0])
			valList.append(float(element.split(splitChar)[1]))
		except IndexError:
			pass
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
		first_element = True
		for valrun in range(height):
			if first_element:
				file.write(str(vals[valrun][valkey]))
				first_element = False
			else:
				file.write(',' + str(vals[valrun][valkey]))
		file.write('\n')
	file.close()


print("Stebix Python Script Version 0.1")
print(' ')
print(' ')
print('Creation Date 2017-01-06')
print('Current date: ', dt.date.today())
print(' ')
print(' ')

while True:
	while True:
		print('Please input the directory with double slashes, where the flexPDE summaries are saved.')
		path = input('Input path: ')
		if os.path.isdir(path):
			print('Success, directory exists')
			os.chdir(path)
			break
		print('Error: No such directory found')


	print('Listing txt-content of set working directory ', os.getcwd(), ' ...')
	print(' ')

	exTXT = False
	for entry in os.listdir(os.getcwd()):
		if entry.endswith('.txt'):
			print(entry)
			exTXT = True
	if not exTXT:
		print('No existing TXT-Files in this directory!') 


	data_files = getFiles('Sim_Info_')
	mf_keys = []
	mf_vals = []
	for filename in data_files:
		file = open(filename, 'r')
		# Inhalt des Files wird als Liste eingelesen, Element von content entspricht einer Zeile
		sf_content = list(file)
		sf_cleanData = clearHeader(escCharCleanup(sf_content), '-----')
		keys, vals = splitData(sf_cleanData, '=')
		mf_keys = keys
		mf_vals.append(vals)

	print(' ')
	print(' ')
	print('Please input the name for the results file: ')
	name = input()
	print('Creating result file ' + str(name) + '.txt ...')
	writeFile(name, mf_keys, mf_vals)
	print('Done!')

	cont = True
	while True:
		print('Continue with another task [C] or exit [X]?')
		action = input()
		if action == 'C' or action == 'c':
			break
		elif action == 'X' or action == 'x':
			cont = False
			break
		print('Invalid input!')
	if cont == False:
		break