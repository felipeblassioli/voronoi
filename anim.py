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
	# plt.annotate(
	# 	label, 
	# 	xy = (x, y), xytext = (-5,5),
	# 	textcoords = 'offset points', ha = 'right', va = 'bottom'
	# )	

def plot_line(*args,**kwargs):
	color = kwargs.pop('color', 'blue')
	pts = list(args)
	hah=[list(t) for t in zip(*pts)]
	plt.plot(hah[0],hah[1],'-', color=color)

def plot_directrix(y,color='red'):
	plt.plot([-10,width],[y,y],'-',color=color)


def plot_vertical(x,color='black'):
	plt.plot([x,x],[-10,height],'-',color=color)

import pylab



from fortune.geometry import vertex, coefficients
def parabola (list_x, focus, directrix):
	A,B,C = coefficients(focus,directrix)
	#print 'coe', A,B,C, 'focus', focus, 'directrix', directrix
	if A == 0:
		return None
	return [ A*(x**2) + B*x + C for x in list_x ]

def plot_parabola(focus,directrix, endpoints=None,pts=pylab.linspace(-10, width, num=320), color='purple'):
	#print focus, 'directrix', directrix
	a = focus[X]
	b = focus[Y]
	label = '{} ({},{})'.format(focus[2],a,b)
	# plt.annotate(
	# 	label, 
	# 	xy = (a, b), xytext = (-5,5),
	# 	textcoords = 'offset points', ha = 'right', va = 'bottom'
	# )
	f = (a,b)
	#print f
	# Plot the focus
	plt.plot(a,b, 'bo',color=FOCUS_COLOR)
	# Plot vertex
	#v = vertex(a,b,directrix)
	#plt.plot(v[0],v[1], 'bo',color=c)
	# Plot the parabola
	#print 'plot_parabola', focus, directrix, endpoints
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
		#print 'endpoints',start,end
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
from anim import *
from fortune.geometry import intersection, circle, euclidean_distance as dist, same_point


i=1
circles = []
past_circle_events = []
def animate(self,e,draw_bottoms=True, draw_circles=False):
	global i
	global circles
	global past_circle_events

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
		#print '\t', arc, self.T.predecessor(arc), self.T.sucessor(arc)
		end,start=None,None
		# plot intersections
		if self.T.predecessor(arc) and self.T.predecessor(arc).point[Y] != e.point[Y]:
			start = intersection(self.T.predecessor(arc).point,arc.point,e.point[Y])
			#plt.plot(start[0],start[1],'o',color='red')
		if self.T.sucessor(arc) and self.T.sucessor(arc).point[Y] != e.point[Y]:
			end = intersection(arc.point,self.T.sucessor(arc).point,e.point[Y])
			#plt.plot(end[0],end[1],'o',color='red')
		plot_parabola(arc.point,e.point[Y],endpoints=[start,end],color='purple')
		#print '\t\tstart = ',start,'end = ',end


	#print 'edges:'
	for h in self.edges:
		print '\t', h, h.origin, h.current(e.point[Y])
		plot_line(h.origin, h.current(e.point[Y]), color='blue')

	if not e.is_site:
		bottom, center = e.point, e.center
		radius = dist(center,bottom)
		circle=plt.Circle(center,radius,color='b',fill=False)
		fig.gca().add_artist(circle)

		past_circle_events.append(e)

	for e in past_circle_events:
		plot_points([e.point], color='green')

	for evt in self.Q:
		# Circle Event
		if not evt.is_site:
			bottom, center = evt.point, evt.center
			print 'Circle', bottom, center
			#if same_point(evt.point, e.point):
			if draw_circles:
				radius = dist(center,bottom)
				circle=plt.Circle(center,radius,color='b',fill=False)
				fig.gca().add_artist(circle)

			# plot_points([center,bottom], color='green')
			if draw_bottoms and bottom:
				plot_points([bottom], color='green')

	#plot_vertical(e.point[X])
	plot_directrix(e.point[Y])
	plot_points(self.input)
	if e.is_site:
		plot_points([e.point], color='black')
	
	fig.savefig(filename, bbox_inches='tight')
	print '============================'
	i+=1
