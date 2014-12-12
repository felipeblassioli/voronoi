from math import sqrt

X,Y=0,1
INFINITY = 9999

def _point(x,a,b,c):
	return (x, a*(x**2)+b*x+c)

def vertex(x,y,directrix):
	return (x, (y + directrix) / 2.0)

def solve(a,b,c):
	sols = []
	d = b**2-4*a*c # discriminant

	if d < 0:
		print 'discriminant is < 0!'
	elif d == 0:
		x = (-b+sqrt(b**2-4*a*c))/2*a
		sols.append(x)
	else:
		x1 = (-b+sqrt((b**2)-(4*(a*c))))/(2*a)
		x2 = (-b-sqrt((b**2)-(4*(a*c))))/(2*a)
		sols.append(x1)
		sols.append(x2)
	return sols
	
def coefficients(focus, directrix):
	"""
	Variables:
	  - h and k are the coordinates of the vertex
	  - p is the distance from the vertex to the directrix
	"""
	h,k = vertex(focus[X],focus[Y],directrix)
	p = abs(k - directrix)

	if p == 0:
		# This parabola should be a vertical line
		# This happens when focus[Y] == directrix
		A,B,C=0,0,focus[X]
	else:
		A = 1.0 / (4*p)
		B = -1*h / (2.0*p)
		C = (h**2 / (4.0*p)) + k


	return A,B,C

def intersection(p,q,directrix):
	"""Returns the points of intersection of the two whose focuses are p and q."""
	a,b,c = coefficients(p,directrix)
	d,e,f = coefficients(q,directrix)

	# print 'intersection', p,q,directrix
	# print '\t',a,b,c
	# print '\t',d,e,f

	if p[Y] == q[Y]:
		x = (p[X] + q[X]) / 2.0
		# Fucking degenerated cases: WE need help from hedge.vertex_from to to deal with this
		if p[X] > q[X]:
			return INFINITY,INFINITY
		if p[Y] == directrix:
			return x, directrix
		parabola = (a,b,c)
		#return x,directrix
		#return None
	elif q[Y] == directrix:
		x = q[X]
		parabola = (a,b,c)
	elif p[Y] == directrix:
		x = p[X]
		parabola = (d,e,f)
	else:
		if a == d:
			#print 'Houston we got a problem'
			x = (f-c)/(b-e)
		else:
			sols = solve(a-d,b-e,c-f) 
			# we get the rightmost point
			x = sols[0]
		parabola = (a,b,c)
	# plug-back the results in the parabola
	return _point(x,*parabola)

def circle(a,b,c):
	"""Find the rightmost point on the circle through a,b,c."""
	# Algorithm from O'Rourke 2ed p. 189.
	A = b[X] - a[X]  
	B = b[Y] - a[Y]
	C = c[X] - a[X]  
	D = c[Y] - a[Y]
	E = A*(a[X]+b[X]) + B*(a[Y]+b[Y])
	F = C*(a[X]+c[X]) + D*(a[Y]+c[Y])
	G = 2.0*(A*(c[Y]-b[Y]) - B*(c[X]-b[X]))

	# Points are co-linear and not finite radius exists
	if G == 0: return None

	center = (D*E-B*F)/G, (A*F-C*E)/G;
	radius = sqrt((a[X] - center[X])**2 + (a[Y] - center[Y])**2)
	bottom = center[X], center[Y] - radius

	#return bottom, center
	return center, radius

def euclidean_distance(p,q):
	return sqrt( (p[X] - q[X])**2 + (p[Y]-q[Y])**2 )

def same_point(p,q,epsilon=0.00001):
	_eq = lambda a, b, t: abs(a - b) < t

	return _eq(p[X],q[X],epsilon) and _eq(p[Y],q[Y], epsilon)

from collections import namedtuple
from math import sqrt
_Point = namedtuple('Point', ['x', 'y', 'label'])
class Point(_Point):
	"""A point in the plane

	Attributes:
	x: float, the x coordinate
	y: float, the y coordinate

	Properties:
	square: float, the square of the norm of the vector (x, y)
	norm: float, the norm of the vector (x, y)
	"""
	def __new__(_cls, x, y, label=None):
		'Create a new instance of Point(x, y)'
		return _Point.__new__(_cls, x, y, label)

	def __repr__(self):
		if self.label is not None:
			return "%s(%r, %r, %r)" % (self.__class__.__name__, self.x, self.y, self.label)
		return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

	def __add__(self, other):
		return self.__class__(self.x + other.x, self.y + other.y)

	def __neg__(self):
		return self.__class__(-self.x, -self.y)

	def __sub__(self, other):
		return self + (-other)

	def __div__(self, other):
		return self.__class__(self.x / other, self.y / other)

	def __cmp__(self, other):
		if other is None:
			return False
			
		cmp_x = cmp(self.x, other.x)
		if cmp_x != 0:
			return cmp_x
		return cmp(self.y, other.y)

	def __abs__(self):
		return self.norm

	@property
	def square(self):
		return self.x**2 + self.y**2

	@property
	def norm(self):
		return sqrt(self.square)