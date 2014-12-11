# -*- coding: utf-8 -*-
from .geometry import X,Y

from collections import namedtuple
from math import sqrt
_Point = namedtuple('Point', ['x', 'y', 'label'])
class Point(_Point):
	"""A point in the plane

	Attributes:
	x: float, the x coordinate
	y: float, the y coordinate

	Properties:
	square: float, the square of the norm of the vector (x, y)
	norm: float, the norm of the vector (x, y)
	"""
	def __new__(_cls, x, y, label=None):
		'Create a new instance of Point(x, y)'
		return _Point.__new__(_cls, x, y, label)

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

	def __add__(self, other):
		return self.__class__(self.x + other.x, self.y + other.y)

	def __neg__(self):
		return self.__class__(-self.x, -self.y)

	def __sub__(self, other):
		return self + (-other)

	def __div__(self, other):
		return self.__class__(self.x / other, self.y / other)

	def __cmp__(self, other):
		cmp_x = cmp(self.x, other.x)
		if cmp_x != 0:
			return cmp_x
		return cmp(self.y, other.y)

	def __abs__(self):
		return self.norm

	@property
	def square(self):
		return self.x**2 + self.y**2

	@property
	def norm(self):
		return sqrt(self.square)

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
		if len(point) < 3:
			self.point = Point(point[X], point[Y], None)
		else:
			self.point = Point(point[X], point[Y], point[2])
		
		self.is_site = True

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Event(point={},is_site={})".format(self.point,self.is_site)

	def __cmp__(self, other):
		assert isinstance(other,Event)
		c = cmp(other.point[Y],self.point[Y])
		if c == 0:
			return cmp(self.point[X], other.point[X])
		else:
			return c

class CircleEvent(Event):
	def __init__(self, point, arc, center):
		super(CircleEvent,self).__init__(point)
		self.arc = arc
		self.center = center
		self.is_site = False
		self.deleted = False

	def __str__(self):
		return "CircleEvent(point={},arc={},deleted={})".format(self.point,self.arc,self.deleted)