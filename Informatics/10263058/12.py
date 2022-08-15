s = "1" * 99

while "111" in s:
	s = s.replace("11","2", 1)
	s = s.replace("22","1", 1)
print(s)