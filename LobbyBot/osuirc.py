from types import SimpleNamespace
from queue import Queue
from socketreader import SocketStreamReader
import socket

class OsuIrc:
	def __init__(self, user, passwd):
		super().__init__()
		self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._reader = SocketStreamReader(self._conn)
		self.user = user
		self.passwd = passwd

	def _readline(self):
		return self._reader.readline().decode()

	def  _sysmsg(self, line):
		if("PING" in line):
			self.send(f"PONG {line.split()[1]}")
			return True
		elif("QUIT" in line): return True
		
		return False

	def connect(self):
		self._conn.connect(("irc.ppy.sh", 6667))
		self._auth()

	def _auth(self):
		self.send(f"PASS {self.passwd}")
		self.send(f"NICK {self.user}")

	def line(self):
		ln = None
		while True:
			ln = self._readline()
			if not self._sysmsg(ln): break
		return ln

	"""Send !mp command to BanchoBot or room if specified"""
	def mp(self, msg, room = None):
		self.pm(f"{room or 'BanchoBot'}", f"!mp {msg}")

	"""Send msg to target"""
	def pm(self, target, msg):
		self.send(f"PRIVMSG {target} :{msg}")

	"""Send raw text line"""
	def send(self, msg: str):
		self._conn.send((msg + "\n").encode())

	def close(self):
		self._conn.close()