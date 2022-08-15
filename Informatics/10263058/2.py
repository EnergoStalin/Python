from itertools import product

print('x','y','z','w')
a = []
for x,y,z,w in product([0,1], repeat=4):
	if (((z <= w) or (y == w)) and ((x or z) == y)): #??????????????
		a += [[x,y,z,w]]
list(map(print, a[1:-1]))