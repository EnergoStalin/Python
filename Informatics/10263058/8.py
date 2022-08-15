from itertools import product, takewhile
print(sum(1 for _ in takewhile(lambda x: x[0] != "С",product(sorted("ПАРУС", key=lambda x: ord(x)), repeat=3))) + 1)