ops = [
	lambda x: x+1,
	lambda x: x*2
]

C = 0

def rec(n, has15 = False, has31 = False):
	if(n == 35 and has15 and not has31):
		global C
		C += 1
	elif(n == 15): has15 = True
	elif(n == 31): has31 = True
	if(n >= 35): return
	for o in ops:
		rec(o(n), has15, has31)

rec(2)

print(C)