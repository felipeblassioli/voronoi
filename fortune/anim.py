# -*- coding: utf-8 -*-

FOCUS_COLOR = 'blue'
X = 0
Y = 1
width = 35
height = 35

import numpy as np
import matplotlib.pyplot as plt
def plot_points(pts,color='red'):
	try:
		x,y,label = zip(*pts)
		x,y,label = list(x),list(y),list(label)
	except:
		x,y = zip(*pts)
		x,y = list(x),list(y)
	plt.plot(x,y,'o',color=color)

def plot_line(a,b,**kwargs):
	color = kwargs.pop('color', 'blue')
	x,y=[],[]
	for p in [a,b]:
		x.append(p[X])
		y.append(p[Y])
	plt.plot(x,y,'-',color=color)

def plot_directrix(y,color='red'):
	plt.plot([-10,width],[y,y],'-',color=color)


def plot_vertical(x,color='black'):
	plt.plot([x,x],[-10,height],'-',color=color)

import pylab



from geometry import vertex, coefficients
def parabola (list_x, focus, directrix):
	A,B,C = coefficients(focus,directrix)
	if A == 0:
		return None
	return [ A*(x**2) + B*x + C for x in list_x ]

def plot_parabola(focus,directrix, endpoints=None,pts=pylab.linspace(-10, width, num=320), color='purple'):
	a = focus[X]
	b = focus[Y]
	label = '{} ({},{})'.format(focus[2],a,b)
	# plt.annotate(
	# 	label, 
	# 	xy = (a, b), xytext = (-5,5),
	# 	textcoords = 'offset points', ha = 'right', va = 'bottom'
	# )
	f = (a,b)
	# Plot the focus
	plt.plot(a,b, 'bo',color=FOCUS_COLOR)
	# Plot vertex
	#v = vertex(a,b,directrix)
	#plt.plot(v[0],v[1], 'bo',color=c)
	# Plot the parabola
	if focus[Y] == directrix:
		if endpoints[0]:
			end = endpoints[0][Y]
		elif endpoints[1]:
			end = endpoints[1][Y]
		else:
			end = height
		
		plt.plot([a,a],[directrix,end],'b-',color=color,linewidth=2)
	else:
		start = endpoints[0][X] if endpoints[0] is not None else -10
		end = endpoints[1][X] if endpoints[1] is not None else width
		#print '\tplot focus', focus, start,end
		if start != -10:
			pts = pylab.linspace(-10,start,num=240)
			#print '\t\tstart: -10 to ',start
			plt.plot(pts, parabola(pts,f,directrix), '-',color='#e3e3e3',linewidth=1)

		if end != width:
			pts = pylab.linspace(end,width,num=240)
			#print '\t\tend: ',end,'to',width
			plt.plot(pts, parabola(pts,f,directrix), '-',color='#e3e3e3',linewidth=1)

		pts = pylab.linspace(start,end,num=240)
		plt.plot(pts, parabola(pts,f,directrix), '-',color=color,linewidth=2)

from matplotlib import pyplot as plt
from pylab import savefig
from geometry import INFINITY, intersection, circle, euclidean_distance as dist, same_point

def _draw_beachline(e, beachline):
	isInfinity = lambda x: x is not None and x[0] == INFINITY and x[1] == INFINITY
	#print beachline.T.dumps()
	for arc in beachline:
		end,start=None,None
		pred,suc = beachline.predecessor(arc), beachline.sucessor(arc)
		#print pred, arc, suc
		if pred is not None:
			start = intersection(pred.site,arc.site,e.y)
			# if start[X] == INFINITY and start[Y] == INFINITY:
			# 	start = None
		if suc is not None:
			end = intersection(arc.site,suc.site,e.y)
			# if end[X] == INFINITY and end[Y] == INFINITY:
			# 	end = None
		if isInfinity(start) and isInfinity(end) or isInfinity(start) and end is None:
			continue
		elif isInfinity(start):
			start = None
		elif isInfinity(end):
			end = None
		# print 'arc is',arc, 'intersections are',start,end, 'pred/suc', beachline.predecessor(arc),beachline.sucessor(arc)
		plot_parabola(arc.site,e.y,endpoints=[start,end],color='purple')

def _draw_hedges(e, hedges):
	for h in hedges:
		if h._origin:
			plot_line(h.vertex_from(e.y), h.vertex_to(e.y), color='blue')
		else:
			plot_line(h.vertex_from(e.y), h.vertex_to(e.y), color='blue')

def _draw_circle_events(e, event_queue, past_circle_events, draw_bottoms=True, draw_circles=False, fig=None, draw_past_circles=False):
	if not e.is_site:
		bottom, center, radius = e.bottom, e.center, e.radius
		#radius = dist(center,bottom)
		circle=plt.Circle(center,radius,color='b',fill=False)
		fig.gca().add_artist(circle)

		past_circle_events.append(e)
		plot_points([bottom], color='green')

	if draw_past_circles:
		for e in past_circle_events:
			plot_points([e.bottom], color='green')

	for evt in event_queue:
		# Circle Event
		if not evt.is_site and evt.is_valid:
			bottom, center = evt.bottom, evt.center
			#if same_point(evt.site, e.site):
			if draw_circles:
				radius = evt.radius
				circle=plt.Circle(center,radius,color='b',fill=False)
				fig.gca().add_artist(circle)

			# plot_points([center,bottom], color='green')
			if draw_bottoms and bottom:
				plot_points([bottom], color='green')

i=1
past_circle_events = []
from pylab import axes
import voronoi
def animate(self,e,draw_bottoms=True, draw_circles=False, draw_circle_events=True):
	global i
	global past_circle_events

	filename = 'tmp-{0:03}.png'.format(i)
	#print 'animate', e, type(e), isinstance(e,voronoi.SiteEvent), isinstance(e,voronoi.CircleEvent)
	plt.clf()
	fig = plt.gcf()
	# plt.axis([0,width, 0, height])
	if self.bounding_box is not None:
		plt.axis(self.bounding_box)
	#plt.axis([-5,25, -5, 25])

	_draw_beachline(e, self.T)
	_draw_hedges(e, self.edges)
	if draw_circle_events:
		_draw_circle_events(e, self.Q, past_circle_events, draw_bottoms, draw_circles, fig)

	plot_directrix(e.y)
	plot_points(self.input)
	if e.is_site:
		plot_points([e.site], color='black')
	
	plt.grid(True)
	axes().set_aspect('equal', 'datalim')
	fig.savefig(filename, bbox_inches='tight')
	print filename, 'beachline', self.T, 'Input:', self.input
	i+=1
