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

def plotmodels(kInlay, kMatrix, phi):
	for key, funcparam in am.funcPack_maxwellbased().items():
		ax.axhline(funcparam[0](kInlay, kMatrix, phi), label=key, color=funcparam[1][0],
				   ls=funcparam[1][1:])

# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

title = 'Rand_Disp phi=0.2 Nrg=5_50 avg=20 d=0.015'

rfile_close = 'CompiledResult d0001.txt'
rfile_med = 'CompiledResult d0005.txt'
rfile_far = 'CompiledResult d001.txt'
rfile_efar = 'CompiledResult d0015.txt'

ckeys, cvals = getData(rfile_close)
mkeys, mvals = getData(rfile_med)
fkeys, fvals = getData(rfile_far)
fekeys, fevals = getData(rfile_efar)

# Code, e.g. plotting

#print(fkeys)
#print(fvals)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_title(title)

ax.set_xlim(4, 51)
#ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Anzahl der Inhomogenitäten N')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')

ax.errorbar(cvals[5], cvals[0], yerr=cvals[1], fmt='ro', label='Simulationswert $\lambda(N) \quad d=0.001$')
ax.errorbar(mvals[5], mvals[0], yerr=mvals[1], fmt='bo', label='Simulationswert $\lambda(N) \quad d=0.005$')
ax.errorbar(fvals[5], fvals[0], yerr=fvals[1], fmt='go', label='Simulationswert $\lambda(N) \quad d=0.01$')
ax.errorbar(fevals[5], fevals[0], yerr=fevals[1], fmt='yo', label='Simulationswert $\lambda(N) \quad d=0.015$')

plotmodels(1,0.01,0.2)

ax.legend(loc=1)

fig.savefig(title + '.pdf')
#fig.savefig(title + '.png', dpi=800)
plt.show()