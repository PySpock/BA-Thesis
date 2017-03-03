import os 
import subprocess
import multiprocessing as mp
import time
from tqdm import tqdm
import logging
import errors

def printfile(fname='test.txt'):
	with open(fname, 'r') as f:
		content = list(f)
		for item in content:
			print(item.strip())

"""
cache = ['line1\n', 'line2\n', 'line3\n']
with open('test.txt', 'w') as newfile:
	for line in cache:
		newfile.write(line)

print('please modify accordingly and save:')
subprocess.run(['notepad.exe', 'test.txt'])
printfile()
input()
"""
class asdf:
	pass

def ladd(lista, listb):
	result = []
	for a, b in zip(lista, listb):
		result.append(a + b)
		logging.debug('Intermediate result:  ' + str(a + b))
		time.sleep(0.05)
	return result



def writefiles(flist=['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']):
	i = 0
	for file in flist:
		with open(file, 'w') as cf:
			cf.write('this is an emergency')
		print('written ', file, 'to disk')
		time.sleep(1)


def pi(s):
	print(s)
	time.sleep(0.25)

class simproc(mp.Process):

	def __init__(self, tms, char='n'):
		self.tms = tms
		self.char = char

	def run(self):
		for n in range(self.tms):
			pi(self.char)


s1 = simproc(5, char='n')
s2 = simproc(5, char='k')
s1.run()
s2.run()
