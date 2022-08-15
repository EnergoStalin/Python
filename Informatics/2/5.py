def F(N):
	bn = bin(N)[2:]
	return f"{bn}{sum(map(int, bn)) % 2}"

for N in range(0,10000):
	if(int(F(int(F(N), 2)),2) > 77):
		print(N)
		break