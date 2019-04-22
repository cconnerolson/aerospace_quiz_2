import numpy as np
import pyromat as pm
import pandas as pd
import matplotlib.pyplot as plt

import constant as k


class Problem1(object):
	"""Take-home Quiz 2, Problem 1"""
	version = '1.1'
	
	def __init__(self, T3t=k.T3t, T0=k.T0, Pa=k.Pa, delta=0.001):
		self.delta = delta
		self.data = self.create_data_array()
		self.T3t, self.T0, self.Pa = T3t, T0, Pa
		self.P3t = (np.asscalar(self.air.d(T=self.T3t)) / 1000)
		self.air = pm.get('ig.air')
		self.cp0 = np.asscalar(self.air.cp(T=self.T0, p=self.Pa))
	
	def __repr__(self):
		pass
	
	def __str__(self):
		pass
	
	def create_data_array(self):
		"""
		Creates an empty numpy array for the simulation data
		:param delta: spacing between data points
		:return:
		"""
		c = int((4 - 1.5) / self.delta + 1)
		array = np.zeros((c, 2))
		# array[:, 0] = np.arange(1.5, (4 + self.delta), self.delta)
		array[:, 0] = np.linspace(1.5, 4, c)
		print(array)
		return array
	
	def Tt_2_T(self, gamma, Tt, M):
		"""
		Calculates T from Tt
		:param gamma: gamma
		:param Tt: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return Tt / (1 + ((gamma - 1) / 2) * M**2)
	
	def T_2_Tt(self, gamma, T, M):
		"""
		Calculates Tt from T.
		:param gamma: gamma
		:param T: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return T * (1 + ((gamma - 1) / 2) * M**2)
	
	def Pt_2_P(self, gamma, Pt, M):
		"""
		Calculates PT from P.
		:param gamma: gamma
		:param Pt: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		pass
	
	def P_2_Pt(self, gamma, P, M):
		"""
		Calculates P from Pt.
		:param gamma: gamma
		:param P: temperature [K]
		:param M: mach number
		:return: P
		[K]
		"""
		pass
	
	def at_3(self):
		P3t = (np.asscalar(self.air.d(T=self.T3t)) / 1000) * 287.05 * self.T3t
		
		cp3 = np.asscalar(self.air.cp(T=self.T0, p=self.Pa))
		

if __name__ == '__main__':
	Problem1()
