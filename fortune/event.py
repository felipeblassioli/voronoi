# -*- coding: utf-8 -*-
from .geometry import X,Y

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