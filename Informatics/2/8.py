from itertools import product, takewhile

print(list(takewhile(lambda x: x[1][0] != "Л", enumerate(product("ЕЛМРУ", repeat=4))))[-1][0] + 1)