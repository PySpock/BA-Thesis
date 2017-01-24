import os
import shutil

# Script tries to locate the AnalyticalModels.py file in the current working directory
# It then copies the file to all sub-subfolders of the specified subfolder 
# here: '\\Graph Generation' in the current working directory


print('AnalyticModel Distribution Script')
print(' ')
print(' ')
print('Directory is ' + os.getcwd())
print('Listing content: ')
for item in os.listdir(os.getcwd()):
	print(item)

while True:
	print(' ')
	print('Trying to locate AnalyticModels.py in current working directory ...')
	if 'AnalyticModels.py' in os.listdir(os.getcwd()):
		print('File found!')
		am_path = os.getcwd() + '\\AnalyticModels.py'
	else:
		print('Fatal error: File AnalyticModels.py not found!')
		print('Press enter to exit')
		dummy = input()
		break

	subfolder = '\\Graph Generation'
	print('Trying to open folder ' + subfolder + ' in current working directory ...')
	try:
		fold_content = os.listdir(os.getcwd() + subfolder)
	except OSError:
		print('Fatal Error: Could not open ' + os.getcwd() + subfolder)
		print('Press enter to exit')
		dummy = input()
		break
	else:
		print(' ')
		print('Success!')
		folders_path = [os.getcwd() + subfolder + '\\' + item
						for item in fold_content 
						if os.path.isdir(os.getcwd() + subfolder + '\\' + item)]
		for fpath in folders_path:
			print('Absolute path of subfolder: ' + fpath)

	for dest in folders_path:
		shutil.copy(am_path, dest)
		print(' ')
		print('Copied AnalyticModels.py successfully to ' + dest)
	print(' ')
	print('Succesfully copied to all subfolders')
	print('Press Enter to exit script')
	dummy = input()
	break