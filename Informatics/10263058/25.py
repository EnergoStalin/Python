def delims(num, range):
	for d in range:
		if not(num % d): yield d
	yield 0

def minmaxdel(num):
	m = next(delims(num, range(2, num)))
	return m, 0 if m == 0 else int(num / m)

c = 5
x = 700000
while c > 0:
	s = sum(minmaxdel(x))
	if(str(s)[-1] == '8'):
		print(x, s)
		c -= 1
	x += 1