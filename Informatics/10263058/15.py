from itertools import product

for A in range(0, 10000):
	for x in range(0, 10000):
		if not(x&25 != 0) <= ((x&17 == 0) <= (x&A != 0)):
			break
	else:
		print(A)
		break