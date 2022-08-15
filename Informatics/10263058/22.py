for i in range(1000, 0, -1):
	x = i
	a=0; b=0
	while x>0:
		a = a+1
		if x%2==0:
			b += x%10
		x = x//10
	if(a == 3 and b == 12):
		print(i)
		break