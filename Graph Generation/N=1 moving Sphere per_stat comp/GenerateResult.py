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
		vals_split = np.asarray([line.split(',') for line in val_lines], dtype=np.float64)
		# Implementation with "classic" Python lists
		#val_lines_clean = []
		#for stritem in val_lines:
		#	cache = stritem.split(',')
		#	val_lines_clean.append([float(value) for value in cache])
	return key_lines, vals_split

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

per_res = 'PerRes.txt'
stat_res = 'StatRes.txt'
delimiter = '-----'

per_lines = readFile(per_res)
pkeys, pvals = separateKeysVals(per_lines, delimiter)

stat_lines = readFile(stat_res)
skeys, svals = separateKeysVals(stat_lines, delimiter)

# Code, e.g. plotting

print(pkeys)
print(pvals)
print(svals)


plt.rc('font', family='serif')
plt.plot(svals[2], 1000*svals[0], 'ro', label='Feste Randbedingung')
plt.plot(pvals[2], 1000*pvals[0], 'g^', label='Periodische Randbedingung')
plt.xlabel('Position der Inhomogenität ' r'x / m')
plt.ylabel('Effektive Wärmeleitfähigkeit   ' r'$\mathregular{\lambda_{eff} \: / \: mW(m \cdot K)^{-1}}$')
plt.legend(loc=8)
plt.savefig('Stat_Per_Comp.pdf')
plt.show()