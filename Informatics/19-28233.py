def f(x, p = 0):
	if(x >= 65 or p > 2):
		return p == 2
	
	if(p % 2 == 0):
		return f(x+1, p+1) and f(x*3, p+1)
	else:
		return f(x+1, p+1) or f(x*3, p+1)

for x in range(1, 67):
	if(f(x)):
		print(x)
	
