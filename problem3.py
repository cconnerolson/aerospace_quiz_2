import numpy  as np
import pyromat as pm
import pandas as pd
import matplotlib.pyplot as plt

from problem1 import Problem1
from problem2 import Problem2
import constant as k


class Problem3(object):
	"""Take-home Quiz 2, Problem 3"""
	version = '0.1'
	
	def __init__(self, T3t=k.T3t, T0=k.T0, Pa=k.Pa, delta=0.01, verbose=True):
		self.delta = delta
		self.data = Problem1.empty_data_array(delta)
		self.T3t = T3t
		self.T0 = T0
		self.Pa = Pa
		self.verbose = verbose
		self.P2 = Problem2()
	
	def diffuser_efficiency(self, M0):
		"""
		Calculates the efficiency of the diffuser for a RAMJET engine (from problem 3)
		:param M0: M0, Mach No. at inlet
		:return: Πd, diffuser efficiency
		"""
		return 1 - 0.08 * (M0 - 1)**1.1
	
	