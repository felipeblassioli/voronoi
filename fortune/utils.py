class Node(object):
	def __init__(self, data=None, prev=None, next=None):
		self.data = data
		self.next = next
		self.prev = prev

	def __str__(self):
		return str(self.data)

	def __repr__(self):
		return str(self)

class LinkedList(object):
	def __init__(self):
		self.head = None

	def add(self, data):
		curr = self.head
		if curr is None:
			self.head = Node(data)
			return self.head
		elif curr.data > data:
			self.head = Node(data,next=curr)
			curr.prev = self.head
			return self.head
		else:
			while curr.next is not None:
				if curr.next.data > data:
					break
				curr = curr.next
			new_node = Node(data,next=curr.next,prev=curr)
			if curr.next is not None:
				curr.next.prev = new_node
			curr.next = new_node
			return new_node

	def __iter__(self):
		curr = self.head
		while curr is not None:
			yield curr
			curr = curr.next
		
	def __str__(self):
		data = []
		curr = self.head
		while curr is not None:
			data.append(curr.data)
			curr = curr.next
		return "[%s]" %(', '.join(str(i) for i in data))

	def __repr__(self):
		return self.__str__()

def out(start_node):
	# if start_node == None:
	# 	start_node = self.root
	print 'start', start_node
	space_symbol = "-"
	spaces_count = 140
	out_string = ""
	initial_spaces_string  = space_symbol * spaces_count + "\n" 
	if not start_node:
		return "AVLTree is empty"
	else:
		level = [start_node]
		while (len([i for i in level if (not i is None)])>0):
			level_string = initial_spaces_string
			for i in xrange(len(level)):
				j = (i+1)* spaces_count / (len(level)+1)
				level_string = level_string[:j] + (str(level[i]) if level[i] else space_symbol) + level_string[j+1:]
			level_next = []
			for i in level:
				level_next += ([i.left, i.right] if i else [None, None])
			level = level_next
			out_string += level_string                    
	return out_string

class BinarySearchTree(object):
	def __init__(self):
		self._root = None

	def minimum(self, x):
		# Cormen 3ed p291
		while x.left is not None:
			x = x.left
		return x

	def maximum(self, x):
		# Cormen 3ed p291
		while x.right is not None:
			x = x.right
		return x

	def predecessor(self,x):
		"""
		Given a node
		If all keys are distinct, the sucessor of a node x is the node with the smallest key greater than x.key
		"""

		# Cormen 3ed p292
		if x.left is not None:
			return self.maximum(x.left)
		y = x.parent
		while y is not None and x == y.left:
			x = y
			y = y.parent
		return y

	def sucessor(self,x):
		# Cormen 3ed p292
		if x.right is not None:
			return self.minimum(x.right)
		y = x.parent
		while y is not None and x == y.right:
			x = y
			y = y.parent
		return y

	def dumps(self):
		return out(self._root)

	@property
	def is_empty(self):
		return self._root is None

	def __iter__(self):
		nodes = []
		def _traverse(node):
			if node.left is not None:
				_traverse(node.left)
			nodes.append(node)
			if node.right is not None:
				_traverse(node.right)
		if self._root:
			_traverse(self._root)
			for n in nodes:
				yield n
		else:
			raise Exception('Tree is_empty')

	def __str__(self):
		return ' '.join([ str(x) for x in self ])

from random import randint
if __name__ == '__main__':
	l = LinkedList()
	for i in range(1,10):
		n = randint(1,100)
		print 'add', n
		l.add(n)

	print 'List:'
	for x in l:
		print x

	print l

	l = LinkedList()
	print str(l)