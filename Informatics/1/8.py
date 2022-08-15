from itertools import permutations

DCT = "ABCDEFG"
print(len(list(filter(lambda x: x[0] == "A" and not "BGF" in "".join(x), permutations(DCT, r=4)))))

C = 0
for a in DCT:
	for b in filter(lambda x: x != a, DCT):
		for c in filter(lambda x: not x in [a, b], DCT):
			for d in filter(lambda x: not x in [a, b, c], DCT):
				s = "".join([a,b,c,d])
				if("A" != s[0] or "BGF" in s): continue
				C += 1
print(C)