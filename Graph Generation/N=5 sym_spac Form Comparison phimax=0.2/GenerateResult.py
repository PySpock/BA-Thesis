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

resf_Sp = 'SphRes.txt'
resf_Cub = 'CubRes.txt'
resf_Tri = 'TriRes.txt'
resf_Rho = 'RhoRes.txt'
resf_invTri = 'invTriRes.txt'
resf_ElB = 'ElpBRes.txt'
resf_ElH = 'ElpHRes.txt'

sp_keys, sp_vals = getData(resf_Sp)
cb_keys, cb_vals = getData(resf_Cub)
tr_keys, tr_vals = getData(resf_Tri)
rh_keys, rh_vals = getData(resf_Rho)
itr_keys, itr_vals = getData(resf_invTri)
elb_keys, elb_vals = getData(resf_ElB)
elh_keys, elh_vals = getData(resf_ElH)

# Code, e.g. plotting

#print(sp_keys)
#print(cb_keys)
#print(cb_vals)
#print(rh_vals)

vF = np.linspace(0.005, 0.2, 250)
ki = 1.00
km = 0.01
color = ['r-', 'g-', 'y-', 'k-', 'm-', 'b-']
itr = 0


#for modelname, model in am.funcPack_maxwellbased().items():
#	plt.plot(vF, model(ki, km, vF), color[itr], label=modelname)
#	itr += 1

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_ylim(0.00975,0.0315)
ax.set_xlim(0,0.21)
ax.set_xlabel('Volume fraction $\phi$ ')
ax.set_ylabel('Eff. Wärmeleitfähigkeit $\lambda$ in $\mathrm{W (m \cdot K)^{-1}}$')

ax.plot(sp_vals[1], sp_vals[0], 'ro', label='Kreisform')
ax.plot(cb_vals[1], cb_vals[0], 'gs', label='Quadratform')
ax.plot(tr_vals[1], tr_vals[0], 'y^', label='Dreieicksform')
ax.plot(itr_vals[1], itr_vals[0], 'mv', label='Dreicksform inv.')
ax.plot(rh_vals[1], rh_vals[0], 'bd', label='Rhombusform')
ax.plot(elb_vals[1], elb_vals[0], 'kp', label='Ellipsenform waager.')
ax.plot(elh_vals[1], elh_vals[0], 'ch', label='Ellipsenform senkr.')

ax.legend(loc=2)

fig.savefig('N=5 sym_spac FormComp phiM=0.2.eps')
fig.savefig('N=5 sym_spac FormComp phiM=0.2.pdf')
fig.savefig('N=5 sym_spac FormComp phiM=0.2.png', dpi=400)
plt.show()


