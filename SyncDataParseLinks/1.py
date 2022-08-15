import csv
import json
import re

def linkFilter(x):
	regex = [
		r".*?kemono.party/.*?/.*?/\d+/post/.*?",
		r".*?pixiv.net/.*?/artworks/.*?",
		r".*?pixiv.net/.*?/artworks/.*?",
		r"https://konachan.com/post/show/.*",
		r"https://anime-pictures.net/pictures/view_post/.*",
		r".*?anime-pictures.net/direct-images/.*",
		r"https://gelbooru.com/index.php?page=post&s=view.*",
		r".*?fanbox.cc/posts/.*"
	]
	for r in regex:
		if(not re.match(r, x) is None):
			return True
	return False

url = r"(https?://(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?)"

with open("sync-data-dump-2022-6-18-1655561196675-Win32.csv", "r", encoding="utf-8") as f:
	data = [m[0] for m in re.findall(url, f.read())]

data = filter(linkFilter, data)

with open("list.txt", "w", encoding="utf-8") as f:
	f.write("\n".join(data))