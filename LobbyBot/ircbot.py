from colls import UserCollection
import json, apis, bottom

class IrcBot:
	def __init__(self, config):
		super().__init__()
		self.config = config
		self.users = UserCollection()
		self.irc = bottom.Client(host=config["host"], host=config["port"])

	def _connect()

	def start(self):
		self.irc.connect()
		print("Connected to bancho.")

		quote = apis.getRandomAnimeQuote()
		room = quote["character"]
		self.irc.mp(f"make {room}")

		while True:
			line = self.irc.line()
			print(line)
			if "PRIVMSG" in line:
				if room in line:
					pass
				elif "BanchoBot" in line:
					if "You cannot create" in line or not self.room_id:
						self.irc.mp("close")
						self.irc.mp(f"make {room}")
			elif "JOIN" in line:
				self.room_id = line.split(":")[-1]
				self.irc.mp("settings")

	def stop(self):
		self.irc.mp("close", self.room_id)
		self.irc.close()