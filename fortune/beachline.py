# -*- coding: utf-8 -*-

from . import log

class Arc(object):
	def __init__(self, point=None):
		self.site = point
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
		if x is None:
			return x
		# Cormen 3ed p292
		if x.left is not None:
			return self.maximum(x.left)
		y = x.parent
		while y is not None and x == y.left:
			x = y
			y = y.parent
		return y

	def sucessor(self,x):
		if x is None:
			return x
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
	
from geometry import intersection
class AVLNode(dict):
	def __init__(self,p,q=None,left=None,right=None,parent=None):
		self.p = p
		self.q = q
		self.left = left
		self.right = right
		self.parent = parent

		arc = Arc(p)
		# Merge all arc attributes such as .point, circle_event into the node..
		for k,v in arc.__dict__.copy().items():
			self.__setattr__(k,v)

	def __eq__(self,other):
		return self.p == other.p and self.q == other.q

	def __setattr__(self,name,value):
		if name in ['left', 'right'] and isinstance(value,AVLNode):
			value.parent = self
		if name in ['left', 'right', 'parent']:
			super(AVLNode,self).__setitem__(name,value)
		else:
			super(AVLNode,self).__setattr__(name,value)

	def __getattribute__(self,name):
		if name in ['left', 'right', 'parent']:
			return self[name]
		return super(AVLNode,self).__getattribute__(name)
		

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

class AVLBeachLine(BeachLine):
	def __init__(self):
		self.T = BinarySearchTree()

	def search(self, p):
		"""Given a fixed location of the sweep line, determine the arc of the
		beach line that intersects a given vertical line.
		"""
		curr = self.T._root
		while True:
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

	def sucessor(self,x):
		suc = self.T.sucessor(x)
		if suc is not None:
			return self.T.sucessor(suc)

	#def delete(self, arc):

	def delete(self, arc):
		# find internal nodes
		log('\t\t\t deleting %s' % arc)
		
		pred = self.T.predecessor(arc)
		suc = self.T.sucessor(arc)
		
		log('\t\t\t\toriginal pred/suc %s/%s' % (pred,suc))

		# siblings are not true sucessors
		rsib = self.sucessor(arc)
		lsib = self.predecessor(arc)
		log('\t\t\t\tsiblings: %s %s' % (lsib,rsib))
		
		if arc.parent == pred:
			# I am the right child!
			pa = arc.parent
			grandpa = pa.parent
			if grandpa.left == pa:
				grandpa.left = pa.left
			else:
				grandpa.right = pa.left
			suc.p = lsib.p
		else:
			# I am the left child!
			pa = arc.parent
			grandpa = pa.parent
			if grandpa.left == pa:
				grandpa.left = pa.right
			else:
				grandpa.right = pa.right
			pred.q = rsib.p
		log('\t\t\t\tsiblings: %s %s' % (lsib,rsib))
		return lsib, rsib


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
			if node.is_leaf:
				yield node

	def __str__(self):
		return ' '.join([ str(x) for x in self ])

def out(start_node):
	# if start_node == None:
	# 	start_node = self.root
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
