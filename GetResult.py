import numpy as np
import matplotlib.pyplot as plt

def readFile(name):
	file = open(name, 'r')
	line_list_raw = list(file)
	file.close()
	line_list = [line.strip() for line in line_list_raw]
	return line_list

def separateKeysVals(line_list,delimiter):
	split_index = line_list.index(delimiter)
	key_lines = line_list[:split_index]
	val_lines = line_list[split_index + 1:]
	val_lines_clean = []
	for stritem in val_lines:
		cache = stritem.split(',')
		val_lines_clean.append([float(value) for value in cache[:-1]])
	return key_lines, val_lines_clean


resultfile = 'Results.txt'
delimiter = '-----'
lines = readFile(resultfile)
keys, vals = separateKeysVals(test, delimiter)

# Man kann jetzt mit den keys und values sauber weiterarbeiten und z.b. Plotten

# Code