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
	return key_lines, vals_split


def getData(resultfile, delim='-----'):
	file_lines = readFile(resultfile)
	key_data, val_data = separateKeysVals(file_lines, delim)
	return key_data, val_data

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

rfile = 'CompiledResult.txt'

keys, vals = getData(rfile)

# Code, e.g. plotting

#print(keys)
#print(vals)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlim(4, 76)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Anzahl der Inhomogenitäten $i$')
ax.set_ylabel('Wärmeleitfähigkeit $\langle \lambda_{\mathrm{eff}} \\rangle$ / $\mathrm{W (m \cdot K)^{-1}}$')

ax.errorbar(vals[5], vals[0], yerr=vals[1], fmt='ro', label='Simulationswert $\langle \lambda_{\mathrm{eff}} \\rangle (i)$')

ax.hlines(0.01487, 4, 76, label='RayleighYY', linestyle='dashed')

ax.legend(loc=1)

fig.savefig('Rand_Disp phi=0.20 Nrg=5_75 avg=50 d=0.01 ng=200.pdf')
#fig.savefig('Rand_Disp phi=0.05 Nmax=50.png', dpi=800)
plt.show()