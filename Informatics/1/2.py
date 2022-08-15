def impl(a,b):
	return not(a) and b

print("x w y z")
for x in range(2):
	for w in range(2):
		for y in range(2):
			for z in range(2):
				if not((y<=x) or not((x<=z) and (z<=x)) and not(w)):
					print(x,w,y,z)
