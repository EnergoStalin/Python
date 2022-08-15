for x in range(0,10000000):
	sm1 = sum(map(int, filter(lambda e: int(e) % 2 == 0, str(x))))
	sm2 = sum(map(int, [t[1] for t in filter(lambda e: e[0] % 2 == 0, enumerate(str(x)))]))
	if(abs(sm1-sm2) == 13):
		print(x)
		break