# -*- coding: utf-8 -*-

from random import randint
from fortune.anim import animate
from fortune import VoronoiDiagram

if __name__ == '__main__':
	bbox = [-5,35,-5,35]

	degenerate_runs = [
		[(8, 11), (10, 11), (12, 11)],
		[(8, 11, 'a'), (11, 9, 'b'), (13, 9, 'c')],
		[(8, 11), (11, 9), (13, 9), (12, 7), (15, 9), (17, 9), (19, 9), (21, 9), (15, 6), (17, 6), (19, 6), (21, 6)],
		[(8, 11), (10, 11), (12, 11), (14, 11), (8, 8), (10, 8), (12, 8), (14, 8), (8, 6), (10, 6), (12, 6), (14, 6)],
		[(5.0, 0.0), (3.5355339059327378, 3.5355339059327373), (3.061616997868383e-16, 5.0), (-3.5355339059327373, 3.5355339059327378), (-5.0, 6.123233995736766e-16)]
	]

	VoronoiDiagram.animate = animate
	for pts in degenerate_runs:
		v = VoronoiDiagram(pts,bounding_box=bbox, step_by_step=False)