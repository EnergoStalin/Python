import datetime
import json
import webbrowser

import requests

class Token:
	options = {
		"client_id": 5718,
		"redirect_uri": "https://anilist.co/api/v2/oauth/pin",
		"client_secret": "lhQ3ysYE2sk9548Z9jEOR1UVJD9HayydmNo1diTr"
	}
	file = "token.tk"
	cached = None

	def CheckTimestamp(self, res):
		return not(
			int(datetime.datetime.now().timestamp()) - int(res["timestamp"]) > int(res["expires_in"])
		)

	def _GetToken(self):
		url = f"https://anilist.co/api/v2/oauth/authorize?client_id={self.options['client_id']}&redirect_uri={self.options['redirect_uri']}&response_type=code"
		webbrowser.open_new_tab(url)
		access = input("Paste Token Here: ")

		return requests.post('https://anilist.co/api/v2/oauth/token',
			headers={
				'Content-Type': 'application/json',
				'Accept': 'application/json'
			},
			json={
				'grant_type': 'authorization_code',
				'client_id': self.options["client_id"],
				'client_secret': self.options["client_secret"],
				'redirect_uri': self.options["redirect_uri"], # http://example.com/callback
				'code': access # The Authorization Code received previously
			}
		).json()

	def Load(self):
		if self.cached != None and self.CheckTimestamp(self.cached):
			return self.cached["access_token"]

		with open(self.file, "r") as f:
			res = json.load(f)
			if(self.CheckTimestamp(res)):
				self.cached = res
				return res["access_token"]

	def Save(self, data):
		with open(self.file, "w+") as f:
			json.dump(data,f)

	#Performing oauth authorization and store access token
	def GetToken(self):
		try:
			return self.Load()
		except:
			access = self._GetToken()
			#Setting up timestamp
			access["timestamp"] = datetime.datetime.now().timestamp()

			self.Save(access)

			return access["access_token"]
		
if __name__ == '__main__':
	pass