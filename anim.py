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



from fortune.geometry import vertex, coefficients
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
		if start != -10:
			pts = pylab.linspace(-10,start,num=240)
			plt.plot(pts, parabola(pts,f,directrix), '-',color='#e3e3e3',linewidth=1)

		if end != width:
			pts = pylab.linspace(end,width,num=240)
			plt.plot(pts, parabola(pts,f,directrix), '-',color='#e3e3e3',linewidth=1)

		pts = pylab.linspace(start,end,num=240)
		plt.plot(pts, parabola(pts,f,directrix), '-',color=color,linewidth=2)
		#parabolas.append(parabola(pts,f,directrix))
		# Plot a vertical line that has the focus
	#plt.plot([a,a],[0,height],'b-',color=c)

from matplotlib import pyplot as plt
from pylab import savefig
from fortune.geometry import intersection, circle, euclidean_distance as dist, same_point

def _draw_beachline(e, beachline):
	print beachline.T.dumps()
	for arc in beachline:
		end,start=None,None
		# plot intersections
		if beachline.predecessor(arc):
			start = intersection(beachline.predecessor(arc).point,arc.point,e.point[Y])
			plt.plot(start[0],start[1],'o',color='black')
		if beachline.sucessor(arc):
			end = intersection(arc.point,beachline.sucessor(arc).point,e.point[Y])
			plt.plot(end[0],end[1],'o',color='black')
		plot_parabola(arc.point,e.point[Y],endpoints=[start,end],color='purple')

# def _draw_hedges(e, hedges):
# 	for h in hedges:
# 		if h.left[Y] == h.right[Y]:
# 			plot_vertical(h.origin[X])
# 		else:
# 			plot_line(h.origin, h.current(e.point[Y]), color='blue')
# 		#print '\t', h
def _draw_hedges(e, hedges):
	for h in hedges:
		#plot_line(h.left_site, h.right_site, color='gray')
		
		#plot_line(h.line2[0], h.line2[1], color='blue')
		# i = intersection(h.left_site,h.right_site,e.point[Y])
		# j = intersection(h.right_site,h.left_site,e.point[Y])
		# if h._origin is not None:
		# 	plot_line(h.vertex_from, i)
		# 	pass
		# else:
		# 	plot_line(h.line[0], j)
		#plot_line(h.vertex_from, i, color='red')
		#plot_line(h.vertex_from, j, color='orange')
		if h._origin:
			plot_line(h.vertex_from(e.point[Y]), h.vertex_to(e.point[Y]), color='green')
		else:
			plot_line(h.vertex_from(e.point[Y]), h.vertex_to(e.point[Y]), color='blue')
		#plot_line(h.line[0]/(h.line[0].norm), h.line[1]/(h.line[1].norm), color='green')
		print '\t', h

def _draw_circle_events(e, event_queue, past_circle_events, draw_bottoms=True, draw_circles=False, fig=None):
	if not e.is_site:
		bottom, center = e.point, e.center
		radius = dist(center,bottom)
		circle=plt.Circle(center,radius,color='b',fill=False)
		fig.gca().add_artist(circle)

		past_circle_events.append(e)

	for e in past_circle_events:
		plot_points([e.point], color='green')

	for evt in event_queue:
		# Circle Event
		if not evt.is_site:
			bottom, center = evt.point, evt.center
			#if same_point(evt.point, e.point):
			if draw_circles:
				radius = dist(center,bottom)
				circle=plt.Circle(center,radius,color='b',fill=False)
				fig.gca().add_artist(circle)

			# plot_points([center,bottom], color='green')
			if draw_bottoms and bottom:
				plot_points([bottom], color='green')

i=1
past_circle_events = []
from pylab import axes
def animate(self,e,draw_bottoms=True, draw_circles=False, draw_circle_events=True):
	global i
	global past_circle_events

	filename = 'tmp-{0:03}.png'.format(i)
	plt.clf()
	fig = plt.gcf()
	# plt.axis([0,width, 0, height])
	plt.axis([-5,20, 0, 20])

	_draw_beachline(e, self.T)
	_draw_hedges(e, self.edges)
	if draw_circle_events:
		_draw_circle_events(e, self.Q, past_circle_events, draw_bottoms, draw_circles, fig)

	plot_directrix(e.point[Y])
	plot_points(self.input)
	if e.is_site:
		plot_points([e.point], color='black')
	
	plt.grid(True)
	axes().set_aspect('equal', 'datalim')
	fig.savefig(filename, bbox_inches='tight')
	print filename, 'beachline', self.T
	i+=1
