def f(x, p = 1):
	if x >= 28 or p > 3:
		return p == 3

	if p % 2 == 0:
		return f(x + 1, p + 1) or f(x * 2, p + 1)	#PETYA
	else:
		return f(x + 1, p + 1) and f(x * 2, p + 1)	#VANYA

for x in range(1, 29):
	if f(x):
		print(x)