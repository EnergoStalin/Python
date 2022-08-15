from itertools import islice
from Match import Match
import sys, json

def main():
	m = Match(sys.argv[1])
	[m.join(Match(i)) for i in islice(sys.argv, 2, None)]

	list = m.makeList()
	with open("Top.json", "w") as f:
		json.dump(list, f, indent=4)

	with open("Top.csv", "w") as f:
		m.writeList(list, f)

if __name__ == "__main__":
	main()