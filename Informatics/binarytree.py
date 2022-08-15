class Node:
	def __init__(self, value, left: 'Node' = None, right: 'Node' = None) -> None:
		self._left = left
		self._right = right
		self.value = value

	def __iter__(self):
		if self._left:
			for x in self._left:
				yield x

		yield self.value
		
		if self._right:
			for x in self._right:
				yield x
		

node = Node(15, Node(10, Node(46)), Node(6, Node(15, Node(10, Node(46)), Node(6)), Node(15, Node(10, Node(46)), Node(6))))

for val in node:
	print(val)