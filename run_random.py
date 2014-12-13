# -*- coding: utf-8 -*-

from random import randint
from fortune.anim import animate
from fortune import VoronoiDiagram

if __name__ == '__main__':
	bbox = [-5,35,-5,35]

	VoronoiDiagram.animate = animate
	for i in range(1,50):
		x = [ randint(0,20) for i in range(1,20)]
		y = [ randint(0,20) for i in range(1,20)]
		pts = zip(x,y)
		v = VoronoiDiagram(pts,bounding_box=bbox, step_by_step=False)