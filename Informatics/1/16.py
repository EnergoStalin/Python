def A(n, fnct):
	if(n == 1): return n
	elif(n > 1): return fnct(n)

def G(n): return A(n, lambda x: F(n - 1) - 4 * G(n - 1))
def F(n): return A(n, lambda x: F(n - 1) + 2 * G(n - 1))

print(abs(sum(map(int, str(abs(G(10))))) - sum(map(int, str(abs(F(21)))))))