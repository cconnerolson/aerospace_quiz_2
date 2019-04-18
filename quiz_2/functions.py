import numpy as np
import constant as k
import given as g
import math

# General

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


def generate_data_array(problem):
	if problem == 1:
		p1_data = np.zeros((251, 2))
		p1_data[:, 0] = np.linspace(1.5, 4.0, 251)
		return p1_data
	elif problem == 2:
		return [2]
	elif problem == 3:
		return [3]
	elif problem == 4:
		return [4]
	else:
		raise ValueError('invalid input')

# Problem 1

def fuel_ratio(mach, T3t=g.T3t, T0=g.T0, gamma=k.GAMMA, Qr=g.Qr):
	"""
	Calculates fuel ratio
	:param mach:
	:return: f, fuel ratio
	"""
	c_p = schomate(T3t, output='c_p')
	return (T3t - T0 * (1 + ((gamma - 1) / 2) * mach**2)) / ((Qr / c_p) - T3t)


def speed_of_sound(T = g.T0, R=k.R, gamma=k.GAMMA):
	"""
	Calculates the speed of sound in air at the given ambient pressure.
	:param T: ambient temperature [K]
	:param R: ideal gas constant for air
	:param gamma: specific gravity of air
	:return: speed of sound [m/s]
	"""
	return math.sqrt(gamma * R * T)


