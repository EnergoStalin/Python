from itertools import chain
data = None

with open("./10263058/9_27522.csv", "r") as f:
	f.readline()
	data = f.readlines()

data = map(lambda x: x.split(";")[1::], data)
data = map(lambda x: x.strip('"').replace(",", "."), chain(*data))
data = filter(lambda x: len(x) > 1, data)
data = list(map(float, data))

avg = round(sum(data) / len(data), 1)
print(sum(1 for _ in filter(lambda x: x < avg, data)))