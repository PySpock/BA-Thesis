import os 
import subprocess
import threading as th
import time
from tqdm import tqdm

def printfile(fname='test.txt'):
	with open(fname, 'r') as f:
		content = list(f)
		for item in content:
			print(item.strip())

cache = ['line1\n', 'line2\n', 'line3\n']
with open('test.txt', 'w') as newfile:
	for line in cache:
		newfile.write(line)

"""print('please modify accordingly and save:')
subprocess.run(['notepad.exe', 'test.txt'])
printfile()
input()
"""



def writefiles(flist=['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']):
	i = 0
	for file in flist:
		with open(file, 'w') as cf:
			cf.write('this is an emergency')
		print('written ', file, 'to disk')
		time.sleep(1)



newthread = th.Thread(target=writefiles, name='umpalumpa')
#newthread.start()

from tqdm import trange


for i in trange(10, desc='1st loop'):
    for j in trange(5, desc='2nd loop', leave=False):
        for k in trange(100, desc='3nd loop'):
            time.sleep(0.01)

print(newthread.name)
