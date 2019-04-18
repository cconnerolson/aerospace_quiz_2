# Values

Qr = 43_000  # kJ/kg, calorific value of fuel
T0 = 223  # K, inlet temperature
T3t = 2_000  # K, combustion chamber stagnation temperature
Pa = 16.5  # kPa, atmospheric pressure


# Functions

def diffuser_efficiency(mach):
	"""
	Calculates the efficiency of the diffuser for a RAMJET engine (from problem 3)
	:param mach: M0, Mach No. at inlet
	:return: Πd, diffuser efficiency
	"""
	return 1 - 0.08 * (mach - 1)**1.1

