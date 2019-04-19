import numpy as np
from problem1 import Problem1
import pyromat as pm

import constant as k


class Problem2(object):
	"""Take-home Quiz 2, Problem 2"""
	version = '1.0'
	
	def __init__(self, delta=0.01):
		self.M0_at_SF_max = 2.34
		self.SF_max = 817.5201699820385
		self.air = pm.get('ig.air')
		self.delta = 0.01
		self.data = Problem1.empty_data_array(delta)
		self.check()
	
	def empty_data_array(self, delta=0.01):
		"""
		Creates an empty numpy array for the simulation data
		:param delta: spacing between data points
		:return:
		"""
		c = int((4 - 1.5) / delta + 1)
		array = np.zeros((c, 2))
		array[:, 0] = np.arange(1.5, (4 + delta), delta)
		return array
	
	def c_p(self, T=k.T0, P=k.Pa):
		"""
		Calculates isobaric specific heat of air as a function of temperature and pressure.
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: specific heat [kJ/kg*K]
		"""
		return np.asscalar(self.air.cp(T=T, p=P))
	
	def c_v(self, T=k.T0, P=k.Pa):
		"""
		Calculates isochoric specific heat of air at as a function of temperature and pressure.
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: specific heat [kJ/kg*K]
		"""
		return np.asscalar(self.air.cv(T=T, p=P))
	
	def gamma(self, T, P=k.Pa):
		"""
		Calculates gamma as a function of isobaric and isochoric heat capacity.
		:param T:
		:param P:
		:return:
		"""
		c_p = self.c_p(T=T, P=P)
		c_v = self.c_v(T=T, P=P)
		return c_p / c_v
	
	def t_ratio(self, gamma, T3t=k.T3t):
		"""
		Calculates T as a function of gamma
		:return:
		"""
		return T3t / (1 + (gamma - 1) / 2)
	
	def throat_convergence(self, Tjj, dT, dg):
		
		
		pass
	
	@staticmethod
	def check():
		print('test executed')


if __name__ == '__main__':
	Problem2()

