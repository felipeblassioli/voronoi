# -*- coding: utf-8 -*-

from . import log
from beachline import AVLBeachLine
from event import SiteEvent, CircleEvent, EventQueue
from dcel import Hedge
from geometry import Point, circle as circumcircle
	
class VoronoiDiagram(object):
	def __init__(self, pts, bounding_box=None, step_by_step=True):
		self.input = pts
		self.bounding_box = bounding_box
		self.edges = []
		self._faces = dict()
		self._compute([ Point(*p) for p in pts ],bounding_box, step_by_step)

	def _compute(self, points, bounding_box=None, step_by_step=True):
		self.T = AVLBeachLine()
		self.Q = EventQueue(points)
		
		# treat degeneracies
		prev = None
		log('EventQueue: %s' % str(self.Q))
		while not self.Q.is_empty:
			event = self.Q.pop()
			log('Popped %s id=%s' % (event,id(event)))
			if isinstance(event, SiteEvent):
				log('_handle_site_event')
				self._handle_site_event(event)

				if step_by_step:
					self.animate(event, draw_bottoms=False)
			else:
				log('_handle_circle_event')
				if event != prev or True:
					self._handle_circle_event(event)
					if step_by_step and event.is_valid:
						self.animate(event, draw_bottoms=False)
			prev = event

			log('%s' % self.T.T.dumps())
			log('beachline: %s' % self.T)
			log('-----')
		self.animate(SiteEvent((0,-100)), draw_circle_events=False)
		

	def _handle_site_event(self, evt):
		if self.T.is_empty:
			self.T.insert(evt.site)
		else:
			a = self.T.search(evt.site)

			if a.circle_event is not None:
				log('Deleting false alarm %s id=%s' % (a.circle_event,id(a.circle_event)))
				a.circle_event = None

			log('\tInserting %s into arc %s' % (evt.site, a))
			x = self.T.insert(evt.site, within=a)

			self._create_twins(x.site,a.site)

			# check the triples where this new site is the far left and far right arc.
			self.check_circle(self.T.predecessor(x),evt.site.y)
			self.check_circle(self.T.sucessor(x),evt.site.y)

	def _handle_circle_event(self, evt):
		if evt.is_valid:
			log('\tRemoving arc %s' % evt.arc)
			log('\t\tbefore removal: %s' % self.T)
			pred,suc = self.T.delete(evt.arc)
			log('\t\t after removal: %s' % self.T)

			log('\t\tChecking for deleting arcs involving %s' % evt.arc)
			if pred.circle_event is not None:
				log('\t\t\tGotta delete pred %s' % pred.circle_event)
				pred.circle_event = None
			else:
				log('\t\t\tpred: no circle_event')
			if suc.circle_event is not None:
				log('\t\t\tGotta delete suc %s' % suc.circle_event)
				suc.circle_event = None
			else:
				log('\t\t\tsuc: no circle_event')

			new_half_edge = self._create_twins(suc.site, pred.site)
 			new_half_edge._origin = evt.center
 			
 			# finish incident hedges !
 			log('\t\tUpdate incident edges')
 			log('\t\t\tpred/suc %s %s' % (pred, suc))
 			for left, right in ((pred.site, evt.arc.site), (evt.arc.site, suc.site)):
 				half_edge = None
 				log('\t\t\tleft/right %s %s' % (left, right))
 				log('\t\t\tneighbours of %s' % self._faces[left])
 				for he in self._faces[left]._iter_neighbours():
 					log('\t\t\t\t%s twin: %s' % (he, he._twin))
 					if he._twin._site == right:
 						#half_edge = he
 						he._origin = evt.center
 						log('\t\t\t Chosen to be updated was %s' % he)
 				#half_edge._origin = evt.center

 			self.check_circle(pred, evt.y)
 			self.check_circle(suc, evt.y)
		else:
			log('\t%s was previously deleted' % evt)

	def _create_twins(self, site1, site2):
		half_edge = Hedge(None, None, site1, self._faces.get(site1, None))
		half_edge._twin = Hedge(None, half_edge, site2, self._faces.get(site2, None))
		self.edges.append(half_edge)
		self._faces[site1] = half_edge
		self._faces[site2] = half_edge._twin

		log('\t\tCreated new half-edge: %s' % half_edge)
 		log('\t\t\t _faces = %s' % self._faces)
 		
		return half_edge

	def _check_circle(self, predecessor, arc, sucessor, sweep_line_y):
		log('\t\tcheck circle for triple %s %s %s' % (predecessor,arc,sucessor))
		if not predecessor or not sucessor or not arc:
			return

		a, b, c = predecessor.site, arc.site, sucessor.site
		if determinant(b - a, c - b) <= 0:
			circle = circumcircle(a,b,c)
			if circle is not None:
				self.Q.push(CircleEvent(arc,circle))

	def check_circle(self, arc, sweep_line_y):
		predecessor = self.T.predecessor(arc)
		sucessor = self.T.sucessor(arc)

		self._check_circle(predecessor,arc,sucessor,sweep_line_y)

def determinant(v1, v2):
    """Determinant of two vectors, represented by Point instances"""
    return v1.x * v2.y - v1.y * v2.x