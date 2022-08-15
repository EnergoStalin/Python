import asyncio
from aiohttp import web

class RequestCapture:
	def __init__(self):
		super().__init__()
		self.request = None
		self._captured = None

		self._app = web.Application()
		self._app.add_routes([web.get("/", self._localhost)])
		
		self._runner = web.AppRunner(self._app)

		self._synced(self._runner.setup()) #Setup runner
		self._site = web.TCPSite(self._runner, host="127.0.0.1", port=80)

		self._synced([
			self._site.start(), #Start serving site
			self._waitForRequest(), #Wait for first request on localhost
			self._site.stop() #Stop server when request arrives
		])

	#Syncronously run coroutine or list of coroutines
	def _synced(self, awaitable):
		if isinstance(awaitable, list):
			for aw in awaitable:
				asyncio.get_event_loop().run_until_complete(aw)
		else:
			asyncio.get_event_loop().run_until_complete(awaitable)

	async def _waitForRequest(self):
		while not self._captured:
			await asyncio.sleep(1)
		

	async def _localhost(self, request):
		self.request = request
		self._captured = True
		return web.Response(text="Success")