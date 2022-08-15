import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Queries
# q = '0B8t03WgYV96bcGtyck5veko1M0E' in parents and mimeType='application/vnd.google-apps.folder'
# fields = items(id,title,selfLink)

class Drive:
	SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

	def __init__(self: 'Drive', cacheFolder: 'str' = '.'):
		self._cacheFolder = cacheFolder
		self.service = build('drive', 'v2', credentials=self._auth())

	def _auth(self: 'Drive') -> 'Credentials':
		tokenPath = os.path.join(self._cacheFolder, 'token.json')
		credsPath = os.path.join(self._cacheFolder, 'credentials.json')

		creds = None
		# The file token.json stores the user's access and refresh tokens, and is
		# created automatically when the authorization flow completes for the first
		# time.
		if os.path.exists(tokenPath):
			creds = Credentials.from_authorized_user_file(tokenPath, self.SCOPES)
		# If there are no (valid) credentials available, let the user log in.
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
					credsPath, self.SCOPES)
				creds = flow.run_local_server(port=0)
			# Save the credentials for the next run
			with open(tokenPath, 'w') as token:
				token.write(creds.to_json())
		return creds

	async def get_folders(self, root: 'str'):
		page_token = None
		while True:
			res = self.service.files().list(
				q=f"'{root}' in parents and mimeType='application/vnd.google-apps.folder'",
				fields = "nextPageToken, items(id,title,selfLink)",
				pageToken = page_token
			).execute()

			folders = []
			for drive in res.get('items', []):
				folders.append({'title': drive.get('title'), 'id': drive.get('id')})

			page_token = res.get('nextPageToken', None)
			if page_token is None:
				break
			yield folders
	
	async def get_folder(self, root: 'str', itemName: 'str'):
		res = self.service.files().list(
			q=f"'{root}' in parents and mimeType='application/vnd.google-apps.folder' and name='{itemName}'"
		).execute().get('items', [])[0]

		return {'title': res.get('title'), 'id': res.get('id')}