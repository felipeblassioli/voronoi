# -*- coding: utf-8 -*-

from heapq import heappush, heappop, heapify

from .event import Event, CircleEvent
from .dcel import Hedge
from .geometry import X,Y,circle, same_point
from .beachline import LLBeachLine, AVLBeachLine

class Voronoi(object):
	def __call__(self, pts):
		self.edges = []
		self._faces = {}
		self.vertices = []
		self.input = pts
		print 'input is ', pts
		return self.run(pts, bounding_box=[-5,20,0,20])

	def run(self, points, bounding_box=None):
		"""
		Receive a sets of points and return the voronoi diagram in a DCEL
		Q: Event queue
		T: Status structure
		D: Doubly connected edge list
		"""

		self.T = AVLBeachLine()
		self.Q = [ Event(p) for p in points ]
		heapify(self.Q)
		while len(self.Q) > 0:
			event = heappop(self.Q)
			if event.is_site: 
				self._handle_site_event(event)
			else: 
				self._handle_circle_event(event)
			self.animate(event)

		if bounding_box is not None:
			for e in self.edges:
				e.trim(*bounding_box)


		#self._finish(self.root)
		self.animate(Event((0,-100)), draw_circle_events=False)
		return self.edges

	def _create_twins(self, site1, site2):
		half_edge = Hedge(None, None, site1, self._faces.get(site1, None))
		half_edge._twin = Hedge(None, half_edge, site2, self._faces.get(site2, None))
		self.edges.append(half_edge)
		self._faces[site1] = half_edge
		self._faces[site2] = half_edge._twin

		return half_edge
	# def finish(self):
	# 	"""Finish the edges"""
	# 	y = 
	# 	for h in edges:
	# 		h.finish(intersection)

	# http://www.ams.org/samplings/feature-column/fcarc-voronoi
	def _handle_site_event(self, evt):
		"""
		ProcessSite(event)

		If (binaryTree == null)
			Set event as root
		Else
			a. Find correct position in binaryTree for this site event.  This is done by 
			   starting at root and checking breakpoints of internal nodes as you reach them.  
			   Go to right or left child in the tree based on whether the current site event’s 
			   x-coordinate is greater than or less than the breakpoint (if it is equal to a 
			   	breakpoint either direction can be chosen).  Stop when a leaf node is encountered.
			b. If the arc that this site hits contains a pointer to a circle event in the queue, 
			   delete that circle event from the queue (it is a false alarm and will never happen).  
			   Also delete circle events involving this arc from the queue.  These events can be 
			   found by looking at the neighbours of this arc in the binary tree (note that the 
			   	neighbours will not always exist, and they can be other leaves than just the 
			   	sibling of this leaf)
			c. Remove the leaf that this site event hits and replace it with a subtree with three 
			   leaf nodes.  The left and right leaves will contain the original site, and the middle 
			   leaf will contain this new site.  The two new internal nodes of the tree will represent 
			   the two breakpoints that have been created along with the new edge that needs to be 
			   created.  Create a new edge in the edge vertex list and point each internal node to one 
			   side of this new edge.
			d. Check for circle events caused by this new site.  Note that we don’t have to check the 
			   triple of leaves where the new site is the middle leaf, because the breakpoints can’t 
			   converge.  Instead, check the triples where this new site is the far left and far right 
			   arc.  If the breakpoints are converging, calculate the circle event priority and place it 
			   in the queue.  Make a pointer from the middle leaf (the leaf that will disappear in the 
			   circle event) to the event in the queue.
		"""
		if self.T.is_empty:
			self.T.insert(evt.point)
		else:
			# a is the arc vertically above evt.point in the beachline
			a = self.T.search(evt.point)
			#print 'arc above', evt, 'is', a
			# If the arc a points to circle event, delete that event
			if a.circle_event is not None:
				print 'False alarm'
				a.circle_event.deleted = True

			x = self.T.insert(evt.point,within=a)
			# Create edges
			self._create_twins(x.point,a.point)

			# check the triples where this new site is the far left and far right arc.
			predecessor = self.T.predecessor(x)
			sucessor = self.T.sucessor(x)
			self.check_circle(predecessor, evt.point[Y])
 			self.check_circle(sucessor, evt.point[Y])
			

 	def _handle_circle_event(self, evt):
 		"""

 		ProcessCircle(event)
			1. Update breakpoints involving the arc that is disappearing in this event.  
			   The edges that these breakpoints point to will be finishing.
			2. Check for circle events involving this arc in the immediate left and right arcs of the beach line.  
			   If circle events exist at these nodes, delete them.
			3. Remove the corresponding arc leaf from the binaryTree.  Delete internal parent node of this arc leaf, 
			   and promote sibling leaf or subtree to the parent’s position.  Update breakpoints in binaryTree to 
			   reflect the new breakpoint that has been created.  Note that there will be two breakpoints that are 
			   disappearing in this event, and one new breakpoint that is being created.  This newly created breakpoint 
			   needs to point to one side of a new edge created in the edge vertex list.  The other side of the edge 
			   should be set to the vertex created by this event.
			4. Check new triples of arcs created by this rearranging of the binaryTree for circle events.  If a circle 
			   event is detected put it in the priority queue, and put pointers in the leaf nodes that will disappear 
			   in that event.
 		Source: http://cgm.cs.mcgill.ca/~mcleish/644/Projects/DerekJohns/Sweep.htm#SweepAlgorithm
 		"""
 		if not evt.deleted:
 			print 'delete arc ', evt.arc, id(evt.arc)
 			# new hedge
 			#h = Hedge(self.T.predecessor(evt.arc).point, self.T.sucessor(evt.arc).point, evt.point[Y])
 			#self.edges.append(h)
 			self.vertices.append(evt.center)
 			print 'new HE for ', self.T.predecessor(evt.arc), self.T.sucessor(evt.arc), self.T.predecessor(evt.arc).point, self.T.sucessor(evt.arc).point
 			new_half_edge = self._create_twins(self.T.sucessor(evt.arc).point, self.T.predecessor(evt.arc).point)
 			#new_half_edge = self._create_twins(self.T.sucessor(evt.arc).point, self.T.sucessor(evt.arc).point)
 			new_half_edge._origin = evt.center

 			for left, right in ((self.T.predecessor(evt.arc).point, evt.arc.point),
 								(evt.arc.point, self.T.sucessor(evt.arc).point)):
 				half_edge = None
 				for he in self._faces[left]._iter_neighbours():
 					if he._twin._site == right:
 						half_edge = he
 						break
 				print 'updating', half_edge
 				if half_edge:
 					half_edge._origin = evt.center
 			#remove possible circle events involving this site'
 			x = evt.arc
 			for e in self.Q:
 				if not e.is_site:
 					if e.arc.point == evt.arc.point:
 						print 'deleting', self.T.predecessor(e.arc),  self.T.sucessor(e.arc),'vs', self.T.predecessor(evt.arc), self.T.sucessor(evt.arc), evt.arc, 'is at', id(evt.arc), evt.arc.circle_event
 						e.deleted = True

			predecessor = self.T.predecessor(x)
			sucessor = self.T.sucessor(x)
 			self.T.delete(evt.arc)

 			# if self.T.predecessor(x) is not None and self.T.predecessor(x).circle_event is not None:
 			# 	print 'DELETE THIS SHIT', self.T.predecessor(x).circle_event
 			# 	self.T.predecessor(x).circle_event.deleted = True
 			# if self.T.sucessor(x) is not None and self.T.sucessor(x).circle_event is not None:
 			# 	print 'DELETE THIS SHIT', self.T.sucessor(x).circle_event
 			# 	self.T.sucessor(x).circle_event.deleted = True

 			
			self.check_circle(predecessor, evt.point[Y])
 			self.check_circle(sucessor, evt.point[Y])
 		else:
 			print 'DELETED', evt.arc, id(evt.arc)

 	def _check_circle(self, predecessor, arc, sucessor, y):
 		 # We need a triple of arcs.
 		if not predecessor or not sucessor or not arc:
 			return

 		bottom, center = circle(predecessor.point, arc.point, sucessor.point)
 		if center and bottom[Y] < y:
 			if abs(bottom[Y] - y) < 0.0001: return
 			print 'DETECTED', predecessor, arc, sucessor, ' arc is at', id(arc), 'bottom is', bottom
 			arc.circle_event = CircleEvent(bottom,arc,center)
 			heappush(self.Q, arc.circle_event)

 	def check_circle(self, arc, y):
 		"""Look for a new circle event for arc."""
 		predecessor = self.T.predecessor(arc)
 		sucessor = self.T.sucessor(arc)

 		self._check_circle(predecessor,arc,sucessor,y)





"""
Data Structures:

A priority queue to keep track of the site events and circle events.

A priority queue is used to tell us when the topology of the beach line could change.  The priority of an event is determined by when the sweep line will encounter it.  
For example, if the sweep line starts at the top of the problem space and moves downwards, 
! the site events would be given higher priority if they have a larger y-coordinate (assuming y increases in the upward direction).  
! Circle events are also given a priority by when the sweep line will encounter them.  
In our example this would be the y-coordinate of the sweep line as it just grazes the bottom of the circle corresponding to the circle event.


- Site events will store their site.  
- Circle events will store the position they will occur, as well as a pointer to the arc (leaf) in the binary tree that will disappear when this circle event occurs. 

The algorithm progresses by simply popping the highest priority event from the queue and calculating the manner in which the topology of the beach line changes.

The site events are known beforehand and can be entered into the priority queue during initialization.  
However, the circle events are detected as the beach line changes its shape, and need to be entered into the queue at that time.  More on this process can be found below.

Source: http://cgm.cs.mcgill.ca/~mcleish/644/Projects/DerekJohns/Sweep.htm#CircleEvents
"""