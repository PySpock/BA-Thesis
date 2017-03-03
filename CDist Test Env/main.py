import subprocess
import numpy as np

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
	return (descriptorpath, descriptorname)