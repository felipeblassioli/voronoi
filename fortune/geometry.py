from math import sqrt

X,Y=0,1


def _point(x,a,b,c):
	return (x, a*(x**2)+b*x+c)

def vertex(x,y,directrix):
	return (x, (y + directrix) / 2.0)

def solve(a,b,c):
	sols = []
	d = b**2-4*a*c # discriminant

	if d < 0:
		print ("This equation has no real solution")
	elif d == 0:
		x = (-b+sqrt(b**2-4*a*c))/2*a
		# print ("This equation has one solutions: "), x
		sols.append(x)
	else:
		x1 = (-b+sqrt((b**2)-(4*(a*c))))/(2*a)
		x2 = (-b-sqrt((b**2)-(4*(a*c))))/(2*a)
		# print ("This equation has two solutions: ", x1, " or", x2)
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

	#print p,A

	return A,B,C

def intersection(p,q,directrix):
	"""Returns the points of intersection of the two whose focuses are p and q."""
	a,b,c = coefficients(p,directrix)
	d,e,f = coefficients(q,directrix)

	#print 'intersection', p, q, directrix
	if p[Y] == q[Y]:
		x = (p[X] + q[X]) / 2.0
	elif q[Y] == directrix:
		x = q[X]
		parabola = (a,b,c)
	elif p[Y] == directrix:
		x = p[X]
		parabola = (d,e,f)
	else:
		sols = solve(a-d,b-e,c-f) 
		#print 'sols', sols
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
	if G == 0: return None, None

	center = (D*E-B*F)/G, (A*F-C*E)/G;
	radius = sqrt((a[X] - center[X])**2 + (a[Y] - center[Y])**2)
	bottom = center[X], center[Y] - radius

	return bottom, center

def euclidean_distance(p,q):
	return sqrt( (p[X] - q[X])**2 + (p[Y]-q[Y])**2 )

def same_point(p,q,epsilon=0.00001):
	_eq = lambda a, b, t: abs(a - b) < t

	return _eq(p[X],q[X],epsilon) and _eq(p[Y],q[Y], epsilon)


if __name__ == '__main__':
	print intersection((4,12),(8,11),10)
	print intersection((8,11),(4,12),10)

	print intersection((8,11),(11,10),6.5)
	print intersection((11,10),(8,11),6.5)