# -*- coding: utf-8 -*-
from .geometry import intersection

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