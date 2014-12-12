# -*- coding: utf-8 -*-

from geometry import intersection, Point, INFINITY
class Hedge(object):
    """An half-edge of the resulting graph.

    The attributes of a Hedge are used internally to define the corresponding half-edge.

    Properties:
        line: (Point, Point), a point and a vector defining the line on which the edge lies
        left_site: Point, the site on the left of the edge
        right_site: Point, the site on the right of the edge
        vertex_from: Point, the start point of the edge, or None if the edge is not bounded
        vertex_to: Point, the end point of the edge, or None if the edge is not bounded
    """
    def __init__(self, origin, twin, site, next_edge):  #pylint: disable=W0231
        self._origin = origin
        self._twin = twin
        self._site = site
        self._next_edge = next_edge
        self._cut_origin = None

    def __repr__(self):
        return "%s(left_site=%r, right_site=%r)" % (
            self.__class__.__name__, self.left_site, self.right_site)

    def _iter_neighbours(self):
        he = self
        while he is not None:
            yield he
            he = he._next_edge

    @property
    def line(self):
        """Returns p, v such that p is the point of the line lying in the middle of the two sites
        and v is a vector directing the line in the direction that keeps the left site on the left"""
        diff = self.right_site - self.left_site
        return (self.left_site + self.right_site) / 2.0, Point(-diff.y, diff.x)

    @property
    def line2(self):
        """Returns p, v such that p is the point of the line lying in the middle of the two sites
        and v is a vector directing the line in the direction that keeps the left site on the left"""
        diff = self.right_site - self.left_site
        return (self.left_site + self.right_site) / 2.0, diff

    @property
    def left_site(self):
        return self._site

    @property
    def right_site(self):
        return self._twin._site

    from geometry import intersection
    def vertex_from(self,y):
        if self._origin is not None:
            return self._origin
        i = intersection(self.left_site, self.right_site, y)
        # they are collinear
        if i[1] == INFINITY and i[0] == INFINITY:
            x = (self.left_site.x + self.right_site.x) / 2.0
            return Point(x,INFINITY)
        return Point(i[0],i[1])
        #return self._cut_origin

    def vertex_to(self,y):
        if self._origin is not None:
        	pass
            #print 'hi', self, 'to', self._twin
            #return intersection(self.left_site, self.right_site, y)
        return self._twin.vertex_from(y)

    def trim(self, x_min, x_max, y_min, y_max):
        """Trim an infinite edge to make it fit in a bounding box"""
        x0, y0 = self.line[0].x, self.line[0].y
        for a, b, obj in (
            (-self.line[1].x, -self.line[1].y, self),
            (self.line[1].x, self.line[1].y, self._twin),):
            if getattr(obj, '_origin') is None:
                x_limit = x_max if a > 0 else x_min
                y_limit = y_max if b > 0 else y_min
                if a != 0:
                    t = (x_limit - x0) / a
                    _y = y0 + b * t
                    if y_min <= _y <= y_max:
                        setattr(obj, '_cut_origin', Point(x_limit, _y))
                        continue
                assert b != 0
                t = (y_limit - y0) / b
                _x = x0 + a * t
                assert x_min <= _x <= x_max
                setattr(obj, '_cut_origin', Point(_x, y_limit))

