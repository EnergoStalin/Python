class Task:
	'''
		Task interface
	'''
	def solve(self):
		'''
			Should contain all implementation
		'''
		pass
	def test(self, res) -> bool:
		'''
			Method can be used fo running additional tests on solve function result
		'''
		return res != None

class TaskWithFile(Task):
	'''
		Simply it's just a file wrapper
	'''
	def __init__(self, file: str):
		self.fn = file
		self.cache = None
	def readFile(self, cached=False):
		if self.cache != None:
			return self.cache
		data = None
		with open(self.fn,"r") as f:
			data = f.read()
			
		if cached:
			self.cache = data
		return data
	def clearCache(self):
		self.cache = None

class TaskManager:
	'''
		Handling task execution for you
	'''
	def __init__(self):
		self.tasks = []
		self.results = {}
	def clearResults(self):
		self.results = {}
	def clearTasks(self):
		self.tasks = []
	def clear(self):
		self.clearRes()
		self.clearTasks()
	def addTask(self, task: Task):
		self.tasks.append(task)
	def addTasks(self, tasks: list):
		self.tasks += tasks
	def getTypeName(self, task: Task):
		desc = type.__str__(task)
		start = desc.find(".") + 1
		end = desc.find(" ", start)

		return desc[start:end]
	def execute(self) -> dict:
		'''
			Execute tasks and run tests see Task interface for more info
		'''
		for t in self.tasks:
			res = t.solve()
			if t.test(res):
				self.results[self.getTypeName(t)] = res
			else:
				self.results[self.getTypeName(t)] = "Test Failed"
		return self.results
	def load(self, fn: str):
		'''
			Magic method for parsing answers file
			Save reults into results property not overriding existing results
			Format is:
			[task number] # [answer]
		'''
		text = None
		with open(fn, "r") as f:
			text = [i[:-1] for i in f.readlines()]
		
		for l in text:
			if l == "" or l.startswith("#"):
				continue
			center = l.find("#")
			if self.results.get(l[:center].strip(" ")):
				continue
			self.results[l[:center].strip(" ")] = l[center+1:].strip(" ")
		self.results = dict(sorted(self.results.items(), key=lambda k: int(k[0])))
	def export(self, fn: str = "answers.md"):
		try:
			self.load(fn)
		except:
			pass

		with open(fn, "w") as f:
			for k,v in self.results.items():
				f.write(f"{k} # {v}\n")
