"""Simulation Worker"""

import os
import numpy as np
import subprocess
import multiprocessing as mp
import shutil as sh
import random as rnd
import logging
import errors
import csv


def dist(posA, posB):
	"""Calculates the distance of two points in a cartesian coordinate system"""
	d = np.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)
	return d


def radius(N, phi, xL=1.0, yL=0.1):
	"""	Given the total number of inlays N, volume fraction phi and underlying
	mesh dimensions xL and yL, this function calculates the radius
	of a single inlay"""
	r = np.power((4 * xL * yL * phi) / (np.pi * N), 0.5)
	return r


def flexArr(vals):
	""" Converts a Python list -> vals to a flexPDE-styled array of the form
	array(val1, val2, ..., valN). Output as string so it can be written to the
	descripto file"""
	f_array = 'array(' + ','.join([str(val) for val in vals]) + ')'
	return f_array


def sortPos(pos_list):
	xPos = [pos[0] for pos in pos_list]
	yPos = [pos[1] for pos in pos_list]
	return [xPos, yPos]


def compatible(newpos, rad, ex_circles, delta=0.01):
	"""	Check wether the inlay specified by newpos-coordinates with radius rad
	is compatible with all the other inlays in the list of existing inlays ex_circles
	within the minimum distance margin delta"""
	comp_OK = True
	for cpos in ex_circles:
		if dist(newpos,cpos) < 2 * rad + delta:
			comp_OK = False
			logging.debug('Violation found: ' + str(dist(newpos,cpos) - 2 * rad - delta))
			logging.debug(str(cpos) + ' position: ' + str(ex_circles.index(cpos)))
			break
		else:
			logging.debug('Accord found: ' + str(dist(newpos,cpos) - 2 * rad - delta))
			logging.debug(str(cpos) + ' position: ' + str(ex_circles.index(cpos)))
	return comp_OK


def generate_configuration(N, phi, delta=0.01, max_attempts=100000, xL=1.0, yL=0.1):
	""" Brute force funtion to randomly distribute the inlays in the underlying 
	matrix. Generates a random position within the mesh borders and then checks
	for compatibility with the pre-existing inlay positions. If a violation is 
	found, the position gets discarded and the generation restarts.
	Keywords:
				N 				number of inlays to distribute
				phi				volume fraction of filler particles
				delta			minimal distance margin between inlays 
								and inlays and matrix border
				max_attempts 	maximum number of attempts to find a
								valid position for the i-th inlay
				xLen 			matrix dimension x
				yLen			matrix dimension y"""
	rad = radius(N, phi, xL, yL)
	if rad > yL - delta:
		raise errors.MeshCollisionError(rad, yL, delta)
	intervX = xL - rad - delta
	intervY = yL - rad - delta
	ctr = 0
	configuration = []
	while len(configuration) < N:
		newX = rnd.uniform(-intervX,intervX)
		newY = rnd.uniform(-intervY,intervY)
		if compatible([newX,newY], rad, configuration, delta):
			configuration.append([newX,newY])
			logging.debug('Appended!')
			logging.debug(str(configuration))
			logging.debug('Length: ' + str(len(configuration)))
		ctr = ctr + 1
		if ctr >= max_attempts:
			raise errors.GenerationAttemptsExceeded(N, len(configuration), max_attempts)
	return configuration


def dump_config_tofile(confnum, config):
	filename = 'Config_Info_' + str(confnum) + '.txt'
	x_row = [coord[0] for coord in config]
	y_row = [coord[1] for coord in config]
	with open(filename, 'w', newline='') as confile:
		confwriter = csv.writer(confile, delimiter=',')
		confwriter.writerow(x_row)
		confwriter.writerow(y_row)


def updateDescriptor(update_lines, filename, sep=['{Modifikation Beginn}','{Modifikation Ende}']):
	""" Updates the flexPDE descriptor file with a passed list of strings. The lines between the 
		separator markers (comments in flexPDE descriptor) are fully replaced with the contents
		of the forwarded string list.
		Keyword arguments:
				update_lines			list of strings/lines which will be written between the 
										separators in a pre-existing flexPDE descriptor file
				filename				string of filename of flexPDE descriptor file to modify
				sep 					list of two strings enclosing the lines in the descriptor
										which will be overwritten. Default:
										['{Modifikation Beginn}','{Modifikation Ende}'] """
	# Open file in read-mode and update content in-place in memory
	try:
		file = open(filename, 'r')
	except (IOError, FileNotFoundError):
		logging.critical('Fatal Error while opening ' + filename + ' Could not complete action.')
		raise errors.DescriptorError
	else:
		raw_lines = list(file)
		desc_lines = [line.strip() for line in raw_lines]
		l_index = desc_lines.index(sep[0]) + 1
		h_index = desc_lines.index(sep[1])
		del desc_lines[l_index:h_index]
		for newline in reversed(update_lines):
			desc_lines.insert(l_index, newline)
		file.close()
	# Open file in write mode to overwrite with updated content from memory
	try:
		file = open(filename, 'w')
	except IOError:
		logging.critical('Fatal Error while writing ' + filename + ' Could not complete action.')
		raise errors.DescriptorError
	else:
		for line in desc_lines:
			file.write(line + '\n')
		file.close()


def single_run(descriptorpath, descriptorname, startstage, N_arr, phi, delta=0.01, xL=1.0, yL=0.1):
	flexepath = 'C:\\FlexPDE6\\FlexPDE6n.exe'
	stagenum = startstage
	modpars = ['stagenum = ','number = ','xOff = ','yOff = ','volFrac=']
	update = [0 for param in modpars]
	max_scratch_retries = 10
	
	for N in N_arr:
		stagenum += 1
		scratch_retries = 0
		while scratch_retries < max_scratch_retries:
			try:
				raw_pos = generate_configuration(N, phi, delta, max_attempts=100000, xL=1.0, yL=0.1)
				break
			except errors.MeshCollisionError as mesherr:
				logging.error(mesherr.msg)
				continue
			except errors.GenerationAttemptsExceeded as generr:
				logging.warning(generr.msg)
				scratch_retries += 1

		if scratch_retries >= max_scratch_retries:
			logging.error('Config generation failed fatally. Skipping run N')
			continue

		xPos = sortPos(raw_pos)[0]
		yPos = sortPos(raw_pos)[1]
		# Generate list of lines which are updated
		update[0] = modpars[0] + str(stagenum)
		update[1] = modpars[1] + str(int(N))
		update[2] = modpars[2] + flexArr(xPos)
		update[3] = modpars[3] + flexArr(yPos)
		update[4] = modpars[4] + str(phi)

		# Update the descriptor file
		try:
			updateDescriptor(update, descriptorname)
		except errors.DescriptorError as descerr:
			logging.error('Descriptor update failed')
			continue

		# Run simulation for current iteration in flexPDE
		logging.info('Doing stage run ' + str(stagenum) + ' Simulating ' + str(N) + 'particles/inlays.')
		max_timeouts = 10
		timeouts = 0
		timeout_time = 25
		while True:
			try:
				subprocess.call([flexepath, descriptorpath + '\\' + descriptorname], timeout=timeout_time)
			except subprocess.TimeoutExpired:
				logging.info('FlexPDE timed out. timeout_time = ' + str(timeout_time))
				timeouts += 1
				if timeouts >= max_timeouts:
					logging.warning('Maximum timeout threshold of '+ str(max_timeouts) + ' reached'
									+ 'Re-generating current geometry and restarting.')
					raw_pos = generate_configuration(N, phi, delta, max_attempts=100000, xL=1.0, yL=0.1)
					xPos = sortPos(raw_pos)[0]
					yPos = sortPos(raw_pos)[1]
					update[2] = modpars[2] + flexArr(xPos)
					update[3] = modpars[3] + flexArr(yPos)
					updateDescriptor(update, descriptorname)
					timeouts = 0
				continue
			else:
				dump_config_tofile(stagenum, raw_pos)
				break
	logging.info('Finished single simulation run!')


def move_files(startstrings, src, dest):
	dirlist = os.listdir(src)
	movfiles = []
	for startstring in startstrings:
		for item in dirlist:
			if item[0:len(startstring)] == startstring:
				movfiles.append(item)

	f_src = ['\\'.join([src, movfile]) for movfile in movfiles ]
	f_dest = ['\\'.join([dest, movfile]) for movfile in movfiles]

	for src, dest in zip(f_src, f_dest):
		sh.move(src, dest)

def create_folders(avg_runs):
	procpath = os.getcwd()
	datapath = '\\'.join([procpath, 'data'])
	try:
		os.mkdir(datapath)
	except FileExistsError:
		pass
	for i in range(1, avg_runs + 1):
		runpath = '\\'.join([datapath, 'run' + str(i)])
		try:
			os.mkdir(runpath)
		except FileExistsError:
			pass


class SimulationProcess(mp.Process):
	def __init__(self, descriptorpath, descriptorname, startstage, avg_runs, Narr, phi, delta):
		self.descriptorpath = descriptorpath
		self.descriptorname = descriptorname
		self.startstage = startstage
		self.Narr = Narr
		self.avg_runs = avg_runs
		self.phi = phi
		self.delta = delta

	def run(self):
		create_folders(self.avg_runs)
		src = self.descriptorpath
		for run in range(1, self.avg_runs + 1):
			dest = '\\'.join([src, 'data', 'run' + str(run)])
			single_run(self.descriptorpath, self.descriptorname, self.startstage, self.Narr,
						self.phi, self.delta)
			move_files(['Sim_Info_', 'Config_Info_'], src, dest)
		

path = 'C:\\Users\\Jannik\\Desktop\\Rand Disp\\Rand_Disp WIP'
name = 'Rand_Disp Sphere.pde'

os.chdir(path)
print(os.getcwd())
input()

logging.basicConfig(level=logging.INFO)

s1 = SimulationProcess(path, name, 5, [1,2,3,4,5], 0.05, 0.01)
s1.run()
