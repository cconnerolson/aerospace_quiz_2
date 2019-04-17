from numpy import *

delta = 0.01

c = int((4 - 1.5) / delta + 1)
array = zeros((c, 2))
array[:, 0] = arange(1.5, (4.0 + delta), delta)

for row in array:
	print(row)