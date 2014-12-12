# -*- coding: utf-8 -*-

DEBUG = True

def log(s):
    if DEBUG:
        print s

from .voronoi import VoronoiDiagram