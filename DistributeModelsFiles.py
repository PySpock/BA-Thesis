import os
import shutil

while True:
	print('AnalyticModel Distribution Script')
	print(' ')
	print(' ')
	print('Directory is ' + os.getcwd())
	print('Listing content: ')
	for item in os.listdir(os.getcwd()):
		print(item)

	print('Trying to locate AnalyticModels.py in current working directory ...')
	if 'AnalyticModels.py' in os.listdir(os.getcwd()):
		print('File found!')
		am_path = os.getcwd() + '\\AnalyticModels.py'
	else:
		print('Fatal error: File AnalyticModels.py not found!')
		print('Press enter to exit')
		dummy = input()
		break

	print('Trying to open folder Graph Generation in current working directory ...')
	subfolder = '\\Graph Generation'
	try:
		fold_content = os.listdir(os.getcwd() + subfolder)
		print(fold_content)
	except OSError:
		print('Fatal Error: Could not open ' + os.getcwd() + subfolder)
		print('Press enter to exit')
		dummy = input()
		break
	else:
		print('Success!')
		folders_path = [os.getcwd() + subfolder + '\\' + item
						for item in fold_content 
						if os.path.isdir(os.getcwd() + subfolder + '\\' + item)]
		print(folders_path)

	for dest in folders_path:
		shutil.copy(am_path, dest)
		print('Copied AnalyticModels.py successfully to ' + dest)
	print('Succesfully copied to all subfolders')
	print('Press Enter to exit script')
	dummy = input()
	break