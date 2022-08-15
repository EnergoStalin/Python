for n in range(0, 10000000000):
	N = n
	Z = 0
	Y = 0
	while N > 0:
		Z += 1
		if Y < (N % 16):
			Y = N % 16
		N //= 16
	if(Z == 4 and Y == 15):
		print(n)
		break