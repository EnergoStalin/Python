from itertools import product

def pair(it):
	for i in range(len(it) - 1):
		for k in range(i + 1, len(it)):
			yield (it[i], it[k])

data = list(map(int, open("./10263058/17.txt").readlines()))
res = list(filter(lambda x: not(x % 60), map(lambda x: abs(x[0] - x[1]), pair(data))))
print(len(res), max(res))

#832722 9960