import numpy as np
from problem1 import Problem1
import pyromat as pm
import matplotlib.pyplot as plt
import pandas as pd


import constant as k


class Problem2(object):
	"""Take-home Quiz 2, Problem 2"""
	version = '0.1'
	
	def __init__(self, delta=0.01):
		self.data = Problem2.empty_data_array(delta)
		self.SF_ideal, self.M0_ideal = Problem1.return_values()
		# self.M0_at_SF_max = 2.34
		# self.SF_max = 817.5201699820385
		self.air = pm.get('ig.air')
		self.delta = 0.01
		self.g = self.gamma(k.T0)
		self.Ts, self.gs = self.throat_convergence()
		self.Ps = self.pressure_from_temperature()
		self.Te = self.temperature_from_pressure()
		self.Me_id = self.Me_ideal()
		self.A = self.area_ratio()
		self.execute()
		
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
		Calculates specific heat of air as a function of temperature and pressure.
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: specific heat [kJ/kg*K]
		"""
		return np.asscalar(self.air.cp(T=T, p=P))
	
	def gamma(self, T, P=k.Pa):
		"""
		Calculates gamma as a function of temperature and pressure.
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: gamma
		"""
		return np.asscalar(self.air.gam(T=T, p=P))
	
	def T_from_Tt(self, gamma, Tt, M=1):
		"""
		Calculates T from Tt
		:param gamma: gamma
		:param Tt: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return Tt / (1 + ((gamma - 1) / 2) * M**2)
	
	def throat_convergence(self, T_jj=2000, dT=1, dg=1):
		gamma_jj = self.gamma(T_jj)
		while dT > 0.001 or dg > 0.001:
			T_ii = self.T_from_Tt(gamma_jj, Tt=k.T3t)
			gamma_ii = self.gamma(T_ii)
			dT, dg = abs((T_ii - T_jj) / T_jj), abs((gamma_ii - gamma_jj) / gamma_jj)
			T_jj, gamma_jj = T_ii, gamma_ii
		# print('T* = {}\nGamma* = {}'.format(T_ii, gamma_ii))
		return (T_ii, gamma_ii)
	
	def pressure_from_temperature(self):  # for calcuating P*
		rho = np.asscalar(self.air.d(T=self.Ts)) / 1000
		return rho * 287.05 * self.Ts
	
	def temperature_from_pressure(self):
		rho = np.asscalar(self.air.d()) / 1000
		return k.Pa / (rho * 287.05)
	
	def Me(self, M0):
		return ((2 * (((1 + ((self.g - 1) / 2) * M0**2)**(self.g / (self.g - 1)))**((self.gs - 1) / self.gs))) / (self.gs - 1))**0.5
	
	def Me_ideal(self):
		return ((2 * (((1 + ((self.g - 1) / 2) * self.M0_at_SF_max**2)**(self.g / (self.g - 1)))**((self.gs - 1) / self.gs))) / (self.gs - 1))**0.5
	
	def area_ratio(self):
		a = (self.gs / self.gs)**0.5
		b = (1 / self.Me_id)
		c_num = ((1 + ((self.gs - 1) / 2) * self.Me_id**2)**((self.gs + 1) / (2 * (self.gs - 1))))
		c_den = (1 + ((self.gs - 1) / 2))**((self.gs + 1) / (2 * (self.gs - 1)))
		A = a * b * (c_num / c_den)
		return A
	
	def fuel_ratio(self, mach, T0=k.T0, gamma=k.GAMMA, Qr=k.Qr):
		"""
		Calculates fuel ratio.
		:param mach:
		:return: f, fuel ratio
		"""
		c_p = self.c_p(T=k.T3t, P=k.Pa)
		return (k.T3t - T0 * (1 + ((gamma - 1) / 2) * mach**2)) / ((Qr / c_p) - k.T3t)
	
	def speed_of_sound(self, T=k.T0, R=k.R, gamma=k.GAMMA):
		"""
		Calculates the speed of sound in air at the given ambient pressure.
		:param T: ambient temperature [K]
		:param R: ideal gas constant for air
		:param gamma: specific gravity of air
		:return: speed of sound [m/s]
		"""
		return (self.gamma(T) * R * T)**0.5
	
	def momentum_thrust(self, M0):
		"""
		Calculate ideal thrust as a function of Mach number.
		:param M0: mach number at inlet
		:return: momentum component of thrust
		"""
		a0 = self.speed_of_sound()
		f = self.fuel_ratio(mach=M0)
		return a0 * M0 * ((1 + f) * (M0 / self.Me(M0)) * (k.T3t / (k.T0 * (1 + ((self.g - 1) / (2)) * M0**2)))**0.5 - 1)
	
	def pressure_thrust(self):
		
		pass
	
	def loop(self):
		for idx, row in enumerate(self.data):
			self.data[idx, 1] = self.momentum_thrust(M0=(row[0]))
	
	def numpy_to_df(self):
		return pd.DataFrame(self.data, index=np.arange(1.5, (4 + self.delta), self.delta), columns=['M0', 'T/m'])
	
	def plot(self, df):
		x, y = 'M0', 'T/m'
		xmax, ymax = df['T/m'].idxmax(), df['T/m'].max()
		# print(xmax, ymax)
		df.plot(kind='line', x=x, y=y)
		plt.title('Specific Thrust vs. Mach Number at Input', fontsize=18, y=1.02)
		plt.legend().remove()
		plt.xlabel(r'$M_0$', labelpad=8, fontsize=14)
		plt.xlim(1.3, 4.2)
		plt.ylabel(r'$\frac{T}{\dot{m}}$', rotation=0, labelpad=15, fontsize=18)
		plt.ylim(100, 500)
		plt.grid()
		plt.tight_layout()
		plt.axvline(x=xmax, linestyle='dashed', color='black', alpha=0.5)
		plt.axhline(y=ymax, linestyle='dashed', color='black', alpha=0.5)
		plt.plot(xmax, ymax, 'ro')
		label = 'Maximum Specific Thrust =' + str(round(ymax, 2)) + '\nat $M_0$ =' + str(round(xmax, 2))
		plt.annotate(label, xy=(2.5, 800), xytext=((xmax + 0.08), (ymax + 18)), bbox=dict(facecolor='white', edgecolor='black', pad=4))
		plt.savefig(r'plots/p2_plot.png', bbox_inches='tight', dpi=200)
		plt.show()
	
	def execute(self):
		self.loop()
		df = self.numpy_to_df()
		self.plot(df)
		df.to_csv(r'data/p2_data.csv')


if __name__ == '__main__':
	p2 = Problem2()

#print(p2.Me2())


