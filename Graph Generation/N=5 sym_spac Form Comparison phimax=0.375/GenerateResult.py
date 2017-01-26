import numpy as np
import matplotlib.pyplot as plt
import AnalyticModels as am

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
		vals_split = np.asarray([line.split(',') for line in val_lines], dtype=np.float64)
		# Implementation with "classic" Python lists
		#val_lines_clean = []
		#for stritem in val_lines:
		#	cache = stritem.split(',')
		#	val_lines_clean.append([float(value) for value in cache])
	return key_lines, vals_split

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

resultfileSp = 'SymSpacSpheres.txt'
resultfileCb = 'SymSpacCubes.txt'
delimiter = '-----'

sp_lines = readFile(resultfileSp)
cb_lines = readFile(resultfileCb)
sp_keys, sp_vals = separateKeysVals(sp_lines, delimiter)
cb_keys, cb_vals = separateKeysVals(cb_lines, delimiter)

# Code, e.g. plotting

print(sp_keys)
print(cb_keys)

plt.plot(sp_vals[1], sp_vals[0], 'ro', label='Spheres')
plt.plot(cb_vals[1], cb_vals[0], 'gs', label='Cubes')
plt.legend()
plt.show()