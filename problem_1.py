from main import *
from numpy import zeros, arange

# p1_data = fn.generate_data_array(1)


def ideal_thrust(M0, gamma=k.GAMMA, T3t=g.T3t, T0t=g.T0):
	a0 = fn.speed_of_sound(T=g.T0)
	f = fn.fuel_ratio(mach=M0)
	return a0 * M0 * ((1 + f) * math.sqrt(T3t / (T0t * (1 + ((gamma - 1) / (2)) * M0**2))) - 1)


# ii = 0
# for M, T in p1_data:
#   p1_data[ii, 1] = ideal_thrust(M0=M)
#   ii += 1

# pd.DataFrame(p1_data).to_csv("data/p1_data.csv")


class Problem1(object):
	"""Take-home Quiz 2, Problem 1"""
	version = '0.1'
	
	def __init__(self, T3t=2000, T0t=223, Pa=16.5, delta=0.01):
		self.T3t = T3t  # [K]
		self.T0t = T0t  # [K]
		self.Pa = Pa  # [K]
		self.data = Problem1.empty_data_array(delta)
	
	def empty_data_array(self, delta=0.01):
		"""
		Creates an empty numpy array for the simulation data
		:param delta: spacing between data points
		:return:
		"""
		c = int((4 - 1.5) / delta + 1)
		array = zeros((c, 2))
		array[:, 0] = arange(1.5, (4.0 + delta), delta)
		return array
	
	@classmethod
	def schomate(T, output):
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
		return math.sqrt(gamma * R * T)
	
	def ideal_thrust(self, M0, gamma=1.4):
		"""
		Calculate ideal thrust as a function of Mach number.
		:param gamma: specific gravity of air
		:param T3t:
		:param T0t:
		:return: thrust
		"""
		a0 = fn.speed_of_sound(T=g.T0)
		f = fn.fuel_ratio(mach=M0)
		return a0 * M0 * ((1 + f) * math.sqrt(self.T3t / (self.T0t * (1 + ((gamma - 1) / (2)) * M0**2))) - 1)
	
	def loop(self):
		pass



p1 = Problem1()