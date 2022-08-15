import requests, sys, json, shutil, os
from bs4 import BeautifulSoup

user = sys.argv[1]

soup = BeautifulSoup(requests.get("https://osu.ppy.sh/u/" + user).text, "html.parser")
js = json.loads(soup.find("script", id="json-extras").contents[0])

try: shutil.rmtree(user)
except: pass
os.mkdir(user)

for i in range(0, 6):
	score = js["scoresBest"][i]
	url = score["beatmapset"]["covers"]["cover@2x"]
	sp = os.path.join(user, score["beatmapset"]["title"] + ".jpg") #Allways jpg
	print(url, " -> ", sp)
	with open(sp, "wb") as f:
		for chunk in requests.get(url, stream=True):
			f.write(chunk)