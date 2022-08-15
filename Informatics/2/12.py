S = "8" * 70
while True:
	if("2222" in S): S = S.replace("2222", "88", 1)
	elif("8888" in S): S = S.replace("8888", "22", 1)
	else: break

print(S)