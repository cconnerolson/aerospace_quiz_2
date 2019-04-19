def diffuser_efficiency(mach):
	"""
	Calculates the efficiency of the diffuser for a RAMJET engine (from problem 3)
	:param mach: M0, Mach No. at inlet
	:return: Πd, diffuser efficiency
	"""
	return 1 - 0.08 * (mach - 1)**1.1