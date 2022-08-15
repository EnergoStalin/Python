from itertools import product

def pairs(it): return [(it[i-1], it[i]) for i in range(1, len(it))]

nums = None
with open(r"./Доп. файлы/Задание 17/17.txt", encoding="utf-8") as f:
	nums = list(map(int, f.readlines()))

mx = max(list(filter(lambda x: not x % 3, nums)))
pair = list(filter(lambda x: ((not x[0] % 3 or not x[1] % 3) and sum(x) < mx),
	pairs(nums)))
print(len(pair), max(map(sum, pair)))


