# -*- coding: utf-8 -*-

class Arc(object):
	def __init__(self, point=None):
		self.point = point
		# The node in the event queue that represents the circle event in which this event will disappear
		self.circle_event = None

	def __str__(self):
		return "Arc(point=[{}])".format(self.point)

class BeachLine(object):
	"""
	Beach line: The beach line is represented using a dictionary
	(e.g. a balanced binary tree or skip list). An important fact of the
	construction is that we do not explicitly store the parabolic
	arcs. They are just their for the purposes of deriving the
	algorithm. Instead for each parabolic arc on the current beach line,
	we store the site that gives rise to this arc. Notice that a site may
	appear multiple times on the beach line (in fact linearly many times
	in n). But the total length of the beach line will never exceed 2n-1.

	Between each consecutive pair of sites pi and
	pj, there is a breakpoint. Although the breakpoint moves as
	a function of the sweep line, observe that it is possible to compute
	the exact location of the breakpoint as a function of pi,
	pj, and the current y coordinate of the sweep line. Thus,
	as with beach lines, we do not explicitly store breakpoints. Rather,
	we compute them only when we need them.

	The important operations that we will have to support on the beach line are

	(1) Given a fixed location of the sweep line, determine the arc of the
	beach line that intersects a given vertical line. This can be done by
	a binary search on the breakpoints, which are computed ``on the
	fly''. (Think about this.)

	(2) Compute predecessors and successors on the beach line.

	(3) Insert an new arc pi within a given arc pj,
	thus splitting the arc for pj into two. This creates three
	arcs, pj, pi, and pj.

	(4) Delete an arc from the beach line.

	It is not difficult to modify a standard dictionary data structure to
	perform these opera tions in O(log n) time each.
	"""

	def search(self, p):
		"""Given a fixed location of the sweep line, determine the arc of the
		beach line that intersects a given vertical line.
		"""
		raise NotImplementedError()

	def predecessor(self,arc):
		"""
		Given a node
		If all keys are distinct, the sucessor of a node x is the node with the smallest key greater than x.key
		"""
		raise NotImplementedError()

	def sucessor(self,arc):
		raise NotImplementedError()

	def delete(self, arc):
		raise NotImplementedError()

	def insert(self, p, within=None):
		"""Insert an new arc pi within a given arc pj,
		thus splitting the arc for pj into two. This creates three
		arcs, pj, pi, and pj.
		"""
		raise NotImplementedError()

	@property
	def is_empty(self):
		raise NotImplementedError()



def intersect(p, node):
	"""Will a new parabola at point p intersect with arc at node?"""
	#print 'intersect', p, node
	if node.prev:
		a = intersection(node.prev.data.point, node.data.point, p[Y])[X]
		#print '\ta', a
	if node.next:
		b = intersection(node.data.point, node.next.data.point, p[Y])[X]
		#print '\tb', b
	if (not node.prev or a <= p[X]) and (not node.next or p[X] <= b):
		return True
	return False

from .geometry import X,Y,intersection
from .utils import LinkedList, Node as LLNode
class Node(LLNode):
	def __init__(self,data,next=None,prev=None):
		self.__dict__.update(data.__dict__.copy())
		super(Node,self).__init__(data,prev,next)

	def __str__(self):
		return "Node(point=[{}]) at {}".format(self.point,hex(id(self)))

	def __repr__(self):
		return str(self)


class LLBeachLine(BeachLine):
	def __init__(self):
		self.list = LinkedList()

	def search(self, p):
		#print 'search', p, self.list
		for node in self.list:
			# node.data is the arc
			#print 'node', node
			if intersect(p,node):
				return node
		raise Exception('No intersection for p = %s' % str(p))

	def insert(self,p,within=None):
		arc = Arc(p)
		print 'insert', arc, within
		if within is not None:
			# within <-> node <-> tmp
			#if within.next and not intersect(arc.point,within.next):
			tmp = Node(Arc(within.data.point),next=within.next)
			node = Node(arc,prev=within,next=tmp)
			tmp.prev = node
			if within.next:
				within.next.prev = tmp
			within.next = node
			# print '\ttmp', tmp.data, tmp.prev, tmp.next
			# print '\tnode', node.data, node.prev, node.next
			# print '\twithin', within.data, within.prev, within.next

			# print hex(id(tmp)),hex(id(within)),hex(id(node))
			# print 'head', self.list.head
			# for n in self.list:
			# 	print n
			# else:
			# 	print 'fuuuuuuuuuuuuuu'
			# 	within.next = Node(arc,)
			#print 'there', self.list
		else:
			self.list.head = Node(arc)
			node = self.list.head
			#print 'here', self.list

		return node

	def delete(self, arc):
		print 'delete', arc
		if arc.prev:
			arc.prev.next = arc.next

		if arc.next:
			arc.next.prev = arc.prev

	def sucessor(self,node):
		return node.next

	def predecessor(self,node):
		return node.prev

	@property
	def is_empty(self):
		return self.list.head is None

	def __str__(self):
		return str([ node.point[2] for node in self.list])

	def __iter__(self):
		for n in self.list:
			yield n

class AVLNode(object):
	def __init__(self,p,q=None,left=None,right=None,parent=None):
		self.p = p
		self.q = q
		self.left = left
		self.right = right
		self.parent = parent

		arc = Arc(p)
		self.__dict__.update(arc.__dict__.copy())

	def key(self,directrix):
		if self.q is None:
			return self.p[0]
		else:
			return intersection(self.p, self.q, directrix)[0]

	def __str__(self):
		if self.q:
			return '(%s,%s)' % (self.p[2], self.q[2])
		else:
			return '(%s)' % self.p[2]

	@property
	def is_leaf(self):
		return self.q is None

from utils import BinarySearchTree
class AVLBeachLine(BeachLine):
	def __init__(self):
		self.T = BinarySearchTree()

	def search(self, p):
		"""Given a fixed location of the sweep line, determine the arc of the
		beach line that intersects a given vertical line.
		"""
		curr = self.T._root
		while True:
			#print 'curr', p[1], curr.key(p[1]), curr, curr.left, curr.right, p[1] < curr.key(p[1])
			if p[0] < curr.key(p[1]):
				if curr.left:
					curr = curr.left
				else:
					return curr
			else:
				if curr.right:
					curr = curr.right
				else:
					return curr

	def predecessor(self,x):
		"""
		Given a node
		If all keys are distinct, the sucessor of a node x is the node with the smallest key greater than x.key
		"""
		pred = self.T.predecessor(x)
		if pred is not None:
			return self.T.predecessor(pred)
		else:
			print 'predecessor is none!'

	def sucessor(self,x):
		suc = self.T.sucessor(x)
		if suc is not None:
			return self.T.sucessor(suc)
		else:
			print 'sucessor is none!'

	def delete(self, arc):
		# find internal nodes

		print 'delete'
		pred = self.T.predecessor(arc)
		suc = self.T.sucessor(arc)
		# siblings are not true sucessors
		rsib = self.sucessor(arc)
		lsib = self.predecessor(arc)

		print 'siblings:'
		print lsib, arc, rsib
		print 'successors'
		print pred, arc, suc
		if arc.parent == pred:
			# I am the right child!
			print 'I AM RIGHT !!!!!!!!!!!!', arc.parent
			pa = arc.parent
			grandpa = pa.parent
			if grandpa.left == pa:
				grandpa.left = pa.left
			else:
				grandpa.right = pa.left
			suc.p = lsib.p
		else:
			# I am the left child!
			print 'I AM LEFT !!!!!!!!!!!!', arc.parent
			pa = arc.parent
			grandpa = pa.parent
			if grandpa.left == pa:
				grandpa.left = pa.right
			else:
				grandpa.right = pa.right
			pred.q = rsib.p


	def insert(self, p, within=None):
		"""Insert an new arc pi within a given arc pj,
		thus splitting the arc for pj into two. This creates three
		arcs, pj, pi, and pj.
		"""
		if within is not None:
			within.q = p
			within.left = AVLNode(within.p, parent=within)
			within.right = AVLNode(p,within.p, parent=within)
			cur = within.right
			cur.left = AVLNode(cur.p, parent=cur)
			cur.right = AVLNode(cur.q, parent=cur)

			node = cur.left
		else:
			self.T._root = AVLNode(p)
			node = self.T._root
		return node

	@property
	def is_empty(self):
		return self.T._root is None

	def __iter__(self):
		for node in self.T:
			#if node.is_leaf:
			yield node

	def __str__(self):
		return ' '.join([ str(x) for x in self ])