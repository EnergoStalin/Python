import os, json, requests, webbrowser, urllib, datetime
from requestcap import RequestCapture

class AuthClient:
	CREDS = "creds.json"
	TOKEN = "token.json"
	SECRET = "secret.json" #Runtime changes wont saved
	OAUTH = "https://osu.ppy.sh/oauth/authorize"
	TOKENENDPOINT = "https://osu.ppy.sh/oauth/token"

	def __init__(self, creds = dict(), secret = dict()):
		super().__init__()
		self.creds = creds
		self.secret = secret
		self.session = None
		self.token = None

		if(not self.creds):
			self._safeCall(self._loadCreds)
		if(not self.secret):
			self._safeCall(self._loadSecret)

	def auth(self):
		self._getToken()
		self._save()

		if self.session:
			return self.session
		self.session = requests.Session()
		self.session.headers.update({
			"User-Agent": "OsuApi-Python",
			"Authorization": f"{self.token['token_type']} {self.token['access_token']}",
			"Accept": "application/json",
		})
		return self.session

	def _getToken(self):
		try:
			self._loadToken()
		except:
			self._requestOauth()

			resp = requests.post(self.TOKENENDPOINT, data={
				"client_id": self.secret["id"],
				"client_secret": self.secret["secret"],
				"code": self.creds["code"],
				"grant_type": "authorization_code",
				"redirect_uri": self.secret["redirect"]
			}).text

			if("error" in resp.lower()):
				with open("error.html", "w", encoding="utf-8") as f:
					f.write(resp)
				return

			self.token = json.loads(resp)
			self.token["timestamp"] = datetime.datetime.now().timestamp()

	def _requestCode(self):
		oauth = {
			"client_id": self.secret["id"],
			"redirect_uri": self.secret["redirect"],
			"response_type": "code",
			"scope": self.secret["scopes"]
		}

		webbrowser.open(self.OAUTH + "?" + urllib.parse.urlencode(oauth))
		return RequestCapture().request.url.query["code"]

	def _requestOauth(self):
		code = None
		try: self._loadCreds()
		except: code = self._requestCode()
		code = code or self.creds.get("code", None)
			
		if(not code): raise Exception("Premission denied.")

		self.creds.update({
			"code": code,
			"scopes": self.secret["scopes"]
		})

	def _loadToken(self):
		self.token = self._jsonFromFile(self.TOKEN)

		if(not self._checkToken()):
			raise Exception()
		assert(self.token)

	def _checkToken(self):
		return datetime.datetime.fromtimestamp(self.token.get("timestamp", None) or datetime.datetime.now().timestamp()) + datetime.timedelta(seconds=int(self.token["expires_in"])) > datetime.datetime.now()
		
	def _loadCreds(self):
		self.creds = self.creds or self._jsonFromFile(self.CREDS)
		assert(self.creds)

	def _loadSecret(self):
		self.secret = self.secret or self._jsonFromFile(self.SECRET)
		assert(self.secret)

	def _jsonToFile(self, file, jsn):
		with open(file, "w") as f:
			json.dump(jsn, f, indent=4)

	def _jsonFromFile(self, file):
		with open(file, "r") as f:
			return json.load(f)

	def _safeCall(self, func):
		try:
			func()
		except: pass

	def _save(self):
		self._jsonToFile(self.CREDS, self.creds)
		self._jsonToFile(self.TOKEN, self.token)