from itertools import product


for k, i in product(range(1,1000), repeat=2):
	s = i
	x = k
	s = 100*s + x
	n = 1
	while s < 2021:
		s = s + 5*n
		n = n + 1
	if( n == 17):
		print(i, k)
		break

