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