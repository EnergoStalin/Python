AGG = []
for i in range(450000, 100000000):
	DIVS = []
	for d in range(1, i):
		if(i % d == 0):
			DIVS += [d]
	sm = sum(DIVS)
	if(sm != 0 and sm % 7 == 0):
		AGG += [(i, sm)]
		if(len(AGG) == 6): break

print(AGG)