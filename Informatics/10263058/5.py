def pairwise(i):
	it = iter(i)
	return zip(it, it)

for i in range(10000, 0, -1):
	if("".join(map(str, sorted(list(map(lambda x: sum(map(int, x)), pairwise(str(i)))))))) == "1515":
		print(i)
		break