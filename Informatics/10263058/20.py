def f(x, p = 0):
	if(x >= 64 or p > 3):
		return p == 3

	return f(x + 1 , p + 1) or f(x * 3 , p + 1) if (p % 2 == 0) else f(x + 1 , p + 1) and f(x * 3 , p + 1)

for x in range(1, 65):
	if(f(x)):
		print(x)