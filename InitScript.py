import os
import datetime as dt
import random as rand
import matplotlib.pyplot as plt

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

def getFiles(startString):
	# Returnt Liste mit Dateinamen aus aktuellem Verzeichnis, die mit dem übergebenen String beginnen
	txt_file_list = []
	for filename in os.listdir(os.getcwd()):
		if filename[0:len(startString)] == startString:
			txt_file_list.append(filename)
	return txt_file_list

print("Stebix Python Script Version 0.1")
print(' ')
print(' ')
print('Creation Date 2017-01-06')
print('Current date: ', dt.date.today())
print(' ')

print('Listing content of current working directory ', os.getcwd(), ' ...')
print(' ')

if os.getcwd() != 'C:\\Users\\Jannik\\Desktop\\Python':
	print('Changing directory to: ')
	os.chdir('C:\\Users\\Jannik\\Desktop\\Python')
	print(os.getcwd())

for entry in os.listdir(os.getcwd()):
	print(entry)

print(' ')
# number = input('Please enter number of TXT-files to create: ')
number = 3

# Erstellt Dummy-Dateien zu Testzwecken

for i in range(number):
	file = open('Data' + str(i) + '.txt', 'w')
	file.write('{ASCII Header: Morituri te salutant} \n')
	file.write('-------------\n')
	for it in range(6):
		file.write('DataPoint ' + str(it) + ': ' + str(rand.uniform(0, 3)) + '\n')
	file.close()

data_files = getFiles('Data')

style_list = ['ro', 'g^', 'go']


for filename, style in zip(data_files, style_list):
	file = open(filename, 'r')
	# Inhalt des Files wird als Liste eingelesen, Element von content entspricht einer Zeile
	content = list(file)
	cleanData = clearHeader(escCharCleanup(content), '-------------')
	keys, vals = splitData(cleanData, ':')
	plt.plot(vals, style)


plt.show()

print(number)
input('Press ENTER to close program 345346')

print('input a numvber')
n = input()

print(int(n) ** 3)