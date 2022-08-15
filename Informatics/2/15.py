from re import A


D = list(range(17, 59))
C = list(range(29, 81))
A = []

for x in range(0, 100):
	if not((x in D) <= ((not(x in C) and not(x in A)) <= (not(x in D)))):
		A.append(x)
print(abs(A[0] - A[-1]), len(A))
		