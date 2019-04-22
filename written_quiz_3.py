import constant as k

class Functions(object):
	"""Written Take-home Quiz 3 Function Toolkit"""
	version = '0.1'
	
	def __init__(self, P=0, Pt=0, T=0, Tt=0):
		self.P = P
		self.Pt = Pt
		self.T = T
		self.Tt = Tt
		self.gamma = k.GAMMA
	
	@classmethod
	def speed_of_sound(self, T=k.T0, R=k.R, gamma=1.4):
		"""
		Calculates the speed of sound in air at the given ambient pressure.
		:param T: ambient temperature [K]
		:param R: ideal gas constant for air
		:param gamma: specific gravity of air
		:return: speed of sound [m/s]
		"""
		return (gamma * R * T)**0.5
	
	@classmethod
	def Tt_2_T(cls, Tt, M, gamma=1.4):
		"""
		Calculates T from Tt
		:param gamma: gamma
		:param Tt: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return Tt / (1 + ((gamma - 1) / 2) * M**2)
	
	@classmethod
	def T_2_Tt(cls, T, M, gamma=1.4):
		"""
		Calculates Tt from T.
		:param gamma: gamma
		:param T: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return T * (1 + ((gamma - 1) / 2) * M**2)
	
	def Pt_2_P(self, Pt, M, gamma=1.4):
		"""
		Calculates PT from P.
		:param gamma: gamma
		:param Pt: temperature [K]
		:param M: mach number
		:return: T [K]
		"""
		return Pt / (1 + ((gamma - 1) / 2) * M**2)**(gamma / (gamma - 1))
	
	def P_2_Pt(self, P, M, gamma=1.4):
		"""
		Calculates P from Pt.
		:param gamma: gamma
		:param P: temperature [K]
		:param M: mach number
		:return: P
		[K]
		"""
		return P * (1 + ((gamma - 1) / 2) * M**2)**(gamma / (gamma - 1))
	



if __name__ == "__main__":
	fn = Functions()
	