# -*- coding: utf-8 -*-
from heapq import heappush, heappop, heapify

from . import log
from .geometry import Point

class EventQueue(object):
	def __init__(self, points):
		# We remove duplicates (This is a degenerate case)
		seen = set()
		seen_add = seen.add
		self.events = [ SiteEvent(p) for p in points if not (p in seen or seen_add(p))]
		heapify(self.events)

		# for debugging only:
		labels = 'abcdefghijklmnopqrstuvxwyz'
		if len(self.events) <= len(labels):
			self.events = [ SiteEvent(Point(evt.site.x, evt.site.y, labels[i])) for i, evt in enumerate(self.events) ]


	def push(self,evt):
		heappush(self.events, evt)

	def pop(self):
		return heappop(self.events)

	def __repr__(self):
		return str(self.events)

	def __iter__(self):
		for x in self.events:
			yield x

	@property
	def is_empty(self):
		return len(self.events) == 0

class FortuneEvent(object):

    def __cmp__(self, other):
    	if other is None:
    		return False
        c = cmp(other.y, self.y)
        if c == 0:
        	return cmp(self.x,other.x)
        return c

    @property
    def y(self):
        raise NotImplementedError()

    @property
    def is_site(self):
        return isinstance(self,SiteEvent)

class SiteEvent(FortuneEvent):

    def __init__(self, site):
    	if type(site) == tuple:
    		self.site = Point(*site)
    	else:
        	self.site = site

    def __repr__(self):
        return u"SiteEvent at y=%s" % self.y

    @property
    def y(self):
        return self.site.y

    @property
    def x(self):
    	return self.site.x
    	
class CircleEvent(FortuneEvent):

	def __init__(self, arc, circle):
		self.arc = arc
		center, radius = circle
		self.circle = (Point(*center), radius)
		arc.circle_event = self

		log('\t\t\t Detected: %s ' % self)

	@property
	def x(self):
		return self.bottom.x

	@property
	def y(self):
		(center, radius) = self.circle
		return center.y - radius

	@property
	def is_valid(self):
		if self.arc.circle_event is None:
			return False
		return self.arc.circle_event == self

	@property
	def radius(self):
		return self.circle[1]

	@property
	def center(self):
		return self.circle[0]

	@property
	def bottom(self):
		return Point(self.center.x, self.center.y - self.radius)

	def __repr__(self):
		return u"CircleEvent at y=%s center is %s arc is %s" % (self.y, self.center, self.arc)

	# @property
	# def is_site(self):
	# 	return False
