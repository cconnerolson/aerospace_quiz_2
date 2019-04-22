import numpy as np
import pyromat as pm
import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize

from problem1 import Problem1
import constant as k


class Problem2(object):
	"""Take-home Quiz 2, Problem 2"""
	version = '0.3'
	
	def __init__(self, T3t=k.T3t, T0=k.T0, Pa=k.Pa, delta=0.01, gamma=k.GAMMA, verbose=True):
		self.delta = delta
		self.data = Problem1.empty_data_array(delta)
		self.P1 = Problem1(verbose=False)
		self.SF_P1, self.M0_P1 = self.P1.SF, self.P1.M0
		self.air = pm.get('ig.air')
		self.T3t = T3t
		self.T0 = T0
		self.Pa = Pa
		self.gamma = gamma
		self.verbose = verbose
		self.M0_star = self.equation_A()
		#self.optimize()
		self.M4 = 2.53
		self.A = self.equation_B(self.M4)
		#self.nozzle_area_ratio = self.equation_B()
		self.execute()
	
	def c_p(self):
		"""
		Calculates specific heat of air as a function of temperature and pressure.
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: specific heat [kJ/kg*K]
		"""
		return np.asscalar(self.air.cp(T=self.T3t))
	
	def gamma(self, T):
		"""
		Calculates gamma as a function of temperature.
		:param T: Temperature [K]
		:return: gamma
		"""
		return np.asscalar(self.air.gam(T=T))
	
	def equation_A(self):
		"""
		Calculates (M_0^*)**2
		:return: (M_0^*)**2
		"""
		print(((2 * ((self.T3t / self.T0)**(1 / 3) - 1)) / (self.gamma - 1))**0.5)
		return ((2 * ((self.T3t / self.T0)**(1 / 3) - 1)) / (self.gamma - 1))**0.5
	
	def equation_B(self, M4):
		"""
		Calcualtes nozzle area ratio.
		:return: negative nozzle area ratio, Ae/A*
		"""
		return (1 / M4) * (((1 + (self.gamma - 1) / 2 * M4**2)**((self.gamma + 1) / (2 * (self.gamma - 1)))) / (((self.gamma - 1) / 2 * M4**2)**((self.gamma + 1) / (2 * (self.gamma - 1)))))
	
	def optimize(self):
		self.print_optimization(self.M0_star)
	
	def print_optimization(self, M4):
		A = self.equation_B(M4)
		M0, Tmax = self.loop2(M4)
		print('M4 = {}, Ae/A* = {}, Tmax = {}, M0 = {}'.format(round(M4, 2), round(A, 3), round(Tmax, 1), round(M0, 2)))
	
	def loop2(self, M4):
		data = np.zeros((251, 2))
		data[:,0] = np.arange(1.5, (4 + 0.01), 0.01)
		for idx, row in enumerate(data):
			data[idx, 1] = self.momentum_thrust(M0=(row[0]), M4=M4) + self.pressure_thrust(M0=(row[0]), M4=M4)
		m, tmax = data.max(axis=0)
		mmax, t = data.argmax(axis=0)
		return mmax, tmax
	
	def optimal_nozzle(self, a=2, b=5):
		r = int((4 - 1.5) / 0.1 + 2)
		array = np.zeros((r, 32))
		array[:, 0] = np.arange((1.5 - 0.1), (4 + 0.1), 0.1)
		array[0, :] = np.arange((a - 0.1), (b + 0.1), 0.1)
		array[0, 0] = 0
		for c, M4 in enumerate(array[0, 1:], 1):
			for r, M0 in enumerate(array[1:, 0], 1):
				# print(self.momentum_thrust(M0, M4) + self.pressure_thrust(M0, M4))
				array[r, c] = (self.momentum_thrust(M0, M4) + self.pressure_thrust(M0, M4))
		print(np.unravel_index(np.argmax(array, axis=None), array.shape))
		print('Max = {}'.format(np.amax(array)))
		x = array[:,0]
		y = array[1:, 1:31]
		print(y)
		plt.plot([x] * len(y), y)
		plt.show()
		#self.data = array
	
	def speed_of_sound(self, T=k.T0, R=k.R, gamma=k.GAMMA):
		"""
		Calculates the speed of sound in air at the given ambient pressure.
		:param T: ambient temperature [K]
		:param R: ideal gas constant for air
		:param gamma: specific gravity of air
		:return: speed of sound [m/s]
		"""
		return (self.gamma * R * T)**0.5
	
	def fuel_ratio(self, M0, Qr=k.Qr):
		"""
		Calculates fuel ratio.
		:param M0: mach number at inlet
		:return: f, fuel ratio
		"""
		c_p = self.c_p()
		return (self.T3t - self.T0 * (1 + ((self.gamma - 1) / 2) * M0**2)) / ((Qr / c_p) - self.T3t)
	
	def pressure_continuity(self, M0):
		"""
		Calculates P4 using the pressure continuity equation.
		:return: P4
		"""
		P0 = self.Pa
		return P0 * ((1 + (self.gamma - 1) / 2 * M0**2)**((self.gamma) / (self.gamma - 1)) / (1 + (self.gamma - 1) / 2 * self.M4**2)**((self.gamma) / (self.gamma - 1)))
	
	def momentum_thrust(self, M0):
		"""
		Calculates momentum component of engine thrust.
		:param M0: mach number at inlet
		:return: momentum component of thrust
		"""
		a0 = self.speed_of_sound()
		f = self.fuel_ratio(M0=M0)
		return a0 * M0 * ((1 + f) * (self.M4 / M0) * (self.T3t**0.5 / self.T0**0.5) * (1 / (1 + (self.gamma - 1) / 2 * self.M4**2)**0.5) - 1)
		# return a0 * M0 * ((1 + f) * (M0 / self.Me(M0)) * (k.T3t / (k.T0 * (1 + ((self.gamma - 1) / (2)) * M0**2)))**0.5 - 1)
	
	def pressure_thrust(self, M0):
		"""
		Calculates pressure component of engine thrust.
		:param M0: input mach number
		:return: pressure component of thrust
		"""
		f = self.fuel_ratio(M0=M0)
		P0 = self.Pa
		P4 = self.pressure_continuity(M0)
		return (1 + f) * (P4 / P0 - 1) * self.equation_B(self.M4) * (k.R * self.T3t / self.gamma)**0.5 * (((self.gamma + 1) / 2)**((self.gamma + 1) / (2 * (self.gamma - 1))) / (1 + (self.gamma - 1) / 2 * M0**2)**(self.gamma / (self.gamma - 1)))
	
	def loop(self):
		for idx, row in enumerate(self.data):
			self.data[idx, 1] = self.momentum_thrust(M0=(row[0])) + self.pressure_thrust(M0=(row[0]))
	
	def numpy_to_df(self):
		return pd.DataFrame(self.data, index=np.arange(1.5, (4 + self.delta), self.delta), columns=['M0', 'T/m'])
	
	def maximums(self):
		self.loop()
		df = self.numpy_to_df()
		self.M0, self.SF = df['T/m'].idxmax(), df['T/m'].max()
	
	def plot(self, df):
		x, y = 'M0', 'T/m'
		xmax, ymax = self.M0, self.SF
		df.plot(kind='line', x=x, y=y)
		plt.title('Specific Thrust vs. Mach Number at Input', fontsize=18, y=1.02)
		plt.legend().remove()
		plt.xlabel(r'$M_0$', labelpad=8, fontsize=14)
		plt.xlim(1.3, 4.2)
		plt.ylabel(r'$\frac{T}{\dot{m}}$', rotation=0, labelpad=15, fontsize=18)
		plt.ylim(0, 1200)
		plt.grid()
		plt.tight_layout()
		plt.axvline(x=xmax, linestyle='dashed', color='black', alpha=0.5)
		plt.axhline(y=ymax, linestyle='dashed', color='black', alpha=0.5)
		plt.plot(xmax, ymax, 'ro')
		label = 'Maximum Specific Thrust = {}\nat $M_0$ = {}'.format(round(ymax, 3), round(xmax, 2))
		plt.annotate(label, xy=(2.5, 800), xytext=((xmax + 0.08), (ymax + 70)), bbox=dict(facecolor='white', edgecolor='black', pad=4))
		#plt.savefig(r'plots/p2_plot.png', bbox_inches='tight', dpi=200)
		plt.show()
	
	def execute(self):
		self.loop()
		df = self.numpy_to_df()  # todo get rid of loop call, already called by maximums
		self.maximums()
		if self.verbose:
			self.plot(df)
			df.to_csv(r'data/p2_data.csv')
			print('Ae/A* = {}'.format(round(self.A, 3)))


if __name__ == "__main__":
	p2 = Problem2()
