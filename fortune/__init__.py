# -*- coding: utf-8 -*-

DEBUG = False

def log(s):
    if DEBUG:
        print s

from .voronoi import VoronoiDiagram