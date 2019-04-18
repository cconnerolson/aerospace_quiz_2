from numpy import zeros, arange


class Problem2(object):
	"""Take-home Quiz 2, Problem 2"""
	version = '1.0'
	
	def __init__(self):
		pass
	
	def empty_data_array(self, delta=0.01):
		"""
		Creates an empty numpy array for the simulation data
		:param delta: spacing between data points
		:return:
		"""
		c = int((4 - 1.5) / delta + 1)
		array = zeros((c, 2))
		array[:, 0] = arange(1.5, (4 + delta), delta)
		return array