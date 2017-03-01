import os

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
		folderpath = input('Path=')
		if not os.path.isdir(folderpath):
			print('Fatal error: Invalid path or folder missing!')
			print('Please retry!')
			continue
		os.chdir(folderpath)
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
	return (folderpath, descriptorname)

def get_Nrange():
	""" Reads the parameters for inlay numbers (Nmin, Nmax, stepsize dN) into a tuple, which 
		is returned"""
	print('Please specify the range over which the number of particles is varied.')
	print('The necessary parameters are the minimal number of inlays Nmin, the ')
	print('maximal number Nmax and the step size dN by which the number of inlays')
	print('is increased in every simulation run from Nmin to Nmax')
	print()
	while True:
		nmin = input('Nmin = ')
		nmax = input('Nmax = ')
		dn = input('dN = ')
		print('Nmin=', nmin, '  Nmax=', nmax, '  dN=', dn)
		print('Continue [ENTER] or re-enter values [r]')
		switch = input()
		if switch == 'R' or switch == 'r':
			continue
		break
	return (nmin, nmax, dn)

def get_other_params():
	""" Reads the parameters for averaging runs (avg_runs), volume fraction (phi), minimal
		distance between border and inlays (delta) as well as matrix dimensions (xL, yL)
		into a tuple which is returned"""
	while True:
		xL = 1.0
		yL = 0.1
		print('Please specify the number of averaging runs to conduct:')
		avg_runs = input('Avg_Runs=')
		print('Please specify the volume fraction of the particles:')
		phi = input('Phi=')
		print('Please specify the minimal distance delta between the inlays themselves')
		print('and between the inlays and the matrix border:')
		delta = input('Delta=')
		print('Use default values (xL = 1.0, yL = 0.1) for matrix dimeension [ENTER] or')
		print('specify them [r]')
		switch = input()
		if switch == 'R' or switch == 'r':
			xL = input('xL = ')
			yL = input('yL = ')
		print('Avg_Runs=', avg_runs,'Phi=', phi, '  Delta=', delta, '  xL=', xL, '  yL=',yL)
		print('Continue [ENTER] or re-enter values [r]')
		switch = input()
		if switch == 'R' or switch == 'r':
			continue
		break
	return (avg_runs, phi, delta, xL, yL)

def userinput_parameters(path_tup):
	while True:
		nrg_tup = get_Nrange()
		otherparam_tup = get_other_params()
		parameters = path_tup + nrg_tup + otherparam_tup
		print('Using simulation parameters ')
		print('(descpath, descname, Nmin, Nmax, dN, Avg_Runs, Phi, Delta, xL, yL)')
		print(parameters)
		print('Continue with [ENTER] or re-enter values with [r]')
		switch = input()
		if switch == 'R' or switch == 'r':
			continue
		break
	return parameters

def read_simconfig(cfgfile):
	simvars = ['Nmin', 'Nmax', 'dN', 'Avg_Runs', 'Phi', 'Delta', 'xL', 'yL']
	with open(cfgfile, 'r') as cfg:
		rawlines = list(cfg)
	lines = [item.strip() for item in rawlines]


def simconfig(cfgfile='SimConfig.txt'):
	filelist = os.listdir(os.getcwd())
	for filename in filelist:
		if filename == cfgfile:
			print('SimConfig.txt file found!')


def create_foldersystem(parentdir):
	pass
		

print('Stebix main init script')
path_tup = get_path()
userinput_parameters(path_tup)