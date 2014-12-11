from fortune import Voronoi
#from anim import animate
from anim import animate
if __name__ == '__main__':
	v = Voronoi()
	Voronoi.animate = animate
	#pts = [(1,1,'p'),(2,2,'q'),(3,0.5,'r')]
	x = [4,8,11,5,9,12.5]
	y = [12,11,10,6.5,5.5,4.5]
	label = ['a','b','c','d','e','f']
	# x = [4,3,11]
	# y = [12,3,6]
	# label = ['a','b','c']parabola = (a,b,c)

	#Three colinear points
	# x = [10,5,0]
	# y = [11,11,11]
	# label = ['b','c','a']

	# Two colinear points
	# x = [8,11,13]
	# y = [11,9,9]
	# label = ['b','c','d']

	#Three colinear points
	# x = [4,8,11,14]
	# y = [12,11,11,11]
	# label = ['a','b','c','d']

	#x = [4,8,11,5]
	#y = [12,11,10,6.5]
	#label = ['a','b','c','d']
	pts = zip(x,y,label)
	edges = v(pts)

	print '\nEdges:'
	for e in edges:
		print '\t', e
	#print edges	