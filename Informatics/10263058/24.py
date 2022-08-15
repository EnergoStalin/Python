import re

print(max(map(len, re.findall("[^P]+", open("./10263058/24.txt", "r").read()))))