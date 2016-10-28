#Robert Durst
#CS151
#Project9
#Recreate Project 8 physics simulation with inheritance
#	call as physics_objects.py
import graphics as gr
import math
import collision as coll
import random
import time


score = 0

class Thing():
	def __init__(self,win, the_type,radius = 1, position = [0,0], mass = 1):
		self.type = the_type
		self.mass = mass
		self.radius = radius
		self.position = position[:]
		self.velocity = [0,0]
		self.acceleration = [0,0]
		self.force = [0,0]
		self.elasticity = 1
		self.scale = 10
		self.win = win
		self.vis = []

	def undraw(self):
		for object in self.vis:
			object.undraw()
	
	def Color(self,color):
		self.vis[0].setFill(color)
		self.vis[0].setOutline(color)
	def getType(self):
		return self.type
	def getVelocity(self): # returns a 2-element tuple with the x and y velocities.
		return self.velocity[:]
	def setVelocity(self, v): # v is a 2-element list with the new x and y velocities
		self.velocity[0] = v[0]
		self.velocity[1] = v[1]
	def getAcceleration(self): # returns a 2-element tuple with the x and y acceleration values.
		return self.acceleration
	def setAcceleration(self, a): # a is a 2-element list with the new x and y accelerations.
		self.acceleration[0] = a[0]
		self.acceleration[1] = a[1]
	def getForce(self): # returns a 2-element tuple with the current x and y force values.
		return self.force
	def setForce(self, f): # f is a 2-element list with the new x and y force values.
		self.force[0] = f[0]
		self.force[1] = f[1]
	def getMass(self): # Returns the mass of the object as a scalar value
		return self.mass
	def setMass(self, m): # m is the new mass of the object
		self.mass = m
	def getRadius(self):
		return self.radius
	def setRadius(self,r):
		self.radius = r
	def getMass(self): # Returns the mass of the object as a scalar value
		return self.mass
	def setMass(self, m): # m is the new mass of the object
		self.mass = m
	def getPosition(self): # returns a 2-element tuple with the x, y position.
		return self.position
	def setPosition(self, p): # p is a 2-element list with the new x,y values

		for thing in self.vis:
			dx = (p[0] - self.position[0])*self.scale
			dy = self.win.getHeight() - (self.position[1] - p[1])*self.scale
			self.position = p[:]
			thing.move(dx,dy)

	def setScale(self, s):
		self.scale = s
	def getScale(self):
		return self.scale
	def setElasticity(self, e):
		self.elasticity = e
	def getElasticity(self):
		return self.elasticity
	def draw(self):
		for c in self.vis:
			c.draw(self.win)
	def update(self, dt):
		self.position[0] += self.velocity[0]*dt
		self.position[1] += self.velocity[1]*dt

		dx = self.velocity[0]*self.scale*dt
		dy = -self.velocity[1]*self.scale*dt
	
		for x in self.vis:
			x.move(dx,dy)

		
		self.velocity[0] += self.acceleration[0]*dt
		self.velocity[1] += self.acceleration[1]*dt
		
		self.velocity[0] += (self.force[0]*dt)/self.mass
		self.velocity[1] += (self.force[1]*dt)/self.mass
	
	
		self.velocity[0] *= 0.999
		self.velocity[1] *= 0.999
		return [dx,dy]
class Ball(Thing):
	def __init__(self,win, x0, y0, radius = 1):
		Thing.__init__(self, win, "ball", position = [x0, y0])
		self.radius = radius
		self.vis = [gr.Circle(gr.Point(self.position[0]*self.scale,win.getHeight()-self.position[1]*self.scale),self.radius*self.scale)]	

class Floor(Thing):
	def __init__(self,win,x0,y0,width,height):
		Thing.__init__(self,win, "floor", position = [x0,y0])
		self.width = width
		self.height = height
		length = self.width
		thickness = self.height
		x = x0*self.scale
		y = self.win.getHeight()-(y0+thickness/2)*self.scale
		self.vis = [gr.Rectangle(gr.Point( x,y), gr.Point((x0 + length)*self.scale, self.win.getHeight() - (y0 - thickness/2)*self.scale)) ]
	
	def getHeight(self):
		return self.height
	def getWidth(self):
		return self.width
class Wall(Thing):
	def __init__(self,win,x,y,width,height):
		Thing.__init__(self,win, "wall", position = [x,y])
		self.width = width
		self.height = height
		thickness = self.width
		length = self.height
		self.vis = [gr.Rectangle(gr.Point ((x-thickness/2)*self.scale, self.win.getHeight()-y*self.scale), gr.Point( ((x+thickness/2)*self.scale) , self.win.getHeight()-(y+ length)*self.scale)) ]
	
	def getHeight(self):
		return self.height
	def getWidth(self):
		return self.width
		
	def setHeight(self, h):
		self.height = h

class Block(Thing):
	def __init__(self,win,x0,y0,width,height):
		Thing.__init__(self,win, "block", position = [x0,y0])
		self.width = width
		self.height = height
		self.vis = [gr.Rectangle(gr.Point((x0-self.width/2)*self.scale,win.getHeight()-(y0+self.height/2)*self.scale),gr.Point((x0+self.width/2)*self.scale,win.getHeight()-(y0-self.height/2)*self.scale),)]
			
	def getHeight(self):
		return self.height
	def getWidth(self):
		return self.width
	def setHeight(self,h):
		self.height = h
	def setWidth(self,w):
		self.width = w
	def updateShooter(self):
		self.vis.undraw()
	
def buildGame(win):
	wall_left_side = Wall(win,10,0,2,90)
	wall_right_side = Wall(win,78,0,2,90)
	right_ball_cut = Wall(win,84,0,10,90)
	left_ball_cut = Wall(win,4,0,10,90)
	ceiling = Floor(win,10,89,68,2)
	bot_floor_left = Block(win,21,1,25,2)
	bot_floor_right = Block(win,65,1,25,2)
	left_launch_wall = Block(win,71,32,1,60)
	top_right_circle = Ball(win,78,88,8)
	top_left_circle = Ball(win,12,88,8)
	mid_ball_bumper = Ball(win,43,62,2.5)
	top_right_ball_bumper = Ball(win,53,72,2.5)
	bot_right_ball_bumper = Ball(win,53,52,2.5)
	top_left_ball_bumper = Ball(win,33,72,2.5)
	bot_left_ball_bumper = Ball(win,33,52,2.5)
	left_mid_bumper = Block(win,13,42,5,15)
	right_mid_bumper = Block(win,69,42,5,15)
	bumper_below_mid_bumper_ball_left = Ball(win,13,28,2)
	bumper_below_mid_bumper_ball_right = Ball(win,69,28,2)
	triangle_right_1 = Block(win,21,2,21,2)
	triangle_right_2 = Block(win,19,4,18,2)
	triangle_right_3 = Block(win,17,6,15,2)
	triangle_right_4 = Block(win,16,8,11,2)
	triangle_right_5 = Block(win,13.5,10,9,2)
	triangle_right_6 = Block(win,12,12,5,2)
	triangle_right_7 = Block(win,12,13,3,1.5)
	triangle_left_1 = Block(win,63,3,15,2)
	triangle_left_2 = Block(win,61,5,4,2)
	triangle_left_3 = Block(win,63.5,7,4,2)
	triangle_left_4 = Block(win,66,9,4,2)
	triangle_left_5 = Block(win,69,11,4,2)
	triangle_left_6 = Block(win,70.25,13,1.5,2)
	paddle_right = Block(win,52,12,2,8)
	paddle_left = Block(win,34,12,2,8)

	
	wall_left_side.Color("Grey")
	wall_right_side.Color("Grey")
	ceiling.Color("Grey")
	bot_floor_left.Color("Grey")
	bot_floor_right.Color("Grey")
	left_launch_wall.Color("Grey")
	top_right_circle.Color("Green")
	right_ball_cut.Color("Black")
	top_left_circle.Color("Green")
	left_ball_cut.Color("Black")
	mid_ball_bumper.Color("Magenta")
	top_right_ball_bumper.Color("Red")
	top_left_ball_bumper.Color("Red")
	bot_right_ball_bumper.Color("Red")
	bot_left_ball_bumper.Color("Red")
	left_mid_bumper.Color("Purple")
	right_mid_bumper.Color("Purple")
	bumper_below_mid_bumper_ball_left.Color("Red")
	bumper_below_mid_bumper_ball_right.Color("Red")
	triangle_right_1.Color("Grey")
	triangle_right_2.Color("Grey")
	triangle_right_3.Color("Grey")
	triangle_right_4.Color("Grey")
	triangle_right_5.Color("Grey")
	triangle_right_6.Color("Grey")
	triangle_right_7.Color("Grey")
	triangle_left_1.Color("Grey")
	triangle_left_2.Color("Grey")
	triangle_left_3.Color("Grey")
	triangle_left_4.Color("Grey")
	triangle_left_5.Color("Grey")
	triangle_left_6.Color("Black")
	paddle_right.Color("Gold")
	paddle_left.Color("Gold")

	
	


	
	OBJList = [bumper_below_mid_bumper_ball_right,bumper_below_mid_bumper_ball_left,top_right_circle,top_left_circle,wall_left_side,wall_right_side,ceiling,
	bot_floor_left,bot_floor_right,left_launch_wall,right_ball_cut,left_ball_cut,
	mid_ball_bumper,bot_left_ball_bumper,top_left_ball_bumper,bot_right_ball_bumper,
	top_right_ball_bumper,left_mid_bumper,right_mid_bumper,
	triangle_right_1,triangle_right_2,triangle_right_3,triangle_right_4,triangle_right_5,triangle_right_6,triangle_right_7,
	triangle_left_1,triangle_left_2,triangle_left_3,triangle_left_4,triangle_left_5,triangle_left_6,

	paddle_left, paddle_right]
	

	
	
	for object in OBJList:
		object.draw()
	

	
	triangle_left = gr.Polygon(gr.Point(110,750),gr.Point(110,880),gr.Point(330,880))
	triangle_left.setFill("Yellow")
	triangle_left.setOutline("Yellow")
	triangle_left.draw(win)
	triangle_right = gr.Polygon(gr.Point(710,750),gr.Point(710,880),gr.Point(530,880))
	triangle_right.setFill("Yellow")
	triangle_right.setOutline("Yellow")
	triangle_right.draw(win)
	
	return OBJList
	
def launch( ball, x0, y0, dx, dy, forceMag ):

	d = math.sqrt(dx*dx + dy*dy)
	dx /= d
	dy /= d

	fx = dx * forceMag
	fy = dy * forceMag

	ball.setElasticity( 1 )
	ball.setPosition( [x0, y0] )
	ball.setForce( [fx, fy] )
	ball.setVelocity([0,50])

	for i in range(5):
		ball.update(0.02)

	ball.setForce( (0., 0.) )
	ball.setAcceleration( (0., -1.) )
	
			
def test():
	win = gr.GraphWin( 'Pinball', 1000, 1200, False )
	block = Block(win, 25,25,5,5)
	block.draw()
	while win.checkMouse() == None:
		v=0
		
# main code
def main():
	
	score = 0
	balls = 3


	win = gr.GraphWin( 'Pinball', 1200, 900, False )
	win.setBackground("Black")
	obstacles = buildGame(win)
	ball = Ball(win,74,8,2)
	ball.vis[0].setFill("White")
	ball.draw()
	P = gr.Text(gr.Point(1000,200),"P")
	P.setFace('arial')
	P.setStyle("bold")
	P.setSize(36)
	P.setTextColor("White")
	P.draw(win)
	I = gr.Text(gr.Point(1000,240),"I")
	I.setFace('arial')
	I.setStyle("bold")
	I.setSize(36)
	I.setTextColor("White")
	I.draw(win)
	N = gr.Text(gr.Point(1000,280),"N")
	N.setFace('arial')
	N.setStyle("bold")
	N.setSize(36)
	N.setTextColor("White")
	N.draw(win)
	B = gr.Text(gr.Point(1000,320),"B")
	B.setFace('arial')
	B.setStyle("bold")
	B.setSize(36)
	B.setTextColor("White")
	B.draw(win)
	A = gr.Text(gr.Point(1000,360),"A")
	A.setFace('arial')
	A.setStyle("bold")
	A.setSize(36)
	A.setTextColor("White")
	A.draw(win)
	L = gr.Text(gr.Point(1000,400),"L")
	L.setFace('arial')
	L.setStyle("bold")
	L.setSize(36)
	L.setTextColor("White")
	L.draw(win)
	L1 = gr.Text(gr.Point(1000,440),"L")
	L1.setFace('arial')
	L1.setStyle("bold")
	L1.setSize(36)
	L1.setTextColor("White")
	L1.draw(win)
	
	A1 = gr.Text(gr.Point(1000,875),"Click to move paddles.")
	A1.setFace('arial')
	A1.setStyle("bold")
	A1.setSize(20)
	A1.setTextColor("White")
	A1.draw(win)
	A2 = gr.Text(gr.Point(1000,100),"Created By Robert Durst")
	A2.setFace('arial')
	A2.setStyle("bold")
	A2.setSize(20)
	A2.setTextColor("White")
	A2.draw(win)
	A3 =gr.Rectangle(gr.Point(850,800),gr.Point(1150,500))
	A3.setFill('goldenrod4')
	A3.draw(win)
	
	pinball = [P,I,N,B,A,L,L1]
	win.getMouse()
	launch(ball,74,4,5+random.random(),5,1)
	dt = 0.01
	frame = 0
	while True:
		for letter in pinball:
			color = (gr.color_rgb(255*random.random(),255*random.random(),255*random.random()))
			letter.setTextColor(color)
		collided = False
		for item in obstacles:
			if coll.collision(ball,item,dt):
				collided = True
		if collided == False:
			ball.update(dt)
		
		if frame % 10 == 0:
			win.update()
		
	
			
		
		
		frame += 1
		
		
		if ball.getPosition()[1] < 0:
			
			launch(ball,74,3,5+random.random(),5,1)
		
			win.getMouse()


   
	win.getMouse()
	win.close()

if __name__ == "__main__":
	main()
	
		