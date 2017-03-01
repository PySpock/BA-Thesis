# Brute force generating script for center positions of N circles in a 
# rectangle with the dimensions xLen and yLen. The circles are non-overlapping and 
# have a minimal distance delta to all other objects like boundaries
# or neighbor circles

import numpy as np
import math as m
import random as rnd
import os
import subprocess
import ExtractScript as es

class InlayGenerationError(Exception):
	"""Base exception class for all errors occurring during inlay position
	   generation"""
	 pass

class MeshCollisionError(InlayGenerationError):
	"""Raised if inlay size plus delta wiggle room exceeds base mesh size"""
	def __init__(self, rad, yL, delta, msg=None):
		if msg is None:
			msg = ' '.join(['Inlay with r=', rad, 'exceeds base mesh dimension',
						    'yL=', yL, 'plus wiggle room delta=', delta])
		self.rad = rad
		self.yL = yL
		self.delta = delta

class GenerationAttemptsExceeded(InlayGenerationError):
	"""Exeption for failure of circle generation within the defined max_attempts
	   limits. This happens if the maximum packing is reached or the algorithm generated
	   the first inlay positions in such a lavish manner that no more inlays fit in"""
	def __init__(self, Nmax, Ncurr, max_attempts, msg=None):
		if msg is None:
			self.msg = ' '.join(['Warning: Algorithm was unable to generate the requested',
					   			 Nmax, 'inlays within', max_attempts, 'attempts.',
								 Ncurr, 'inlays of the', Nmax, 'requested  inlays were generated!'])
		self.Nmax = Nmax
		self.Ncurr = Ncurr
		self.max_attempts = max_attempts


# Set verbosity of console output globally for more info/debugging:
verbose = False
# Be careful with verbosity setting. The console output gets quite big
# for large numbers of particles/inlays/circles




def dist(posA, posB):
	"""Calculates the distance of two points in a cartesian coordinate system"""
	d = m.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)
	return d


def radius(N, phi, xL=1.0, yL=0.1):
	"""	Given the total number of inlays N, volume fraction phi and underlying
	mesh dimensions xL and yL, this function calculates the radius
	of a single inlay"""
	r = np.power((4 * xL * yL * phi) / (np.pi * N), 0.5)
	return r


def debug(string):
	if verbose:
		print(string)


def flexArr(vals):
	""" Converts a Python list -> vals to a flexPDE-styled array of the form
	array(val1, val2, ..., valN). Output as string so it can be written to the
	descripto file"""
	f_array = 'array(' + ','.join([str(val) for val in vals]) + ')'
	return f_array


def compatible(newpos, rad, ex_circles, delta=0.01):
	"""	Check wether the inlay specified by newpos-coordinates with radius rad
	is compatible with all the other inlays in the list of existing inlays ex_circles
	within the minimum distance margin delta"""
	comp_OK = True
	for cpos in ex_circles:
		if dist(newpos,cpos) < 2 * rad + delta:
			comp_OK = False
			debug('Violation found: ' + str(dist(newpos,cpos) - 2 * rad - delta))
			debug(str(cpos) + ' position: ' + str(ex_circles.index(cpos)))
			debug(' ')
			break
		else:
			debug('Accord found: ' + str(dist(newpos,cpos) - 2 * rad - delta))
			debug(str(cpos) + ' position: ' + str(ex_circles.index(cpos)))
	return comp_OK


def generateInlayPos(N, phi, delta=0.01, max_attempts=100000, xL=1.0, yL=0.1):
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
		raise MeshCollisionError(rad, yL, delta)
	intervX = xL - rad - delta
	intervY = yL - rad - delta
	ctr = 0
	circles = []
	while len(circles) < N:
		newX = rnd.uniform(-intervX,intervX)
		newY = rnd.uniform(-intervY,intervY)
		if compatible([newX,newY], rad, circles, delta):
			circles.append([newX,newY])
			debug('Appended!')
			debug(str(circles))
			debug('Length: ' + str(len(circles)))
		ctr = ctr + 1
		if ctr >= max_attempts:
			raise GenerationAttemptsExceeded(N, len(circles), max_attempts)
	return fail_chk, circles


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
		print('Fatal Error while opening ' + filename + ' Could not complete action.')
		return
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
		print('Fatal Error while writing ' + filename + ' Could not complete action.')
		return
	else:
		for line in desc_lines:
			file.write(line + '\n')
		file.close()





def compileAvgResults(startString='Avg_Res'):
	"""	This function collects the data from every average/meta-simulation run and compiles
	it into one file. For the effective heat conductivity, it calculates the mean, standard
	deviation and standard error over all averaging runs for every number of inlays separately"""
	avg_run_files = es.getFiles(startString)
	with open(avg_run_files[0], 'r') as canary_file:
		content = list(canary_file)
		last_header_line = content.index('-----\n') + 1

	avg_run_results = np.expand_dims(np.genfromtxt(avg_run_files[0], dtype=np.float64, delimiter=',',
									skip_header=last_header_line, autostrip=True), axis=0)

	for single_runfile in avg_run_files[1:]:
		single_run_arr = np.genfromtxt(single_runfile, dtype=np.float64, delimiter=',',
									   skip_header=last_header_line, autostrip=True)

		avg_run_results = np.concatenate((avg_run_results, 
										  np.expand_dims(single_run_arr, axis=0)), axis=0)

	kMean = np.expand_dims(avg_run_results.mean(axis=0)[0], axis=0)
	kSdev = np.expand_dims(avg_run_results.std(axis=0)[0], axis=0)
	kSerr = kSdev / np.sqrt(len(avg_run_files))
	compiled_results = np.concatenate((kMean, kSdev, kSerr, avg_run_results[1, 1:, :]))

	key_list = ['kMean\n', 'kStDev\n', 'kStdErr\n'] + content[1:last_header_line-1] + ['-----']
	keys = ''.join(key_list)

	np.savetxt('CompiledResult.txt', compiled_results, newline='\n', delimiter=',',
				header=keys, comments='')



def single_simuRun(N_arr, phi, delta=0.01, xL=1.0, yL=0.1):
	flexepath = 'C:\\FlexPDE6\\FlexPDE6n.exe'
	#descriptorpath = 'C:\\Users\\Jannik\\Desktop\\Summary\\Rand_Disp phi=0.05 Nmax=50 copy'
	descriptorpath = 'C:\\Users\\stebanij\\Desktop\\Rand_Disp phi=0.05 Nmax=50 copy'
	descriptorname = 'Rand_Disp Sphere.pde'
	try:
		os.chdir(descriptorpath)
	except OSError:
		print('Error: Could not change directory to ' + descriptorpath)
		print('Aborting simulation run.')
		return

	stagenum = 0
	modpars = ['stagenum = ','number = ','xOff = ','yOff = ','volFrac=']
	update = [0 for param in modpars]
	
	for N in N_arr:
		fail_flag, raw_pos = generateCircles(N, phi, delta, xL, yL)
		stagenum = stagenum + 1
		if fail_flag:
			scratch_retries = 0
			while scratch_retries < 5:
				scratch_retries += 1
				print(' ')
				print('Retrying circle generation from scratch by erasing preexisting')
				print('circle positions! Retry: ', scratch_retries)
				print(' ')
				fail_flag, raw_pos = generateCircles(N, phi, delta, xL, yL)
				if not fail_flag:
					print('Success at regenerating positions!')
					break
				elif scratch_retries >= 5:
					print('Skipping simulation run ', stagenum, ' due to error during particle generation.')
					print('Possible error #1: Particle radius bigger than matrix dimension')
					print('Possible error #2: Failed to find valid positions for ', N, ' particles')
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
		updateDescriptor(update, descriptorname)
		# Run simulation for current iteration in flexPDE
		print('Doing stage run ', stagenum, ' Simulating ', N, 'particles/inlays.')
		max_timeouts = 10
		timeouts = 0
		while True:
			try:
				subprocess.call([flexepath, descriptorpath + '\\' + descriptorname], timeout=25)
			except subprocess.TimeoutExpired:
				print(' ')
				print('FlexPDE6n.exe timed out. Retrying current simulation ...')
				print(' ')
				timeouts += 1
				if timeouts >= max_timeouts:
					print('Maximum timeout threshold of ', max_timeouts, ' reached.')
					print('Re-generating current geometry and restarting ...')
					__, raw_pos = generateCircles(N, phi, delta, xL, yL)
					xPos = sortPos(raw_pos)[0]
					yPos = sortPos(raw_pos)[1]
					update[2] = modpars[2] + flexArr(xPos)
					update[3] = modpars[3] + flexArr(yPos)
					updateDescriptor(update, descriptorname)
					timeouts = 0
				continue
			else:
				break
		print(' ')
	print('Finished simulation run!')


def average_simuRun(N_arr, phi, avg_runs, delta=0.01, xL=1.0, yL=0.1):
	for itr in range(1, avg_runs + 1):
		print(' ')
		print('##########################################')
		print('Conducting averaging run', itr, ' of ', avg_runs)
		print('##########################################')
		print(' ')
		single_simuRun(N_arr, phi, delta, xL, yL)
		es.compileResults('Avg_Res_' + str(itr))
	compileAvgResults()



# Set simulation parameters # spheres = nC and volume fraction = phi

nC = 10
phi = 0.3




# Parameter run:

paramN = np.arange(5, 31, 1)
average_simuRun(paramN, phi, avg_runs=30, delta=0.01)