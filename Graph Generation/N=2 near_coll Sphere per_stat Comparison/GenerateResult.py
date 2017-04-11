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

rf_per = 'Nc_Sph_Per.txt'
rf_stat = 'Nc_Sph.txt'

skeys, svals = getData(rf_stat)
pkeys, pvals = getData(rf_per)

# Code, e.g. plotting

# print(pkeys)
# print(skeys)


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_ylim(0.0105, 0.0111)
ax.set_xlim(-2, 2)

ax.set_xlabel('Abstand Inhomogenitäten $d$ / m ')
ax.set_ylabel('Effektive Wärmeleitfähigkeit $\lambda_{\mathrm{eff}}$ / $\mathrm{W (m \cdot K)^{-1}}$')


ax.plot(svals[3], svals[0], 'r+', label='Stat. Randbedingungen', markersize=8, markeredgewidth=1.25)
ax.plot(pvals[3], pvals[0], 'gx', label='Period. Randbedingungen', markersize=8, markeredgewidth=1.0)

ax.legend(loc=8)

ax.annotate('', xy=(-1.7, 0.0108), xytext=(-0.3, 0.0108), arrowprops={'arrowstyle': '|-|'})
ax.annotate('b)', xy=(-1.0, 0.010825))

ax.annotate('', xy=(1.7, 0.0108), xytext=(0.3, 0.0108), arrowprops={'arrowstyle': '|-|'})
ax.annotate('b)', xy=(1.0, 0.010825))

ax.annotate('', xy=(-0.3, 0.010635), xytext=(0.3, 0.010635), arrowprops={'arrowstyle': '|-|'})
ax.annotate('a)', xy=(-0.05, 0.010645))

ax.annotate('', xy=(-2.0, 0.0109), xytext=(-1.7, 0.0109), arrowprops={'arrowstyle': '|-|'})
ax.annotate('c)', xy=(-1.9, 0.01092))

ax.annotate('', xy=(1.7, 0.0109), xytext=(2.0, 0.0109), arrowprops={'arrowstyle': '|-|'})
ax.annotate('c)', xy=(1.8, 0.01092))

fig.savefig('N=2 near_coll per_statComp.pdf')

#fig.savefig('N=2 near_coll per_statComp.eps')
#fig.savefig('N=2 near_coll per_statComp.png', dpi=400)

plt.show()