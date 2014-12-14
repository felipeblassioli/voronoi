# -*- coding: utf-8 -

i = 0
def animate(self, e, **kwargs):
	global i

	beachline = self.T
	tree = self.T.T
	print tree
	if i == 2:
		for n in tree:
			print '\t', n, n.key(e.y)
		print tree.dumps()

	print 
	i+=1
	if i == 3:
		exit(0)

from fortune import VoronoiDiagram
from fortune.beachline import AVLBeachLine
bbox = [-5,35,-5,35]
pts = [(4, 12, 'a'), (8, 11, 'b'), (11, 10, 'c'), (5, 6.5, 'd'), (9, 5.5, 'e'), (12.5, 4.5, 'f')]

# VoronoiDiagram.animate = animate
# v = VoronoiDiagram(pts,bounding_box=bbox, step_by_step=True)

tree = AVLBeachLine()
a,b,c = (4, 12, 'a'), (8, 11, 'b'), (11, 10, 'c')

tree.insert(a)
print tree.T.dumps()

x = tree.search(b)
tree.insert(b, within=x)
print tree.T.dumps()


x = tree.search(c)
print 'x is', x
tree.insert(c, within=x)
print 'x now is', x
print tree.T.dumps()

p = x.parent
tree.T.left_rotate(x)
print x, x.parent
tree.T.right_rotate(p)
tree.T.left_rotate(tree.T._root)
print tree.T.dumps()