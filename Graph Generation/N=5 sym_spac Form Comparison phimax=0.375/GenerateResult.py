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

resultfileSp = 'SymSpacSpheres.txt'
resultfileCb = 'SymSpacCubes.txt'

sp_keys, sp_vals = getData(resultfileSp)
cb_keys, cb_vals = getData(resultfileCb)

# Code, e.g. plotting

print(sp_keys)
print(cb_keys)
print(sp_vals)

# Data for theoretical models

vF = np.linspace(0.0095, 0.375, 350)
ki = 1
km = 0.01


fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlim(0.008, 0.385)
ax.set_ylim(0.008, 0.065)
ax.set_xlabel('Volume fraction $\phi$ ')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')


ax.plot(sp_vals[1], sp_vals[0], 'ro', label='Kreisform')
ax.plot(cb_vals[1], cb_vals[0], 'gs', label='Quadratform')
for modelname, modelprops in am.funcPack_maxwellbased().items():
	ax.plot(vF, modelprops[0](ki, km, vF), modelprops[1], label=modelname)

ax.legend(loc=2)

fig.savefig('N=5 sym_spac FormComp phiM=0.375.eps')
fig.savefig('N=5 sym_spac FormComp phiM=0.375.pdf')
fig.savefig('N=5 sym_spac FormComp phiM=0.375.png', dpi=400)
plt.show()