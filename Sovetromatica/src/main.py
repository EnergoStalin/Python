import asyncio
from itertools import chain
import json
import requests, os
from drive import Drive

class Sovetromantica:
	SOVETROMANTICA_URL = "https://service.sovetromantica.com/v1"

	def request(self, path: str, **params):
		url = f"{self.SOVETROMANTICA_URL}/{path}"
		kwargs = {'params': params}
		response = requests.get(url, **kwargs)

		if response.ok:
			return response.json()
		response.raise_for_status()


async def main():
	id = '0B8t03WgYV96bcGtyck5veko1M0E'
	dr = Drive()
	folders = list(chain(*[f async for f in dr.get_folders(id)]))
	with open('.\\folders.json', 'w', encoding='utf-8') as f:
		f.write(json.dumps(folders, indent=4))

if __name__ == "__main__":
	loop = asyncio.new_event_loop()
	try:
		loop.run_until_complete(main())
	except Exception as ex:
		print(ex)
		loop.run_until_complete(loop.shutdown_asyncgens())
		loop.close()
	# sr = Sovetromantica()
	# print(sr.request("anime/1"))