import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyromat as pm

import constant as k


class Problem1(object):
	"""Take-home Quiz 2, Problem 1"""
	version = '1.1'
	
	def __init__(self, T3t=2000, T0t=223, Pa=16.5, delta=0.01, ST=0):
		self.T3t = T3t  # [K]
		self.T0t = T0t  # [K]
		self.Pa = Pa  # [K]
		self.air = pm.get('ig.air')
		self.delta = delta
		self.data = Problem1.empty_data_array(delta)
		self.cli_prompt()
	
	def cli_prompt(self):
		print('Options:\n    -r        run script\n    -m        return maximum specific thrust and mach number')
		action = input(">>> ")
		if action == '-r':
			self.execute()
		elif action == '-m':
			self.maximums()
		else:
			raise ValueError('Invalid input.')
	
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
		Calculates specific heat of air as a function of temperature and pressure.
		:param T: Temperature [K]
		:param P: Pressure [kPa]
		:return: specific heat [kJ/kg*K]
		"""
		return np.asscalar(self.air.cp(T=T, p=P))
	
	def fuel_ratio(self, mach, T0=k.T0, gamma=k.GAMMA, Qr=k.Qr):
		"""
		Calculates fuel ratio
		:param mach:
		:return: f, fuel ratio
		"""
		c_p = self.c_p(T=self.T3t, P=self.Pa)
		return (self.T3t - T0 * (1 + ((gamma - 1) / 2) * mach**2)) / ((Qr / c_p) - self.T3t)
	
	def speed_of_sound(self, T=k.T0, R=k.R, gamma=k.GAMMA):
		"""
		Calculates the speed of sound in air at the given ambient pressure.
		:param T: ambient temperature [K]
		:param R: ideal gas constant for air
		:param gamma: specific gravity of air
		:return: speed of sound [m/s]
		"""
		return (gamma * R * T)**0.5
	
	def ideal_thrust(self, M0, gamma=1.4):
		"""
		Calculate ideal thrust as a function of Mach number.
		:param gamma: specific gravity of air
		:param T3t:
		:param T0t:
		:return: thrust
		"""
		a0 = self.speed_of_sound()
		f = self.fuel_ratio(mach=M0)
		return a0 * M0 * ((1 + f) * (self.T3t / (self.T0t * (1 + ((gamma - 1) / (2)) * M0**2)))**0.5 - 1)
	
	def loop(self):
		for idx, row in enumerate(self.data):
			self.data[idx, 1] = self.ideal_thrust(M0=(row[0]))
	
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
		plt.ylim(580, 880)
		plt.grid()
		plt.tight_layout()
		plt.axvline(x=xmax, linestyle='dashed', color='black', alpha=0.5)
		plt.axhline(y=ymax, linestyle='dashed', color='black', alpha=0.5)
		plt.plot(xmax, ymax, 'ro')
		label = 'Maximum Specific Thrust =' + str(round(ymax, 2)) + '\nat $M_0$ =' + str(round(xmax, 2))
		plt.annotate(label, xy=(2.5, 800), xytext=((xmax + 0.08), (ymax + 18)), bbox=dict(facecolor='white', edgecolor='black', pad=4))
		plt.savefig(r'plots/p1_plot.png', bbox_inches='tight', dpi=200)
		plt.show()
	
	def execute(self):
		self.loop()
		df = self.numpy_to_df()
		self.plot(df)
		df.to_csv(r'data/p1_data.csv')
	
	def maximums(self):
		self.loop()
		df = self.numpy_to_df()
		M0, SF = round(df['T/m'].idxmax(), 2), round(df['T/m'].max(), 4)
		print('Maximum Specific Thrust = {}\nOccuring at M0 = {}'.format(SF, M0))
		return SF, M0

if __name__ == '__main__':
	Problem1()
