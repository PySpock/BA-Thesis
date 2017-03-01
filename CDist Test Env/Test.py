class Error(Exception):
	pass

class GenError(Exception):
	"""aszdgudzfg"""
	def __init__(self, message, a, b):
		self.a = a
		self.message = message
		self.b = b



def bigger(a,b):
	if a>b:
		raise GenError('fies', a, b)
	else:
		print('nais')


print('lol')
print('')

f=2
g=1

try:
	bigger(f,g)
except GenError as ge:
	print('ready')
	print(ge.message, ge.a, ge.b)
