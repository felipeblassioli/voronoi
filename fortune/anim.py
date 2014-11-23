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



from geometry import vertex, coefficients
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
	if focus[Y] == directrix:
		if endpoints[0]:
			end = endpoints[0][Y]
		elif endpoints[1]:
			end = endpoints[1][Y]
		else:
			end = directrix
		
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