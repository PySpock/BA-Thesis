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


def plot_maxwellbased(kInlay=1.00, kMatrix=0.01, inlayVolFrac=0.1):
	nmin = 0
	nmax = 100
	for name, funcpar in am.funcPack_maxwellbased().items():
		ax.hlines(funcpar[0](kInlay, kMatrix, inlayVolFrac), nmin, nmax, label=name,
					color=funcpar[1][0], linestyle=funcpar[1][1:])


def plot_lewisniels(kInlay=1.00, kMatrix=0.01, inlayVolFrac=0.1):
	nmin = 0
	nmax = 100
	for name, funcpar in am.funcPack_lewisniels().items():
		ax.hlines(funcpar[0](kInlay, kMatrix, inlayVolFrac), nmin, nmax, label=name,
					color=funcpar[1][0], linestyle=funcpar[1][1:])


# Path data to TXT-file with simulation results
# Specify (path and) name as "hardcoded variables"

rfile_vclose = 'CompiledResult.txt'

vckeys, vcvals = getData(rfile_vclose)

title = 'phi=0.3 Nrg=5_30 avg_runs=300 d=0.001 ngrid=200'

# Code, e.g. plotting


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlim(4, 31)
ax.set_xlabel('Anzahl der Inhomogenitäten N')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')

ax.set_title('phi=0.3 Nrg=5_30 avg_runs=300 d=0.001 ngrid=200')

ax.errorbar(vcvals[5], vcvals[0], yerr=vcvals[1], fmt='ko', label='Simulationswert $\lambda(N) \quad d=0.001$')
plot_lewisniels(inlayVolFrac=0.3)
plot_maxwellbased(inlayVolFrac=0.3)

ax.legend(loc=1)

fig.savefig(title + '.pdf')
plt.show()