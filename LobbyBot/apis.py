from osuauth import AuthClient
import requests

ANIMEQUOTE = "https://animechan.vercel.app/api/random"
OSU = AuthClient().auth()

def getUserData(u):
	return OSU.get(f"https://osu.ppy.sh/api/v2/users/{u}?key=username").json()

def getRandomAnimeQuote():
	return requests.get(ANIMEQUOTE).json()