""" Provide a class definition of a simulation object
to refactor and generalize the function interface"""

class simtask(object):
 	"""docstring for simtask"""
 	def __init__(self, descriptorpath=None, decriptorname=None, simpars=None,
 				tot_runs=None, proc_target=None):
 		super(simtask, self).__init__()
 		self.descriptorpath = descriptorpath
 		self.descriptorname = descriptorname
 		self.simpars = simpars
 		self.tot_runs = tot_runs
 		self.proc_target = proc_target

 	def set_path(self)
 		""" Get user input on where the path to the descriptor file on
 			which the simulation run will be based on"""
		while True:
			print('Please specify the folder path where the blueprint descriptor file is located: ')
			self.descriptorpath = input('Path=')

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

			self.descriptorname = descriptorname[0]
			break

	def set_config(self):
	""" Create a TXT-Config file which configures/saves the important simulation parameters"""
	char = '#'
	sharps = 85 * char + '\n'

	baseconfig = ''.join([sharps,'# flexPDE Simulation Configurator\n', '#\n',
							'# Please fill in the desired simulation parameters directly\n',
							'# after the equal signs and save the file.\n',
							'#\n', 
							'# Nmin - minimal number of inlays (conditions: natural number)\n',
							'# Nmax - upper number of inlays (conditions:',
							' natural number and Nmin < Nmax)\n',
							'# dN - stepsize of inlay number (condition: natural number)\n',
							'# avg_runs - number of averaging runs over all configurations\n',
							'# phi - volume fraction of filler particles',
							' (condition: float 0 < phi < 1)\n',
							'# delta - distance betw. inlays and inlays/matrix',
							' (condition: float & reasonable)\n',
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

	self.simpars = [int(values[0]), int(values[1]), int(values[2]),
					 int(values[3]), values[4], values[5]]
