from ircbot import IrcBot
import json

def LoadConfig():
	with open("irc.json") as f:
		return json.load(f)

ib = IrcBot(LoadConfig())
try:
	ib.start()
except KeyboardInterrupt: pass
finally:
	ib.stop()
	print("Bot stopped.")