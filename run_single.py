# -*- coding: utf-8 -*-

from random import randint
from fortune.anim import animate
from fortune import VoronoiDiagram

i=0
def animate2(self, e, **kwargs):
	global i

	beachline = self.T
	tree = self.T.T
	print tree

if __name__ == '__main__':
	bbox = [-5,35,-5,35]

	selected_runs = [
		#[(4, 12, 'a'), (8, 11, 'b'), (11, 10, 'c'), (5, 6.5, 'd'), (9, 5.5, 'e'), (12.5, 4.5, 'f')]
		[(19, 10), (0, 0), (15, 11), (13, 15), (1, 11), (19, 17), (4, 8), (13, 17), (19, 17), (13, 20), (9, 14), (12, 9), (14, 8), (0, 17), (1, 7), (3, 2), (12, 16), (18, 11), (20, 13)]
	]

	VoronoiDiagram.animate = animate2
	for pts in selected_runs:
		v = VoronoiDiagram(pts,bounding_box=bbox, step_by_step=True)