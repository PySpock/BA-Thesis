import subprocess
import numpy as np
import os
import shutil as sh
import simulation as sim


def get_name(filelist):
	""" Filters out the felxPDE problem descriptor file in the passed list of filenames
		fileslist by looking for the file suffix .pde. All filenames with a .pde-suffix
		are returned"""
	descriptorlist = []
	for file in filelist:
		if file[-4:] == '.pde':
			descriptorlist.append(file)
	return descriptorlist


def get_path():
	""" Get user input on where the path to the descriptor file on which the simulation run
		will be based on"""
	while True:
		print('Please specify the folder path where the blueprint descriptor file is located: ')
		descriptorpath = input('Path=')

		if not os.path.isdir(descriptorpath):
			print('Fatal error: Invalid path or folder missing!')
			print('Please retry!')
			continue

		os.chdir(descriptorpath)
		filelist = os.listdir(os.getcwd())
		descriptorname = get_name(filelist)

		if len(descriptorname) > 1:
			print('Warning: Multiple descriptor files in specified directory!')
			print('Using first file as working descriptor.')
		elif len(descriptorname) == 0:
			print('Fatal Error: No flexPDE descriptor file found!')
			print('Please specify folder with problem descriptor file')
			continue

		descriptorname = descriptorname[0]
		break

	return descriptorpath, descriptorname

def simconfig():
	""" Create a TXT-Config file which configures/saves the important simulation parameters"""
	char = '#'
	sharps = 85 * char + '\n'

	baseconfig = ''.join([sharps,'# flexPDE Simulation Configurator\n', '#\n',
							'# Please fill in the desired simulation parameters directly\n',
							'# after the equal signs and save the file.\n',
							'#\n', 
							'# Nmin - minimal number of inlays (conditions: natural number)\n',
							'# Nmax - upper number of inlays (conditions: natural number and Nmin < Nmax)\n',
							'# dN - stepsize of inlay number (condition: natural number)\n',
							'# avg_runs - number of averaging runs over all configurations\n',
							'# phi - volume fraction of filler particles (condition: float 0 < phi < 1)\n',
							'# delta - distance betw. inlays and inlays/matrix (condition: float & reasonable)\n',
							'#\n',
							 sharps, sharps, sharps,
							'Nmin=\n', 'Nmax=\n', 'dN=\n', 'avg_runs=\n', 'phi=\n', 'delta=\n'])

	if os.path.isfile('Simconfig.txt'):
		print('Simconfig.txt already exists. Proceeding will overwrite the file')
		input('[ENTER] to continue')

	with open('Simconfig.txt', 'w') as scfg:
		for line in baseconfig:
			scfg.write(line)
	subprocess.call(['notepad.exe', 'Simconfig.txt'])

	with open('Simconfig.txt', 'r') as scfg:
		content = list(scfg)
		delim_index = list(reversed(content)).index(sharps)
		val_list = [item.strip() for item in content[-delim_index:]]
		params = [item.split('=')[0] for item in val_list]
		values = [float(item.split('=')[1]) for item in val_list]

	simpars = [int(values[0]), int(values[1]), int(values[2]), int(values[3]), values[4], values[5]]

	return simpars

def merge_runfolders():
	

def distribute_avg_runs(tot_runs, proc_target):
	runs_per_process = [tot_runs // proc_target for i in range(proc_target)]
	remainder = tot_runs % proc_target
	if remainder is 0:
		run_dist = [[1, runs_per_process[0]]]
		for i, rpp in enumerate(runs_per_process[1:], start=1):
			newelem = [run_dist[i-1][0] + rpp, run_dist[i-1][1] + rpp]
			run_dist.append(newelem)
		return run_dist

	additional_runs = 0
	remainder_processes = proc_target
	while remainder % remainder_processes is not 0:
		remainder_processes -= 1
		additional_runs = remainder_processes // remainder_processes

	for i in range(remainder_processes):
		runs_per_process[i] += additional_runs

	run_dist = [[1, runs_per_process[0]]]
	for i, rpp in enumerate(runs_per_process[1:], start=1):
		newelem = [run_dist[i-1][1] + 1, run_dist[i-1][1] + rpp]
		run_dist.append(newelem)

	return run_dist



def dispatch_simjobs(simpars, dscname, proc_target=1):
	run_dist = distribute_avg_runs(simpars[3], proc_target)
	Narr = np.arange(simpars[0], simpars[1], simpars[2])
	cdir = os.getcwd()
	dscsource = '\\'.join([cdir, dscname])
	simjob_dirs = []
	sim_proclist = []
	for itr in range(proc_target):
		simjob_dir = '\\'.join([cdir, 'output_simjob' + str(itr)])
		dscdest = '\\'.join([simjob_dir, dscname])
		simjob_dirs.append(simjob_dir)
		try:
			os.mkdir(simjob_dir)
		except FileExistsError:
			pass

		try:
			sh.copyfile(dscsource, dscdest)
		except IOError:
			print('Descfile copy failed. Reraise exception')
			pass

		sim_proclist.append(sim.SimulationProcess(simjob_dir, dscname, run_dist[itr],
													Narr, simpars[4], simpars[5]))

	for i, proc in enumerate(sim_proclist):
		proc.start()
		print('Worker ', i, 'started!')









	

if __name__ == '__main__':

	path, name = get_path()
	simpars = simconfig()
	dispatch_simjobs(simpars, name)


	pass