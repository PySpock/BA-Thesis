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


def getData(resultfile, delim='-----'):
	file_lines = readFile(resultfile)
	key_data, val_data = separateKeysVals(file_lines, delim)
	return key_data, val_data

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

rfile = 'RndDsp50.txt'

keys, vals = getData(rfile)

# Code, e.g. plotting

print(keys)
print(vals)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

#ax.set_xlim(0.008, 0.385)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Anzahl der Inhomogenitäten N')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')


ax.plot(vals[3], vals[0], 'ro', label='Simulationswert $\lambda$(N)')


ax.legend(loc=1)

fig.savefig('Rand_Disp phi=0.05 Nmax=50.eps')
fig.savefig('Rand_Disp phi=0.05 Nmax=50.pdf')
fig.savefig('Rand_Disp phi=0.05 Nmax=50.png', dpi=800)
plt.show()
