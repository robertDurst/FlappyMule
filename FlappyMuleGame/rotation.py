import physics_objects as pho
import math
import graphics as gr

class RotatingBlock(pho.Thing ):
	def __init__(self,win,x0,y0,width,height,Ax = None,Ay = None):
		pho.Thing.__init__(self,win,"rotating block",position = [x0,y0])
		self.width = width
		self.height = height
		self.points = [[-width/2.0, -height/2.0], [width/2.0, -height/2.0], [width/2.0, height/2.0], [-width/2.0, height/2.0]]
		self.angle = 0.0
		self.rvel = 0.0
		self.drawn = False
		self.color = None
		if Ax == None and Ay == None:
			self.anchor = [x0,y0]
		else:
			self.anchor = [Ax,Ay]
	
	def getHeight(self):
		return self.height
	
	def getWidth(self):
		return self.width
		
	def getAngle(self):
		return self.angle
	
	def setAngle(self,a):
		self.angle = a
		
	def getAnchor(self):
		return self.anchor
	
	def setAnchor(self, a):
		self.anchor = a
	
	def getRotVelocity(self):
		return self.rvel
	
	def setRotVelocity(self,r):
		self.rvel = r
	
	def draw(self):
		for thing in self.vis:
			thing.undraw()
		self.render()
		for thing in self.vis:
			thing.draw(self.win)
			thing.setFill(self.color)
			thing.setOutline(self.color)
		self.drawn = True
	
	def render(self):
		angle = math.pi*self.angle/180
		cth = math.cos(angle)
		sth = math.sin(angle)
		pts = []
		for vertex in self.points:
			xt = (vertex[0]+ self.position[0]) - self.anchor[0]
			yt = (vertex[1]+ self.position[1]) - self.anchor[1]
			xtt = cth *xt - sth * yt
			ytt = sth *xt + cth *yt
			xf = xtt + self.anchor[0]
			yf = ytt + self.anchor[1]
			pts.append(gr.Point(self.scale * xf,self.win.getHeight() - self.scale * yf))
		self.vis = [(gr.Polygon(pts[0],pts[1],pts[2],pts[3]))]
	
	def rotate(self, bob):
		self.angle += bob
		if self.drawn:
			self.draw()
	
	def setColor(self,color):
		self.color = color
	
	def update(self,dt):
		da = self.rvel*dt
		if da != 0:
			self.rotate(da)
		pho.Thing.update(self,dt)
			