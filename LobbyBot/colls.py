class UserCollection:
	def __init__(self):
		super().__init__()
		self._users = []

	def get(self, param):
		return next(filter(self._users, lambda e: e["username"] == param or (e["id"] == param and isinstance(param, int))))

	def getId(self, param):
		return self._users.index(self.get(param))

	def add(self, user):
		self._users.append(user)

	def remove(self, user):
		self._users.remove(self.getId(user))
