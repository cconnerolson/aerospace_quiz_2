from numpy import zeros, arange
import pandas as pd
import matplotlib.pyplot as plt
import constant as k
import given as g


class Problem1(object):
	"""Take-home Quiz 2, Problem 1"""
	version = '1.0'
	
	def __init__(self, T3t=2000, T0t=223, Pa=16.5, delta=0.01):
		self.T3t = T3t  # [K]
		self.T0t = T0t  # [K]
		self.Pa = Pa  # [K]
		self.delta = delta
		self.data = Problem1.empty_data_array(delta)
		self.execute()
	
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
	
	@classmethod
	def schomate(cls, T, output='c_p'):
		"""
		Shchomate equation to calculate specific heat of water vapor for a given temperature T.
		:param T: Temperature [K]
		:param output: specify return value
		:return g: gamma, specific gravity [J/mol*K]
			:return c_p: specific heat capacity at constant pressure
		"""
		t = T / 1000
		if 500 <= T < 1700:
			a, b, c, d, e = [30.092, 6.832514, 6.793425, -2.53448, 0.082139]
		elif T == 1700:
			return 2.7175
		elif 1700 < T <= 6000:
			a, b, c, d, e = [41.96426, 8.622053, -1.49978, 0.098119, -11.1576]
		else:
			raise ValueError('Input temperature outside valid domain')
		c_p = (a + (b * t) + (c * t**2) + (d * t**3) + (e / t**2)) / 18
		R = 0.4615
		c_v = c_p - R
		g = c_p / c_v
		if output == 'gamma':
			return g
		elif output == 'c_p':
			return c_p
		else:
			raise ValueError('incorrect output selection argument given.')
	
	def fuel_ratio(self, mach, T0=g.T0, gamma=k.GAMMA, Qr=g.Qr):
		"""
		Calculates fuel ratio
		:param mach:
		:return: f, fuel ratio
		"""
		c_p = Problem1.schomate(self.T3t)
		return (self.T3t - T0 * (1 + ((gamma - 1) / 2) * mach**2)) / ((Qr / c_p) - self.T3t)
	
	def speed_of_sound(T=g.T0, R=k.R, gamma=k.GAMMA):
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
		a0 = Problem1.speed_of_sound()
		f = Problem1.fuel_ratio(self, mach=M0)
		return a0 * M0 * ((1 + f) * (self.T3t / (self.T0t * (1 + ((gamma - 1) / (2)) * M0**2)))**0.5 - 1)
	
	def loop(self):
		for idx, row in enumerate(self.data):
			self.data[idx, 1] = Problem1.ideal_thrust(self, M0=(row[0]))
	
	def numpy_to_df(self):
		return pd.DataFrame(self.data, index=arange(1.5, (4 + self.delta), self.delta), columns=['M0', 'T/m'])
	
	def plot(self, df):
		x, y = 'M0', 'T/m'
		xmax, ymax = df['T/m'].idxmax(), df['T/m'].max()
		# print(xmax, ymax)
		df.plot(kind='line', x=x, y=y)
		plt.title('Specific Thrust vs. Mach Number at Input', fontsize=18, y=1.02)
		plt.legend().remove()
		plt.xlabel(r'$M_0$', labelpad=10, fontsize=14)
		plt.xlim(1.4, 4.1)
		plt.ylabel(r'$\frac{T}{\dot{m}}$', rotation=0, labelpad=15, fontsize=18)
		plt.ylim(675, 975)
		plt.grid()
		plt.tight_layout()
		plt.axvline(x=xmax, linestyle='dashed', color='black', alpha=0.5)
		plt.axhline(y=ymax, linestyle='dashed', color='black', alpha=0.5)
		plt.plot(xmax, ymax, 'ro')
		label = 'Maximum Specific Thrust:\n (' + str(round(xmax,2)) + ', ' + str(round(ymax,2)) + ')'
		plt.annotate(label, xy=(2.5, 800), xytext=((xmax + 0.07), (ymax + 15)), bbox=dict(facecolor='white', edgecolor='black', pad=4))
		plt.savefig(r'plots/p1_plot.png', bbox_inches='tight', dpi=200)
		plt.show()
	
	def execute(self):
		Problem1.loop(self)
		df = Problem1.numpy_to_df(self)
		Problem1.plot(self, df)
		df.to_csv(r'data/p1_data.csv')


Problem1()

