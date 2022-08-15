import json, os, re, requests
from bs4 import BeautifulSoup
import model

class Match:
	def __init__(self, link):
		super().__init__()
		self.LINKS: str = [link]
		self.IDS: str = [self.getIdFromLink(link)]
		self.users: model.User = {}
		self.maps: model.Beatmap = {}
		self.games: list[model.Game] = []

		if(not os.path.exists(self.getCacheFileName())):
			self.fetchData()
			self.saveData()
		else:
			self.loadData()
		self.parseData()

	# Common
	def getIdFromLink(self, lnk):
		return re.findall("https://osu.ppy.sh/community/matches/(\d+)", lnk)[0]

	def fetchData(self):
		soup = BeautifulSoup(requests.get(self.LINKS[0]).text, "html.parser")
		self.rawData = json.loads(soup.find("script", id="json-events").contents[0])

	def parseData(self):
		# Saving users by keys
		for user in self.rawData["users"]:
			self.users[user["username"]] = user

		for event in self.rawData["events"]:
			# Check it is game event or not
			if(event["detail"]["type"] == "other"):
				# Save data about game
				self.games.append(event["game"])

				game = self.games[-1]

				# Save scores from map
				for score in game["scores"]:
					if score["id"] in [sc["id"] for sc in game["scores"]]:
						scores = self.maps.setdefault(game["beatmap"]["id"], [])
						users_played_map = list(map(lambda v: v["user_id"], scores))
						scores += filter(lambda sc: not sc["user_id"] in users_played_map, game["scores"])

	def makeList(self):
		toplist = [
			# Map array
				# title
				# bmsetId
				# id
				# Users by username as "scores"
					# Stats by stats of course
		]

		for id, scores in self.maps.items():
			bm = self.getBeatmapById(id)
			bmset = bm["beatmapset"]
			users = {}
			toplist.append({
				"title": f"{bmset['artist']} - {bmset['title']}",
				"bmsetId": bmset["id"],
				"id": id,
				"scores": users
			})
			for score in scores:
				username = self.getUserById(score["user_id"])["username"]
				stats = {
					"score": score["score"],
					"hits": score["statistics"],
					"accuracy_raw": score["accuracy"],
					"accuracy_normalized": round(score["accuracy"] * 100, 2),
					"max_combo": score["max_combo"],
					"mods": "".join(score["mods"])
				}
				users[username] = stats
		return toplist
	
	def writeList(self, maps, f):
		header = [
			"Player",
			"Mods",
			"Score",
			"Accuracy",
			"Hits",
			"Max Combo"
		]

		#Write maps
		for m in maps:
			f.write(f"{m['title']} ({m['id']}) {','*len(header)},")

		f.write("\n")

		#Write headers
		for i in range(0,len(maps)):
			f.write(",".join(header) + ",,")

		f.write("\n")

		# Write scores
		while(True):
			res = []
			for m in maps: #Write scores on one line for each map
				idx = m.setdefault("score_idx", 0)
				users = list(m["scores"].keys()) #Get users list
				users_count = len(users) #Save user list length
				if(idx >= users_count):
					f.write(","*7)
					res.append(1)
					continue
				user = users[idx] #Get username from list as key
				score = m["scores"][user] #Get user socore on map
				f.write(f'''\
					{user},\
					{score["mods"]},\
					{score["score"]},\
					{score["accuracy_normalized"]},\
					{score["hits"]["count_50"]}|{score["hits"]["count_100"]}|{score["hits"]["count_300"]}|{score["hits"]["count_miss"]},\
					{score["max_combo"]},,\
				'''.replace("\t", "")) # Write user data to csv
				m["score_idx"] = idx + 1
				res.append(0)
			f.write("\n") # Write \n before new score line
			if(all(res)): break

	# Data caching
	def getCacheFileName(self):
		return os.path.join("Cache", f"{'-'.join(self.IDS)}.json")

	def loadData(self):
		with open(self.getCacheFileName(), "r", encoding="utf-8") as f:
			self.rawData = json.load(f)

	def saveData(self):
		if not os.path.exists("Cache"):
			os.mkdir("Cache")

		with open(self.getCacheFileName(), "w", encoding="utf-8") as f:
			json.dump(self.rawData, f)

	# Interface methods
	def getUserById(self, id: int):
		return next(filter(lambda x: x["id"] == id, self.users.values()))

	def getBeatmapById(self, id: int):
		return next(filter(lambda x: x["beatmap"]["id"] == id, self.games))["beatmap"]

	def join(self, mm) -> None:
		'''
			Joining matchs togeter picking only one score per map for each player
		'''
		self.IDS += mm.IDS
		self.LINKS += mm.LINKS
		self.games += mm.games

		self.users.update(mm.users)

		# Merge scores in map
		for id, scores in mm.maps.items():
			fscores = self.maps.setdefault(id, [])
			users_played_map = list(map(lambda v: v["user_id"], self.maps[id]))
			fscores += filter(lambda v: not v["user_id"] in users_played_map, scores)