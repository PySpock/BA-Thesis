import numpy as np

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
#lines = readFile(resultfile)

test = ['hans','wurst','-----','1,2,3,4,5,6,','7,8,9,10,11,12']

keys, vals = separateKeysVals(test, delimiter)

print(keys)
print(vals)

