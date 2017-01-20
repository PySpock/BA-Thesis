import os
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
		val_lines_clean = []
		for stritem in val_lines:
			cache = stritem.split(',')
			val_lines_clean.append([float(value) for value in cache[:-1]])
	return key_lines, val_lines_clean

# Path data to TXT-file with simulation results
# Specify path and name ("hardcoded variables")

filepath = 'C:\\Users\\Jannik\\Desktop\\NewData'
resultfile = 'RandSphere.txt'
delimiter = '-----'

if os.path.isdir(filepath):
	os.chdir(filepath)
	lines = readFile(resultfile)
	keys, vals = separateKeysVals(lines, delimiter)
else:
	print('Path does not exist: ' + filepath)

# Code, e.g. plotting

print(keys)
print(vals)

vF = np.linspace(0.01,0.25,200)
ki = 1.00
km = 0.01

v1corr = [0.25 * vFrac for vFrac in vals[1]]

mx = am.maxwell(ki,km,vF)
cg = am.ChiewGland(ki,km,vF)
rl = am.rayleigh(ki,km,vF)

plt.plot(v1corr, vals[0], 'ro', label='kEff from FEM/numerical')
plt.plot(vF, mx, 'g-', label='Maxwell')
plt.plot(vF, cg, 'b-', label='ChiewGland')
plt.plot(vF, rl, 'y-', label='Rayleigh')
plt.legend(loc=2)
plt.show()