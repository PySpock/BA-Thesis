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
					   			 str(Nmax), 'inlays within', str(max_attempts), 'attempts.',
								 str(Ncurr), 'inlays of the', str(Nmax), 'requested  inlays were generated!'])
		self.Nmax = Nmax
		self.Ncurr = Ncurr
		self.max_attempts = max_attempts

class DescriptorError(Exception):
	""" Base exeption for all descriptor related errors. Used to be reraised in
		calling function/module/thread"""
	pass

class FatalSkipError(Exception):
	""" Fatal skip error ist used to reraise an exception which occured due to an
		unhandleable problem causing the algorithm to skip a stage-run in the
		simulation"""
	pass