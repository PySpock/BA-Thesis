class Error(Exception):
	pass

class GenError(Exception):
	"""aszdgudzfg"""
	def __init__(self,message,a,b):
		self.a = a
		self.message = message
		self.b = b

class testc():
	i = 1
	pass


def hilo(a,b):
	if a>b:
		raise GenError('fies',1,3)
	else:
		print('nais')


print('lol')
a = testc()
a.x = 10

f=2
g=1

try:
	hilo(f,g)
except GenError as ge:
	print('ready')
	print(ge.a)