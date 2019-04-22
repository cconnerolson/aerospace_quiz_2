import numpy as np
from problem1 import Problem1
import pyromat as pm

import constant as k


class Problem2(object):
	"""Take-home Quiz 2, Problem 2"""
	version = '0.1'
	
	def __init__(self, delta=0.01):
		self.M0_at_SF_max = 2.34
		self.SF_max = 817.5201699820385
		self.air = pm.get('ig.air')
		self.delta = 0.01
		# self.data = Problem1.empty_data_array(delta)
		self.Ts, self.gs = self.throat_convergence()
		# self.Te, self.ge, self.Me = self.exit_convergence()
		# self.A = self.area_ratio()
		self.check()
	
	def __str__(self):
		string = 's'
		pass
	
	
	def cli_prompt(self):
		print('Options:\n    -r        run script and plot\n    -p        print class attributes')
		action = input(">>> ")
		if action == '-r':
			self.execute()
		elif action == '-':
			self.maximums()
		else:
			raise ValueError('Invalid input.')
	
	
	def empty_data_array(self, delta=0.01):
		"""
		Creates an empty numpy array for the simulation data
		:param delta: spacing between data points
		:return: empty data for data to stored to
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
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: gamma
		"""
		return np.asscalar(self.air.gam(T=T, p=P))
		# c_p = self.c_p(T=T, P=P)
		# c_v = self.c_v(T=T, P=P)
		# return c_p / c_v
	
	def T_from_Tt(self, gamma, Tt, M=1):
		"""
		Calculates T from Tt
		:param gamma: gamma
		:param Tt: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return Tt / (1 + ((gamma - 1) / 2) * M**2)
	
	def Tt_from_T(self, gamma, T, M=1):
		"""
		Calculates Tt from T
		:param gamma: gamma
		:param T: temperature [K]
		:param M: mach number
		:return: Tt [K]
		"""
		return T * (1 + ((gamma - 1) / 2) * M**2)
	
	def throat_convergence(self, T_jj=2000, dT=1, dg=1):
		gamma_jj = self.gamma(T_jj)
		while dT > 0.001 or dg > 0.001:
			T_ii = self.T_from_Tt(gamma_jj, Tt=k.T3t)
			gamma_ii = self.gamma(T_ii)
			dT, dg = abs((T_ii - T_jj) / T_jj), abs((gamma_ii - gamma_jj) / gamma_jj)
			T_jj, gamma_jj = T_ii, gamma_ii
		# print('T* = {}\nGamma* = {}'.format(T_ii, gamma_ii))
		return (T_ii, gamma_ii)
	
	def Te_from_gamma(self, ge, Me):
		Tet = self.Tt_from_T(gamma=self.gs, T=k.T3t, M=1)
		return Tet / (1 + ((ge - 1) / 2) * Me)
	
	def exit_convergence(self, T_jj=2000, dT=1, dg=1, Me=1):
		gamma_jj = self.gamma(T_jj)
		while dT > 0.001 or dg > 0.001:
			T_ii = self.Te_from_gamma(gamma_jj, Me)
			gamma_ii = self.gamma(T_ii)
			dT, dg = abs((T_ii - T_jj) / T_jj), abs((gamma_ii - gamma_jj) / gamma_jj)
			T_jj, gamma_jj = T_ii, gamma_ii
		Me = (self.gs / gamma_jj)**0.5
		return T_ii, gamma_ii, Me
	
	def area_ratio(self):
		a = (self.ge / self.gs)**0.5
		b = (1 / self.Me)
		c = (self.Te / self.Ts)**0.5
		d_num = ((1 + ((self.ge - 1) / 2) * self.Me**2)**((self.ge + 1) / (2 * (self.ge - 1))))
		d_den = (1 + ((self.gs - 1) / 2))**((self.gs + 1) / (2 * (self.gs - 1)))
		A = a * b * c * (d_num / d_den)
		print(A)
		return A
	
	
	def momentum_thrust(self):
		pass
	
	def pressure_thrust(self):
		pass
	
	
	def check(self):
		
		
		
		
		print('\ntest successfully executed')


if __name__ == '__main__':
	p2 = Problem2()

v = (vars(Problem2()))

print(v)