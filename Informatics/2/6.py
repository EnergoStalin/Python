for i in range(1000000, 0, -1):
	s = i
	s //= 10
	n = 1
	while(s < 51):
		s += 5
		n *= 2
	if(n == 64):
		print(i)
		break