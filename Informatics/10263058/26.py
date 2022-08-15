def todict(dat):
	dct = dict()
	for x in dat:
		dct.setdefault(x[0], [])
		dct[x[0]].append(x[1])

	return dct

with open("./10263058/26.txt", "r") as f:
	rowdata = todict(map(lambda x: list(map(int, x.split())), f.readlines()[1::]))
	mx = []
	for row, data in rowdata.items():
		s = sorted(data)
		for i in range(len(s) - 1):
			if(abs(s[i] - s[i+1]) == 3): # ??? Ого оно работает
				mx.append((row, (min(s[i], s[i+1]) + 1)))
	print(max(mx, key=lambda x: x[0]))