import json

def getAllUsernames(maps):
	_ = []
	for m in maps:
		_ += list(m["scores"].keys())
	return set(_)

def sortScoresBy(maps, by):
	for m in maps:
		m["scores"] = dict(sorted(m["scores"].items(), key=lambda x: x[1][by], reverse=True))

data = None
with open("Top.json") as f:
	data = json.load(f)


users = getAllUsernames(data)
sortScoresBy(data, "score")
useravg = dict(zip(users, [{
	"acc": 0,
	"combo": 0,
	"score": 0,
	"place": 0,
	"maps_played": 0
} for i in range(len(users))]))

for m in data:
	for (i, (user, score)) in enumerate(m["scores"].items()):
		useravg[user]["acc"] += score["accuracy_raw"]
		useravg[user]["combo"] += score["max_combo"]
		useravg[user]["score"] += score["score"]
		useravg[user]["place"] += (i + 1)
		useravg[user]["maps_played"] += 1

for user, score in useravg.items():
	score["acc"] = round(score["acc"] / score["maps_played"], 2)
	score["combo"] = round(score["combo"] / score["maps_played"], 2)
	score["score"] = round(score["score"] / score["maps_played"], 2)
	score["place"] = round(score["place"] / score["maps_played"], 2)

with open("avg.json", "w") as f:
	json.dump(useravg, f, indent=4)

with open("avg.csv", "w") as f:
	f.write("Username,Accuracy,Combo,Score,Place,\n")
	for user, avg in useravg.items():
		f.write(user + ",")
		f.write((",".join(map(str,list(avg.values())[:-1])) + ",\n"))
