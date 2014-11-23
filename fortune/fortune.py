# -*- coding: utf-8 -*-
from heapq import heappush, heappop, heapify
import logging

circles = []

class Event(object):
	"""The priority of an event is determined by when the sweep line will encounter it.  
	There are two kinds of events:
	- Site Events:
	  Site events would be given a higher priority if they have a larger y-coordinate (assuming y increases in the upward direction)
	- Circle Events:
	  Circle events would be given a higher priority if they have a larger y-coordinate of the sweep line as it just grazes the bottom 
	  of the circle corresponding to the circle event.

	  Site event we store the site itself.
	  For a circle event we store is the lowest point of the circle, with a pointer to the leaft in T that represents the arc that will disappear
	"""

	def __init__(self, point):
		self.point = point
		self.is_site = True

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Event(point={},is_site={})".format(self.point,self.is_site)

	def __cmp__(self, other):
		assert isinstance(other,Event)
		return cmp(other.point[Y],self.point[Y])

class CircleEvent(Event):
	def __init__(self, point, arc, center):
		super(CircleEvent,self).__init__(point)
		self.arc = arc
		self.center = center
		self.is_site = False
		self.deleted = False

	def __str__(self):
		return "CircleEvent(point={},arc={},deleted={})".format(self.point,self.arc,self.deleted)


class Arc(object):
	def __init__(self, point=None):
		self.point = point
		# The node in the event queue that represents the circle event in which this event will disappear
		self.circle_event = None

	def __str__(self):
		return "Arc(point=[{}])".format(self.point)

X = 0
Y = 1
edges = []
class Hedge(object):
	def __init__(self,p,q,y):
		self.left = p
		self.right = q
		self.end = None
		self.origin = self.current(y)

	def current(self,directrix):
		if self.end:
			return self.end
		return intersection(self.left,self.right,directrix)

	def finish(self, p):
		if self.end is None:
			self.end = p

	def __str__(self):
		return 'Hedge(left={}, right={}'.format(self.left,self.right)

import llbeachline
class Voronoi(object):
	def __call__(self, pts):
		self.input = pts
		self.run(pts)

	def run(self, points):
		"""
		Receive a sets of points and return the voronoi diagram in a DCEL
		Q: Event queue
		T: Status structure
		D: Doubly connected edge list
		"""

		self.T = llbeachline.LLBeachLine()
		self.Q = [ Event(p) for p in points ]
		heapify(self.Q)
		print 'Q', self.Q
		print '------------- Main Loop ---------'
		while len(self.Q) > 0:
			event = heappop(self.Q)
			if event.is_site: 
				self._handle_site_event(event)
			else: 
				self._handle_circle_event(event)
			self.animate(event)
		
		print '-------------------------------'

		#self._finish(self.root)
		self.animate(Event((0,-100)), draw_bottoms=False)
		print 'done'
		edges = None
		return edges

	# def finish(self):
	# 	"""Finish the edges"""
	# 	y = 
	# 	for h in edges:
	# 		h.finish(intersection)
# // Find the rightmost point on the circle through a,b,c.
# bool circle(point a, point b, point c, double *x, point *o)
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
		global edges
		if self.T.is_empty:
			self.T.insert(Arc(evt.point))
		else:
			# a is the arc vertically above evt.point in the beachline
			a = self.T.search(evt.point)
			# print
			# print '\ta is ', a
			# print
			# If the arc a points to circle event, delete that event
			if a.circle_event:
				print 'false alarm!', a.circle_event
				a.circle_event.deleted = True

			x = self.T.insert(Arc(evt.point),within=a)
			# Create edges
			# Add new half-edges connected to i's endpoints.
			# i->prev->s1 = i->s0 = new seg(z);
			# i->next->s0 = i->s1 = new seg(z);
			edges.append(Hedge(a.point,x.point,x.point[Y]))
			edges.append(Hedge(x.point,a.point,x.point[Y]))

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
 		global edges
 		if not evt.deleted:
 			#print '------->', evt, ' deleting ', evt.arc
 			# Step 1
 			for h in edges:
 				#print '\t', h.current(evt.point[Y]), evt.center, same_point(h.current(evt.point[Y]), evt.center)
 				if same_point(h.current(evt.point[Y]), evt.center):
 					h.finish(evt.center)

 			edges.append(Hedge(evt.arc.prev.point, evt.arc.next.point, evt.point[Y]))
 			#remove possible circle events involving this site'
 			x = evt.arc
 			print 'xxx', evt.arc.circle_event
 			for e in self.Q:
 				if not e.is_site:
 					if e.arc.point == evt.arc.point:
 						e.deleted = True

 			self.T.delete(evt.arc)

			predecessor = self.T.predecessor(x)
			sucessor = self.T.sucessor(x)
			self.check_circle(predecessor, evt.point[Y])
 			self.check_circle(sucessor, evt.point[Y])
 		else:
 			print evt, 'already deleted'

 	def check_circle(self, arc, y):
 		"""Look for a new circle event for arc."""
 		global circles

 		# # Invalidate old events 
 		# if arc.circle_event and arc.circle_event.point[Y] != y:
 		# 	arc.circle_event.deleted = True
 		# 	print 'deleted', arc, arc.circle_event
 		# arc.circle_event = None

 		predecessor = self.T.predecessor(arc)
 		sucessor = self.T.sucessor(arc)
 		# We need a triple of arcs.
 		if not predecessor or not sucessor or not arc:
 			return

 		bottom, center = circle(predecessor.point, arc.point, sucessor.point)
 		#print 'check_circle', arc, y
 		#print '\t', center, bottom
 		circles.append((center,bottom))
 		if center and bottom[Y] < y:
 			if abs(bottom[Y] - y) < 0.0001: return
 			arc.circle_event = CircleEvent(bottom,arc,center)
 			heappush(self.Q, arc.circle_event)
 			print 'CircleEvent DETECTED !!! arc ', y, arc, arc.circle_event


from matplotlib import pyplot as plt
from pylab import savefig
from anim import *
from geometry import intersection, circle, euclidean_distance as dist, same_point
i=1
def animate(self,e,draw_bottoms=True):
	global i
	global circles
	global edges

	filename = 'tmp-{0:03}.png'.format(i)
	plt.clf()
	fig = plt.gcf()
	# plt.axis([0,width, 0, height])
	plt.axis([-5,20, 0, 20])

	print
	print i, 'Event: ', e
	print '============================'
	print 'beachline', self.T, ' in ', filename
	#print 'ARCS:'
	#print 'head',self.T.list.head
	for arc in self.T:
		#print '\t', arc, arc.prev, arc.next
		end,start=None,None
		# plot intersections
		if arc.prev:
			start = intersection(arc.prev.point,arc.point,e.point[Y])
			#plt.plot(start[0],start[1],'o',color='red')
		if arc.next:
			end = intersection(arc.point,arc.next.point,e.point[Y])
			#plt.plot(end[0],end[1],'o',color='red')
		plot_parabola(arc.point,e.point[Y],endpoints=[start,end],color='purple')
		#print '\t\tstart = ',start,'end = ',end

	#print 'edges:'
	for h in edges:
		#print '\t', h, h.origin, h.current(e.point[Y])
		plot_line(h.origin, h.current(e.point[Y]), color='blue')

	for center, bottom in circles:
		# radius = dist(center,bottom)
		# circle=plt.Circle(center,radius,color='b',fill=False)
		# fig.gca().add_artist(circle)

		# plot_points([center,bottom], color='green')
		if draw_bottoms and bottom:
			plot_points([bottom], color='green')

	#plot_vertical(e.point[X])
	plot_directrix(e.point[Y])
	plot_points(self.input)
	
	fig.savefig(filename, bbox_inches='tight')
	print '============================'
	i+=1

if __name__ == '__main__':
	v = Voronoi()
	Voronoi.animate = animate
	#pts = [(1,1,'p'),(2,2,'q'),(3,0.5,'r')]
	x = [4,8,11,5,9,12.5]
	y = [12,11,10,6.5,5.5,4.5]
	label = ['a','b','c','d','e','f']
	# x = [4,3,11]
	# y = [12,3,6]
	# label = ['a','b','c']
	#x = [4,8,11,5]
	#y = [12,11,10,6.5]
	#label = ['a','b','c','d']
	pts = zip(x,y,label)
	edges = v(pts)

	print edges	


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