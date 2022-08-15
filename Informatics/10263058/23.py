def alg(n):
	if(n >= 30):
		return int(n == 30)

	return alg(n + 1) + alg(n + 2) + alg(n + 4)

print(alg(21))