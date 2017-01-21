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
			val_lines_clean.append([float(value) for value in cache])
	return key_lines, val_lines_clean

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

resultfile = 'RandSpheres.txt'
delimiter = '-----'

lines = readFile(resultfile)
keys, vals = separateKeysVals(lines, delimiter)

# Code, e.g. plotting

print(keys)
print(vals)

vF = np.linspace(0.005,0.125,200)
ki = 1.00
km = 0.01

mx = am.maxwell(ki,km,vF)
cg = am.ChiewGland(ki,km,vF)
rl = am.rayleigh(ki,km,vF)
rlYY = am.rayleighYY(ki,km,vF)
mean_rl = 0.5 * (rl + rlYY)

plt.plot(vals[1], vals[0], 'ro', label='kEff from FEM/numerical')
plt.plot(vF, mx, 'g-', label='Maxwell')
plt.plot(vF, cg, 'b-', label='ChiewGland')
plt.plot(vF, rl, 'y-', label='Rayleigh')
plt.plot(vF, rlYY, 'm-', label='RayleighYY')
plt.plot(vF, mean_rl, 'k-', label='Mean of Rayl. and Rayl.YY')
plt.legend(loc=2)
plt.show()