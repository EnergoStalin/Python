def f(x, p = 0):
	if x >= 28 or p > 4:
		return p == 4
	if p % 2:
		return f(x + 1, p + 1) or f(x * 2, p + 1)
	else:
		return f(x + 1, p + 1) and f(x * 2, p + 1)

for x in range(1, 29):
	if f(x):
		print(x)