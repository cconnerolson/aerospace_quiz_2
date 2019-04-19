import numpy as np
import pandas

data = pandas.read_csv('data/isentropic_flow_table.csv')  # , names=colnames)

M_data = data.Ma.tolist()
P_data = data.p.tolist()
T_data = data.t.tolist()
A_data = data.A.tolist()


# print(A_data)

class IsentropicFlow(object):
	"""Isentropic Flow Table Lookup Toolkit"""
	version = '0.1'
	
	def __init__(self, M=0, P=0, T=0, A=0, verbose=False):
		self.M = M
		self.P = P
		self.T = T
		self.A = A
		self.verbose = verbose
	
	def __repr__(self):
		return "IsentropicFlow({}, {}, {}, {})".format(self.M, self.P, self.T, self.A)
	
	def __str__(self):
		return 'M = {}\nP = {}\nT = {}\nA = {}'.format(self.M, self.P, self.T, self.A)
	
	def mach_lookup(self):
		"""
		Returns pressure ratio, temperature ratio, and area ratio
		corresponding to input Mach number using linear interpolation.
		:param M: Mach number
		:return P: Pressure ratio
		:return T: Temperature ratio
		:return A: Area ratio
		"""
		if self.M < 0 or self.M >= 6:
			raise ValueError('Mach number outside valid input domain')
		self.P = np.interp(self.M, M_data, P_data)
		self.T = np.interp(self.M, M_data, T_data)
		self.A = np.interp(self.M, M_data, A_data)
		if self.verbose:
			print(str(self))
	
	def pressure_lookup(self):
		"""
		Returns pressure ratio, temperature ratio, and area ratio
		corresponding to input Mach number using linear interpolation.
		:param M: Mach number
		:return P: Pressure ratio
		:return T: Temperature ratio
		:return A: Area ratio
		"""
		if self.P < 9.746e-4 or self.P > 1:
			raise ValueError('Pressure ratio outside valid input domain')
		self.M = np.interp(self.P, P_data, M_data)
		self.T = np.interp(self.P, P_data, T_data)
		self.A = np.interp(self.P, P_data, A_data)
		if self.verbose:
			print(str(self))
	
	def t2m(self, T):  # 1 output todo verify output, change error range
		"""
		Returns Mach number corresponding to input temperature ratio using linear interpolation.
		:param T: T/T_0 temperature ratio
		"""
		if T < 0 or T >= 6:
			raise ValueError('Temperature ratio outside valid input domain')
		return np.interp(T, T_data, M_data)
	
	def t2p(self, T):  # 1 output todo verify output, change error range
		"""
		Returns pressure ratio corresponding to input temperature ratio using linear interpolation.
		:param T: T/T_0 temperature ratio
		"""
		if T < 0 or T >= 6:
			raise ValueError('Temperature ratio outside valid input domain')
		return np.interp(T, T_data, P_data)
	
	def t2a(self, T):  # 1 output todo verify output, change error range
		"""
		Returns area ratio corresponding to input temperature ratio using linear interpolation.
		:param T: T/T_0 temperature ratio
		"""
		if T < 0 or T >= 6:
			raise ValueError('Temperature ratio outside valid input domain')
		return np.interp(T, T_data, A_data)
	
	def a2m(self, A):  # 2 outputs todo define function, change error range
		"""
		Returns Mach number corresponding to input area ratio using linear interpolation.
		:param A: A/A* area ratio
		"""
		pass
		if A < 0 or A >= 6:
			raise ValueError('Area ratio outside valid input domain')
	
	def a2p(self, A):  # 2 output todo define function, change error range
		"""
		Returns pressure ratio corresponding to input area ratio using linear interpolation.
		:param A: A/A* area ratio
		"""
		pass
		if A < 0 or A >= 6:
			raise ValueError('Area ratio outside valid input domain')
	
	def a2t(self, A):  # 2 outputs todo define function, change error range
		"""
		Returns temperature ratio corresponding to input area ratio using linear interpolation.
		:param A: A/A* area ratio
		"""
		pass
		if A < 0 or A >= 6:
			raise ValueError('Area ratio outside valid input domain')
