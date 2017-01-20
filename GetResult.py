import numpy as np
import matplotlib.pyplot as plt

def readFile(name):
	try:
		file = open(name, 'r')
	except IOError:
		print('File ' + name + ' not found or inaccessible')
		line_list = []
		pass
	else:
		line_list_raw = list(file)
		file.close()
		line_list = [line.strip() for line in line_list_raw]
	return line_list

def separateKeysVals(line_list, delimiter):
	try:
		split_index = line_list.index(delimiter)
	except ValueError:
		return ('Empty', 'Empty')
	else:
		key_lines = line_list[:split_index]
		val_lines = line_list[split_index + 1:]
		val_lines_clean = []
		for stritem in val_lines:
			cache = stritem.split(',')
			val_lines_clean.append([float(value) for value in cache[:-1]])
	return key_lines, val_lines_clean

# Path data to TXT-file with simulation results
# Specify path and name ("hardcoded variables")

filepath = 'C:\\Users\\Jannik\\Desktop\\5 Sphere varVolFrac'
resultfile = 'Results.txt'
delimiter = '-----'

lines = readFile(resultfile)
keys, vals = separateKeysVals(lines, delimiter)

# Code, e.g. plotting