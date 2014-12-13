# -*- coding: utf-8 -*-

import Tkinter
from Tkconstants import *

from Tkinter import Frame, Button, Label, OptionMenu, StringVar, Canvas


class FileListOptionMenu(OptionMenu):
	def __init__(self, master):
		self.var = StringVar(master)
		self.var.set('Selecione um arquivo')

		data_files = sorted(_list_data_files())
		OptionMenu.__init__(self, master, self.var, *data_files)
		# self.config(font=('calibri',(10)),bg='white',width=12)
		# self['menu'].config(font=('calibri',(10)),bg='white')

	@property
	def selected(self):
		"""Returns the current selected data file"""
		return self.var.get()

from fortune.geometry import vertex, coefficients, Point
def parabola (list_x, focus, directrix):
	A,B,C = coefficients(focus,directrix)
	if A == 0:
		return None
	return [ A*(x**2) + B*x + C for x in list_x ]

def _parabola(x, focus, directrix):
	A,B,C = coefficients(focus,directrix)
	if A == 0:
		return None
	return A*(x**2) + B*x + C

def linspace(start,end, total):
	dx = float((end - start)) / total
	x = start
	while x <= end:
		yield x
		x += dx

CANVAS_START = 0 
CANVAS_WIDTH = 10000
CANVAS_HEIGHT = 10000
class PaperMixin(object):

	def plot_circle(self, x, y, r, **kwargs):
		x = self.canvas.canvasx(x)
		y = self.canvas.canvasy(y)

		return self.canvas.create_oval(x-r, y-r, x+r, y+r, **kwargs)

	def plot_parabola(self, focus, directrix, endpoints=None, color='purple'):
		#print 'plot_parabola', focus, directrix, endpoints
		a, b = focus[0], focus[1]

		# Plot the parabola
		if focus[1] == directrix:
			if endpoints[0]:
				end = endpoints[0][1]
			elif endpoints[1]:
				end = endpoints[1][1]
			else:
				end = CANVAS_HEIGHT
			
			#plt.plot([a,a],[directrix,end],'b-',color=color,linewidth=2)
		else:
			start = endpoints[0][0] if endpoints[0] is not None else CANVAS_START
			end = endpoints[1][0] if endpoints[1] is not None else CANVAS_WIDTH
			#print '\tplot focus', focus, start,end
			if start != CANVAS_START:
				#pts = pylab.linspace(-10,start,num=240)
				pass
				#print '\t\tstart: -10 to ',start
				#plt.plot(pts, parabola(pts,f,directrix), '-',color='#e3e3e3',linewidth=1)

			if end != CANVAS_WIDTH:
				pass
				#pts = pylab.linspace(end,width,num=240)
				#print '\t\tend: ',end,'to',width
				#plt.plot(pts, parabola(pts,f,directrix), '-',color='#e3e3e3',linewidth=1)

			#pts = pylab.linspace(start,end,num=240)
			f = lambda x: _parabola(x,focus,directrix)
			prev = start
			for x in linspace(start,end,240):
				p = (prev,f(prev))
				q = (x,f(x))
				prev = x
				self.plot_line(p,q,color=color,linewidth=2)
			#plt.plot(pts, parabola(pts,f,directrix), '-',color=color,linewidth=2)

	def plot_points(self, pts, **kwargs):
		color = kwargs.pop('color', 'red')
		for p in pts:
			self.plot_circle(p[0],p[1],5,fill=color)

	def plot_line(self, a,b,**kwargs):
		linewidth = kwargs.pop('linewidth', 2)
		color = kwargs.pop('color', 'blue')
		x0,y0 = self.canvas.canvasx(a[0]),self.canvas.canvasy(a[1])
		x1,y1 = self.canvas.canvasx(b[0]),self.canvas.canvasy(b[1])

		canvas = self.canvas
		lineto_id = canvas.create_line (x0,y0,x1,y1,fill=color, width=linewidth)
		return lineto_id

	def plot_horizontal_line(self, y, **kwargs):
		start = (CANVAS_START,y)
		end = CANVAS_WIDTH,y
		self.plot_line(start,end, **kwargs)

def parse_file(selected_file):
	with open('data/%s' % selected_file) as f:
		lines = f.read().split('\n')
		pts = []
		for l in lines:
			try:
				c = [ float(c)*25.0 for c in l.split(' ') ]
				x,y = c[0], c[1]
				p = (x+100,y)
				#p = (x,-y+600)
				pts.append(p)
			except:
				print 'Warning: Failed to parse line=[%s]' % l
		return pts

from fortune import VoronoiDiagram

from copy import deepcopy, copy
class CachedVoronoiDiagram(VoronoiDiagram):
	def __init__(self, *args, **kwargs):
		self.steps = []
		kwargs['step_by_step'] = True
		super(CachedVoronoiDiagram, self).__init__(*args, **kwargs)

	def animate(self,e,draw_bottoms=True, draw_circles=False, draw_circle_events=True):
		step = dict(
			beachline = deepcopy(self.T),
			event_queue = deepcopy(self.Q),
			hedges = deepcopy(self.edges),
			e = deepcopy(e)
		)
		self.steps.append(step)

from fortune.geometry import intersection, INFINITY
class AnimatedMixin(PaperMixin):

	def start(self):
		self.past_circle_events = []
		self.current_step = 0
		selected_file = self.filelist.selected
		self.pts = parse_file(selected_file)

		cached = CachedVoronoiDiagram(self.pts,bounding_box=[0,200,0,200], step_by_step=True)
		self.steps = cached.steps
		self._draw_step(**self.steps[0])


	def _draw_beachline(self, e, beachline):
		isInfinity = lambda x: x is not None and x[0] == INFINITY and x[1] == INFINITY
		#print beachline.T.dumps()
		for arc in beachline:
			end,start=None,None
			pred,suc = beachline.predecessor(arc), beachline.sucessor(arc)
			#print pred, arc, suc
			if pred is not None:
				start = intersection(pred.site,arc.site,e.y)
				# if start[0] == INFINITY and start[1] == INFINITY:
				# 	start = None
			if suc is not None:
				end = intersection(arc.site,suc.site,e.y)
				# if end[0] == INFINITY and end[1] == INFINITY:
				# 	end = None
			if isInfinity(start) and isInfinity(end) or isInfinity(start) and end is None:
				continue
			elif isInfinity(start):
				start = None
			elif isInfinity(end):
				end = None
			# print 'arc is',arc, 'intersections are',start,end, 'pred/suc', beachline.predecessor(arc),beachline.sucessor(arc)
			self.plot_parabola(arc.site,e.y,endpoints=[start,end],color='purple')

	def _draw_hedges(self, e, hedges):
		for h in hedges:
			self.plot_line(h.vertex_from(e.y), h.vertex_to(e.y), color='blue')

	def _draw_circle_events(self, e, event_queue, draw_bottoms=True, draw_circles=False, draw_past_circles=False):
		past_circle_events = self.past_circle_events
		if not e.is_site:
			bottom, center, radius = e.bottom, e.center, e.radius

			self.plot_circle(center.x, center.y, radius, outline='blue')
			self.plot_points([bottom], color='green')

		
	def _draw_step(self, e, beachline, event_queue, hedges, **kwargs):
		self.canvas.delete("all")

		# Draw directrix
		self.plot_horizontal_line(e.y, color='red')

		self.plot_points(self.pts)
		self._draw_beachline(e,beachline)
		self._draw_hedges(e, hedges)
		self._draw_circle_events(e, event_queue)

			
		if e.is_site:
			self.plot_points([e.site], color='white')


	def prev(self):
		self.current_step -= 1
		self._draw_step(**self.steps[self.current_step])

	def next(self):
		self.current_step += 1
		self._draw_step(**self.steps[self.current_step])


class MainWindow(AnimatedMixin):
	def __init__(self):
		self._init_ui_components()
		self._create_canvas()

	def _create_canvas(self):
		w = Canvas(tk, width=1000, height=1000, background="black")
		w.pack(side=TOP,fill=BOTH,expand=True)
		#w.pack(side=TOP)


		self.canvas = w
		_cx = self.canvas.canvasx
		_cy = self.canvas.canvasy

		#self.canvas.canvasx
		self.canvas.canvasy = lambda y: -_cy(y) + 600

	def _init_ui_components(self):
		# Containers
		left_frame = Frame(tk)
		right_frame = Frame(tk)
		control_frame = Frame(right_frame)

		left_frame.pack(side=LEFT, fill=BOTH)
		right_frame.pack(side=RIGHT, fill=BOTH)
		control_frame.pack(side=BOTTOM, fill=X, expand=False)

		# File list
		self.filelist = FileListOptionMenu(left_frame)
		self.filelist.pack(side=TOP,fill=X)

		# frame = Frame(tk, relief=RIDGE, borderwidth=2)
		# frame.pack(fill=BOTH,expand=1)

		# Labels
		# lb_filelist = Label(left_frame, text="Hello, World")
		# lb_filelist.pack(fill=X)

		# Buttons
		bt_next = Button(control_frame,text='Next',command=self.next)
		bt_prev = Button(control_frame,text='Prev',command=self.prev)
		bt_run = Button(left_frame,text='Start',command=self.start)

		bt_next.pack(side=RIGHT)
		bt_prev.pack(side=LEFT)
		bt_run.pack(side=BOTTOM,fill=X,expand=True)

		# bt_exit = Button(left_frame,text="Exit",command=tk.destroy)
		# bt_exit.pack(side=BOTTOM)



from os import listdir
def _list_data_files():
	return listdir('data')

if __name__ == '__main__':
	tk = Tkinter.Tk()

	main_window = MainWindow()
	#_init_ui_components()

	tk.mainloop()

