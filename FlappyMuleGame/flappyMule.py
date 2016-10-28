#Robert Durst
#CS151 Fall
#Create the game Flappy Mule
#	run this as flappyMule.py

import graphics as gr
import physics_objects as PO
import random
import collision as coll
import os
import time

#Creates a game class that has settings and other relevant information
class Game():
	def __init__(self):
		self.volumeOn = True
		self.image = 1
		self.cheat = False
	
		#Get the scores from the save
		fp = open('Scores.txt')
		Text = fp.readlines()
		fp.close()

		score_part1 = [] #Get all the scores and names separately
		score_part2 = [] #Combine all names and scores and make a list like the one in the game

		beg = 0
		end = 0
		for text in Text:
			for character in text:	
				if character == ',':
					if beg != 0:
						beg += 1
					score_part1.append(text[beg:end])
					beg = end
				end += 1

		for i in range(20):
			i += 1
			if i%2:
				score_part2.append([int(score_part1[i-1]),score_part1[i-2]])


		self.scores = score_part2[:]
		self.Hiscore = self.scores[0][0]
	
		
	def Cheat(self):
		return self.cheat
		
	def setCheat(self,c):
		self.cheat = c
			
	def getHiScore(self):
		return self.Hiscore
		
	def setHiScore(self, s):
		self.Hiscore = s 
	
	def getImage(self):
		return self.image
		
	def setImage(self,i):
		self.image = i
	
	def getScores(self):
		return self.scores
	
	def getVolume(self):
		if self.volumeOn:
			return 'Volume: On'
		else:
			return 'Volume: Off'
	def Volume(self):
		return self.volumeOn
	
	def setVolume(self, v):
		if v == 1:
			self.volumeOn = True
			
		else:
			self.volumeOn = False
	
	def updateScore(self,score,name):
		if score > self.scores[-1][0]:
			self.scores[-1] = [score,name,1] #So I can identify the rank of the newest score added to the list
			self.scores.sort()
			self.scores = self.scores[::-1]
		
		for x in range(10):
			if len(self.scores[x]) == 3:
				self.scores[x] = [score,name]
				z = x + 1
				
				
		
		x = name
		y = score
		say = 'say Congrats '+str(x)+ ' your score of ' +str(y)+ ' is number '+str(z)+ ' on the high score list.'
		if self.Volume():
			os.system(say)
	
	def checkToAddScore(self,score):
		return score > self.scores[-1][0]
		
	def resetScores(self):
		self.scores =[[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA'],[0,'AAA']]
		self.Hiscore = 0
		self.image = 1
		
#Create the background image and the window
def createGameBackground():
	win = gr.GraphWin("Flappy Mule",400,600)
	win.setBackground('steelblue1')
	
	#Here I will draw Miller Library, the backdrop for my game
	base = gr.Rectangle(gr.Point(10,600),gr.Point(390,500))
	left_rect = gr.Rectangle(gr.Point(10,600),gr.Point(90,500))
	right_rect = gr.Rectangle(gr.Point(310,600),gr.Point(390,500))
	right_tri = gr.Polygon(gr.Point(300,500),gr.Point(400,500),gr.Point(350,450))
	left_tri = gr.Polygon(gr.Point(0,500),gr.Point(100,500),gr.Point(50,450))
	mid_rect = gr.Rectangle(gr.Point(110,600),gr.Point(290,425))
	mid_tri = gr.Polygon(gr.Point(120,500),gr.Point(280,500),gr.Point(200,450))
	pillar1 = gr.Rectangle(gr.Point(120,580),gr.Point(130,500))
	pillar2 = gr.Rectangle(gr.Point(150,580),gr.Point(160,500))
	pillar3 = gr.Rectangle(gr.Point(180,580),gr.Point(190,500))
	pillar4 = gr.Rectangle(gr.Point(210,580),gr.Point(220,500))
	pillar5 = gr.Rectangle(gr.Point(240,580),gr.Point(250,500))
	pillar6 = gr.Rectangle(gr.Point(270,580),gr.Point(280,500))
	stair_rect = gr.Rectangle(gr.Point(110,600),gr.Point(290,580))
	mid_rect2 = gr.Rectangle(gr.Point(170,425),gr.Point(230,375))
	mid_rect3 = gr.Rectangle(gr.Point(180,375),gr.Point(220,325))
	mid_rect4 = gr.Rectangle(gr.Point(185,325),gr.Point(215,275))
	mid_rect5 = gr.Rectangle(gr.Point(190,275),gr.Point(210,240))
	clock = gr.Circle(gr.Point(200,350),10)
	pointer = gr.Polygon(gr.Point(190,240),gr.Point(210,240),gr.Point(200,175))
	dot_top = gr.Circle(gr.Point(200,172),5)
	vert_line = gr.Line(gr.Point(200,167.5),gr.Point(200,157.5))
	hor_line = gr.Line(gr.Point(195,162.5),gr.Point(205,162.5))
	topper = gr.Polygon(gr.Point(205,157.5),gr.Point(195,157.5),gr.Point(197,152.5),gr.Point(200,152.5),gr.Point(200,155),gr.Point(205,155))
	
	sun = gr.Circle(gr.Point(50,50),50)
	sun.setFill('yellow')
	sun.setOutline('yellow')
	
	grass= gr.Rectangle(gr.Point(0,600),gr.Point(400,595))
	grass.setFill('green')
	grass.setOutline('green')
	
	objects = [base,right_rect,left_rect,right_tri,left_tri,mid_rect,mid_tri,pillar1,
	pillar2,pillar3,pillar4,pillar5,pillar6,stair_rect,mid_rect2,mid_rect3,mid_rect4,mid_rect5,clock,pointer,dot_top,
	vert_line,hor_line,topper,sun,grass]
	
	for item in objects:
		item.draw(win)
	
	
	return win


#Method for creating the pipe obstacles
def createObstacle(win):
	y1 = random.randint(5,45)
	y2 = 60-y1
	pipe_top = PO.Block(win,41,y1/2.0,5,y1)
	pipe_bot = PO.Block(win,41,y1+12+y2/2.0,5,y2)
	
	Pipes = [pipe_top,pipe_bot]
	
	for pipe in Pipes:
		pipe.Color('gray55')
		pipe.setVelocity([-15,0])
		pipe.draw()
	
	return Pipes

#Get image method that returns the correct image
def getImage(image):
	Images = [ 'bates.ppm', 'bowdoin.ppm', 'camel.ppm', 'bantam.ppm', 'hamilton.ppm', 'cardinal.ppm',
	 'middlebury.ppm', 'tufts.ppm', 'williams.ppm'	, 'Amherst.ppm', 'mule.ppm' , 'greene.ppm']
	
	return Images[image-1]

#Initializes the placement of the mask (the image that covers the ball)
def maskSprite(win,x,y,image):
		
		mask = gr.Image(gr.Point(x*10,win.getHeight()-y*10),getImage(image))
		mask.draw(win)
		
		return mask

#How I move the mask image
def maskMove(mask,dx,dy):
	mask.move(dx,dy)
	
#Set the original attributes of the sprite and create the sprite
def initializeSprite(win):
	
	sprite = PO.Ball(win,20,30,2)
	
	sprite.Color('black')
	
	sprite.setVelocity([0,0])
	sprite.setAcceleration([0,-15])
	
	#sprite.draw()

	return sprite

def getHole(sprite,pipe_top,pipe_bot):
	s_D = sprite.getPosition()
	pt_D = pipe_top.getPosition()
	pb_D = pipe_bot.getPosition()
	
	xdistance = pt_D[0]-s_D[0]
	
	bot_top_pipe = pt_D[1] + pipe_top.getHeight()/2
	top_bot_pipe = pb_D[1] - pipe_bot.getHeight()/2
	
	mid_hole = (top_bot_pipe + bot_top_pipe) / 2.0
	
	return mid_hole
	
#The actual game phase. This returns a score.
def mainPhase(game):
	
	image = game.getImage()
	
	win = createGameBackground()
	sprite = initializeSprite(win)
	Pipes = createObstacle(win) #index 0 is are the pipes (top and bottom) and index 1 is the checker
	pos = sprite.getPosition()
	mask = maskSprite(win,pos[0],pos[1],image)
	
	if game.Cheat():
		for pipe in Pipes:
			pipe.setVelocity([-12,0])
					
	#Initialize and create the score text
	score = 0
	score_text = gr.Text(gr.Point(200,25),score)
	score_text.setTextColor('white')
	score_text.setSize(36)
	score_text.setStyle('bold')
	score_text.draw(win)
	
	win.getKey()
	
	game_finished = False
	while game_finished == False:
		key = win.checkKey()
		pos1 = sprite.getPosition()
		
		
		if game.Cheat():
			Hole = getHole(sprite,Pipes[0],Pipes[1])
			if	Hole - pos1[1] > 2:
				if game.Volume():
					os.system('afplay woosh.wav&')
				sprite.setVelocity([0,12])
		
		#Make the sprite go up
		if key == 'space':
			if game.Volume():
				os.system('afplay woosh.wav&')
			sprite.setVelocity([0,12])
		
		
		#Make it so that the sprite can't drop down too fast
		if sprite.getVelocity() <= -20:
			sprite.setAcceleration([0,0])
		
		if sprite.getPosition()[1] < 0:
			game_finished = True
			if game.Volume():
				os.system('afplay Loss.wav&')
		
		
		ds = sprite.update(0.1)
		maskMove(mask,ds[0],ds[1])
		
		new_pipe = False
		for pipe in Pipes:
			if coll.collision(sprite,pipe,0.05):
				game_finished = True
				if game.Volume():
					os.system('afplay Loss.wav&')
			
		if Pipes[0].getPosition()[0] < 0:
			for pipe in Pipes:
				pipe.undraw()
			new_pipe = True
		else:
			for pipe in Pipes:
				pipe.update(0.05)
		
		if new_pipe:
			Pipes = createObstacle(win)
			if game.Cheat():
				for pipe in Pipes:
					pipe.setVelocity([-12,0])
			new_pipe = False
		
		
		if abs(sprite.getPosition()[0] - Pipes[0].getPosition()[0]-2.5) < 0.25:
			if game.Volume():
				os.system('afplay ding.wav&')
			score += 1
			score_text.setText(score)
		

		
	key = win.checkKey()
	gameOver = gr.Text(gr.Point(200,300),'Game Over')
	gameOver.setSize(36)
	gameOver.setStyle('bold')
	gameOver.draw(win)
	while key != 'q':
		key = win.checkKey()
		new_pipe = False
		for pipe in Pipes:
	
			if pipe.getPosition()[0] < 0:
				pipe.undraw()
				new_pipe = True
			else:
				pipe.update(0.05)
		
		if new_pipe:
			Pipes = createObstacle(win)
			new_pipe = False
		
		if sprite.getPosition() > -10:
			ds = sprite.update(0.1)
			maskMove(mask,ds[0],ds[1])
	if game.Volume():
		os.system('afplay click.wav&')
		
	win.close()
	if game.Volume():
		os.system('killall afplay')
		
	return score

def addScore(score,game):
		win = gr.GraphWin('Add High Score',500,500)
		win.setBackground('steelblue1')
		
		Title = gr.Text(gr.Point(250,50),'ENTER YOUR INITIALS')
		Title.setStyle('bold')
		Title.setSize(36)
		Title.setTextColor('Black')
		Title.draw(win)
		
		labels = []
		count = 0
		for x in range(3):
			label = gr.Rectangle(gr.Point(125+count*100,200),gr.Point(175+count*100,300))
			label.setFill('grey')
			label.setOutline('grey')
			label.draw(win)
			labels.append(label)
			
			count += 1
		
		letter_label = []
		count = 0
		for x in range(3):
			label = gr.Text(gr.Point(150+count*100,250),'A')
			label.setSize(36)
			label.setStyle('bold')
			label.draw(win)
			letter_label.append(label)
			
			count += 1
				
		#Where the user inputs his or her name if a hiscore is made
		unFinished = True
		labels[0].setOutline('black')
		space_count = 0
		letter_count = 0
		letters =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		
		name = ''
		
		while unFinished:
			key = win.checkKey()
			if key == 'space':
				if space_count != 2:
					if game.Volume():
						os.system('afplay click.wav&')
					name += letters[letter_count]
					
					labels[space_count].setOutline('grey')
					space_count += 1
					labels[space_count].setOutline('black')
					
					letter_count = 0
				elif space_count == 2:
					name += letters[letter_count]
					if game.Volume():
						os.system('afplay click.wav&')
					unFinished = False
					
			if key == 'Up' and letter_count != 25:
				if game.Volume():
					os.system('afplay click.wav&')
				letter_count += 1
				letter_label[space_count].setText(letters[letter_count])
			
			if key == 'Down' and letter_count != 0:
				if game.Volume():
					os.system('afplay click.wav&')
				letter_count -= 1
				letter_label[space_count].setText(letters[letter_count])
			
		if name == 'RSD':
			game.setCheat(True)
		
		if name == 'MAD':
			game.setCheat(False)
		
		game.updateScore(score,name)
		game.setHiScore(game.getScores()[0][0]	)
		win.close()
		return [score,name] 

#The title phase where a menu is presented. This returns a number that corresponds to the choice the user made.
def titlePhase(game):
	if game.Volume():
		os.system('afplay theme.wav&')
	
	win = gr.GraphWin('',500,600,False)
	win.setBackground('steelblue1')
	
	#draw the unmovable labels first
	count = 0
	for x in range(5):
		label = gr.Rectangle(gr.Point(175,100+100*count),gr.Point(325,150+100*count))
		label.setFill('grey')
		label.setOutline('grey')
		label.draw(win)
		count += 1
	
	
	#These are the outlines that appear when the user uses the arrow keys on the menu
	Label_1 = gr.Rectangle(gr.Point(175,100),gr.Point(325,150))
	Label_2 = gr.Rectangle(gr.Point(175,200),gr.Point(325,250))
	Label_3 = gr.Rectangle(gr.Point(175,300),gr.Point(325,350))
	Label_4 = gr.Rectangle(gr.Point(175,400),gr.Point(325,450))
	Label_5 = gr.Rectangle(gr.Point(175,500),gr.Point(325,550))

	labels = [Label_1,Label_2,Label_3,Label_4,Label_5]

	for item in labels:
		item.setOutline('black')

	#These are the labels' labels
	Text_1 = gr.Text(gr.Point(250,125),"Play Game")
	Text_2 = gr.Text(gr.Point(250,225),"High Scores")
	Text_3 = gr.Text(gr.Point(250,325),"Sprites")
	Text_4 = gr.Text(gr.Point(250,425),"Settings")
	Text_5 = gr.Text(gr.Point(250,525),"Exit")
	

	texts = [Text_1,Text_2,Text_3,Text_4,Text_5]

	for item in texts:
		item.setStyle('bold')
		item.setSize(25)
		item.draw(win)

	#This is the title
	Title_Text1 = gr.Text(gr.Point(160,50),"F")
	Title_Text2 = gr.Text(gr.Point(180,50),"L")
	Title_Text3 = gr.Text(gr.Point(200,50),"A")
	Title_Text4 = gr.Text(gr.Point(220,50),"P")
	Title_Text5 = gr.Text(gr.Point(240,50),"P")
	Title_Text6 = gr.Text(gr.Point(260,50),"Y")
	Title_Text7 = gr.Text(gr.Point(300,50),"M")
	Title_Text8 = gr.Text(gr.Point(320,50),"U")
	Title_Text9 = gr.Text(gr.Point(340,50),"L")
	Title_Text10 = gr.Text(gr.Point(360,50),"E")

	Title_Text_Bob = gr.Text(gr.Point(60,50),"BOB'S")
	Title_Text_Bob.setStyle('bold')
	Title_Text_Bob.setSize(36)
	Title_Text_Bob.setTextColor('White')
	Title_Text_Bob.draw(win)

	Title_Text_Game = gr.Text(gr.Point(450,50),"Game")
	Title_Text_Game.setStyle('bold')
	Title_Text_Game.setSize(36)
	Title_Text_Game.setTextColor('White')
	Title_Text_Game.draw(win)
	
	Author = gr.Text(gr.Point(250,575),"By Robert Durst")
	Author.setStyle('bold')
	Author.setSize(20)
	Author.setTextColor('White')
	Author.draw(win)
	
	title = [Title_Text1,Title_Text2,Title_Text3,Title_Text4,Title_Text5,Title_Text6,Title_Text7,Title_Text8,Title_Text9,Title_Text10]

	for item in title:
		item.setStyle('bold')
		item.setSize(36)
		item.setTextColor('White')
		item.draw(win)
	
	labels[0].draw(win)
	update = 0
	change = 0
	unFinished = True #Finished is true when the space is hit
	counter = 0
	color_var = 0
	color = 'blue'
	while unFinished:
		key = win.checkKey()
		
		if key == 'space':
			if game.Volume():
				os.system('afplay click.wav&')
			break
		
		elif key == 'Down':
			if counter != 4:
				if game.Volume():
					os.system('afplay click.wav&')
				labels[counter].undraw()
				counter += 1
				labels[counter].draw(win)
		
		elif key == 'Up':
			if counter != 0:
				if game.Volume():
					os.system('afplay click.wav&')
				labels[counter].undraw()
				counter -= 1
				labels[counter].draw(win)
		#Makes the title change colors (style)
		if update%100 == 0:
			if change == 10:
				change = 0
				color_var += 1
				color = (gr.color_rgb(255*random.random(),255*random.random(),255*random.random()))
			if color_var%2 == 0:
				title[change].setTextColor(color)
				change += 1
			else:
				title[change].setTextColor('white')
				change += 1
	
		update += 1
	if game.Volume():
		os.system('killall afplay')
	win.close()
	return counter+1

def menuSprites(game):
	win = gr.GraphWin('Sprites',500,500)
	win.setBackground('orange')
	
	Title = gr.Text(gr.Point(250,50),'Sprite Selection')
	Title.setStyle('bold')
	Title.setSize(36)
	Title.setTextColor('black')
	Title.draw(win)
	
	HS_Text = gr.Text(gr.Point(200,475),'Current High Score:')
	HS_Text.setStyle('bold')
	HS_Text.setSize(30)
	HS_Text.setTextColor('black')
	HS_Text.draw(win)
	
	
	Current_HS = gr.Text(gr.Point(375,475),game.getHiScore())
	Current_HS.setStyle('bold')
	Current_HS.setSize(30)
	Current_HS.setTextColor('black')
	Current_HS.draw(win)
	
	
	count = 0 #For the rows
	counter = 0 #For the scores needed to achieve the sprite
	Images = []
	for x in range(4):
		image = gr.Image(gr.Point(100,100+100*count),'qBox.ppm')
		image.draw(win)
		text = gr.Text(gr.Point(100,140+100*count),5*counter)
		text.setSize(20)
		text.draw(win)
		counter += 1
		Images.append(image)
		image = gr.Image(gr.Point(250,100+100*count),'qBox.ppm')
		image.draw(win)
		text = gr.Text(gr.Point(250,140+100*count),5*counter)
		text.setSize(20)
		text.draw(win)
		counter += 1
		Images.append(image)
		image = gr.Image(gr.Point(400,100+100*count),'qBox.ppm')
		image.draw(win)
		text = gr.Text(gr.Point(400,140+100*count),5*counter)
		text.setSize(20)
		text.draw(win)
		counter += 1
		Images.append(image)
		count += 1
	
	count = 0
	counter = 0 #because must count out differently in x direction
	
	score = game.getHiScore()
	
	#determine the number of times to run the redraw loop
	if score <= 4:
		times = 1
	elif score < 51:
		times = score/5 +1
	else:
		times = 12 
	
	#Keep track of how many images are allowed to be selected
	selectable = times
	
	#Daw all the unlocked image sprites
	
	check_labels = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]] #used to check that the player cannot select an unknown sprite
	
	for x in range(times):
		Images[x].undraw()
		Images[x] = gr.Image(gr.Point(100+150*counter,100+100*count),getImage(x+1))
		Images[x].draw(win)
		check_labels[count][counter] = 1
		counter += 1
		
		if counter == 3:
			counter = 0
			count += 1
	
	#Create the label that will work as user input
	label_selectors = []
	count = 0
	for x in range(4):
		label1 = gr.Rectangle(gr.Point(75,75+100*count),gr.Point(125,125+100*count))
		label2 = gr.Rectangle(gr.Point(225,75+100*count),gr.Point(275,125+100*count))
		label3 = gr.Rectangle(gr.Point(375,75+100*count),gr.Point(425,125+100*count))

		label_selectors.append([label1,label2,label3])
		
		count += 1
	
	
	
	x = 0
	y = 0
	label_selectors[y][x].draw(win)
	unFinished = True
	while unFinished:
		key = win.checkKey()
		
		if key == 'space':
			if game.Volume():
				os.system('afplay click.wav&')
			if check_labels[y][x] == 1:
				unFinished = False
			else:
				unFinished = True
		
		if key == 'Up' and y != 0:
			if game.Volume():
				os.system('afplay click.wav&')
			label_selectors[y][x].undraw()
			y -= 1
			label_selectors[y][x].draw(win)
		
		if key == 'Down' and y != 3:
			if game.Volume():
				os.system('afplay click.wav&')
			label_selectors[y][x].undraw()
			y += 1
			label_selectors[y][x].draw(win)
		
		if key == 'Left' and x != 0:
			if game.Volume():
				os.system('afplay click.wav&')
			label_selectors[y][x].undraw()
			x -= 1
			label_selectors[y][x].draw(win)
		
		if key == 'Right' and x != 2:
			if game.Volume():
				os.system('afplay click.wav&')
			label_selectors[y][x].undraw()
			x += 1
			label_selectors[y][x].draw(win)
		
	label_to_use = [[1,2,3],[4,5,6],[7,8,9],[10,11,12]]		 
	game.setImage( label_to_use[y][x] )
	
	win.close()
	
def menuHiScores(game): #This is the screen where the high scores will be displayed
	win = gr.GraphWin('High Scores',500,500)
	win.setBackground('green4')
	
	In_Win = gr.Rectangle(gr.Point(100,100),gr.Point(400,400))
	In_Win.setFill('yellow')
	In_Win.setOutline('yellow')
	In_Win.draw(win)
	
	Title = gr.Text(gr.Point(250,50),'High Scores')
	Title.setStyle('bold')
	Title.setSize(36)
	Title.setTextColor('Gold')
	Title.draw(win)
	
	
	scores = game.getScores()
	
	count = 0
	for x in range(10):
		text1 = gr.Text(gr.Point(125,130+count*25),(str(x+1),'.'))
		text1.setSize(20)
		text1.draw(win)
		text2 = gr.Text(gr.Point(225,130+count*25),scores[x][0])
		text2.setSize(20)
		text2.draw(win)
		text3 = gr.Text(gr.Point(325,130+count*25),scores[x][1])
		text3.setSize(20)
		text3.draw(win)
	
		
		count += 1
	
	key = win.checkKey()
	while key != 'space':
		key = win.checkKey()
	
	win.close()
	
def menuSettings(game):
	win = gr.GraphWin('Settings',500,600)
	win.setBackground('pink')
	
	#These are the outlines that appear when the user uses the arrow keys on the menu
	Label_1 = gr.Rectangle(gr.Point(175,100),gr.Point(325,150))
	Label_2 = gr.Rectangle(gr.Point(175,200),gr.Point(325,250))
	Label_3 = gr.Rectangle(gr.Point(175,300),gr.Point(325,350))
	Label_4 = gr.Rectangle(gr.Point(175,400),gr.Point(325,450))
	Label_5 = gr.Rectangle(gr.Point(175,500),gr.Point(325,550))

	labels = [Label_1,Label_2,Label_3,Label_4,Label_5]
	
	for item in labels:
		item.setOutline('grey')
		item.setFill('grey')
		item.draw(win)

	#These are the labels' labels
	Text_1 = gr.Text(gr.Point(250,125),"Volume")
	Text_2 = gr.Text(gr.Point(250,225),"Reset Scores")
	Text_3 = gr.Text(gr.Point(250,325),"Help")
	Text_4 = gr.Text(gr.Point(250,425),"Credits")
	Text_5 = gr.Text(gr.Point(250,525),"Save Scores")
	

	texts = [Text_1,Text_2,Text_3,Text_4,Text_5]

	for item in texts:
		item.setStyle('bold')
		item.setSize(16)
		item.draw(win)
		
	unFinished = True
	count = 0 #Keep track of what label the user is on. Also import for when the user makes a selection so you know what they choose.	
	labels[count].setOutline('black')
	while unFinished:
		key = win.checkKey()
		
		if key == 'q':
			if game.Volume():
				os.system('afplay click.wav&')
			unFinished = False
		
		if key == 'Up' and count != 0:
			if game.Volume():
				os.system('afplay click.wav&')
			labels[count].setOutline('grey')
			count -=1 
			labels[count].setOutline('black')
		
		elif key == 'Down' and count != 4:
			if game.Volume():
				os.system('afplay click.wav&')
			labels[count].setOutline('grey')
			count +=1 
			labels[count].setOutline('black')
	
		elif key =='space':
			if game.Volume():
				os.system('afplay click.wav&')
			
			if count == 0:
				texts[0].setText(game.getVolume())
				if game.getVolume() == 'Volume On':
					counter = 2 #Keep track of the volume being off or on
				else:
					counter = 1
		
				key = win.checkKey()
		
				while key != 'space':
		
					key = win.checkKey()
					if key == 'Up' or key == 'Down':
						if game.Volume():
							os.system('afplay click.wav&')
						if counter%2 == 0:
							game.setVolume(0)
							texts[0].setText(game.getVolume())
							counter += 1
						else:
							game.setVolume(1)
							texts[0].setText(game.getVolume())
							counter += 1
				if game.Volume():
					os.system('afplay click.wav&')
				texts[0].setText('Volume')
			
			elif count == 1:
				texts[1].setText('Ok')
				game.resetScores()
				time.sleep(2)
				texts[1].setText('Reset High Scores')
			
			elif count == 2:
				win1 = gr.GraphWin("Help",1000,500) #Create a new window for the help screen
				
				Title = gr.Text(gr.Point(500,50),'HELP')
				Title.setStyle('bold')
				Title.setSize(36)
				Title.setTextColor('Black')
				Title.draw(win1)
	
		
				text1 = gr.Text(gr.Point(500,100),"After you begin the game, you will have to hit a key to start.")
				text2 = gr.Text(gr.Point(500,125),'Then hit space to make the sprite go up and avoid hitting the pipes or the ground.')
				text3 = gr.Text(gr.Point(500,150),'Once you hit a pipe or the ground you lose. Hit q to quit the game.')
				text4 = gr.Text(gr.Point(500,175),'If you get a new top ten high score you will prompted to enter your initials.')
				text5 = gr.Text(gr.Point(500,200),'Do so with the arrow keys and hit space to advance.')
				text6 = gr.Text(gr.Point(500,225),'You unlock sprites based on your high score. The sprites do not have any score advantages, they only add style.')
				text7 = gr.Text(gr.Point(500,250),'The better sprites require a better high score. You can select which sprite you want to use in the Sprites screen.')
				text8 = gr.Text(gr.Point(500,275),'It is possible to unlock all the sprites in the settings. I would tell you where to look but then you would not get credit for it.')
				text9 = gr.Text(gr.Point(500,300),'Space is used to exit most screens. You must use space to exit this screen and the credit screen or else you will have to restart the program!')
			
				texts = [text1,text2,text3,text4,text5,text6,text7,text8,text9]
				for text in texts:
					text.setSize(14)
					text.draw(win1)
			
				key = win1.checkKey()
				
				while key != 'space':
					key = win1.checkKey()
				if game.Volume():
					os.system('afplay click.wav&')
				win1.close()
				unFinished = False
			elif count == 3:
				win1 = gr.GraphWin("Help",1000,700) #Create a new window for the help screen
				
				
				Title = gr.Text(gr.Point(300,50),'Credits')
				Title.setStyle('bold')
				Title.setSize(36)
				Title.setTextColor('Black')
				Title.draw(win1)
				
				text1 = gr.Text(gr.Point(350,100),"Based on the original Flappy Bird Game by Dong Nguyen. I do not own the images or sounds. I got them from the internet.")
				text1.setSize(12)
				text1.draw(win1)
				
				text2 = gr.Text(gr.Point(300,650),"******* Hint: press the up arrow seven times. *******  ")
				text2.setSize(15)
				text2.draw(win1)
				
				image = gr.Image(gr.Point(850,400),'FlappyBird.ppm')
				image.draw(win1)
				
				image2 = gr.Image(gr.Point(350,400),'flappy2.ppm')
				image2.draw(win1)
				
				key = win1.checkKey()
				count = 0 #Variable for the cheat
				while key != 'space':
					key = win1.checkKey()
					
					if count == 7:
						if game.Volume():
							os.system('afplay clapping.wav&')
						text1.setText('')
						text2.setText('')
						Title.setText('')
						
						win_list = []
						for x in range(10):
							win = gr.GraphWin("???????????????????????????????????????????????????????????????????????????",1000,500) 
							win_list.append(win)
							
						text = gr.Text(gr.Point(500,250),"Congrats you unlocked all sprites and your new high score is 100! Hit space to return to main screen.")
						text.setStyle('bold')
						text.setSize(20)
						text.draw(win_list[-1])
						
						key1 = win_list[-1].checkKey()
						
						while key1 != 'space':
							key1 = win_list[-1].checkKey()
							color = (gr.color_rgb(255*random.random(),255*random.random(),255*random.random()))
							win_list[-1].setBackground(color)
						
						game.setHiScore(100)
						game.scores[0] = [100,'Robert Durst']	
						
						for win in win_list:
							win.close()
						
						if game.Volume():
							os.system('killall afplay')
						
						break
						
					if key == 'Up':
						count += 1
				if game.Volume():
						os.system('afplay click.wav&')		
				win1.close()
				unFinished = False	
				win.close()
	
			elif count == 4:
				texts[4].setText('Ok')
				fp = open('Scores.txt','w') 
				scores = game.getScores()
				for i in range(10):
					fp.write(str(scores[i][0])+','+str(scores[i][1]+','))
				fp.close()
				time.sleep(2)
				texts[4].setText('Save Scores')		
	
	win.close()

def main(): #Where the actual game is run. Runs until the user clicks the red X.
	game = Game()
	while True:
		status = titlePhase(game)
		
		if status == 1:
			score= mainPhase(game)
			if game.checkToAddScore(score):
				score = addScore(score,game)

		elif status == 2:
			menuHiScores(game)
		
		elif status == 3:
			menuSprites(game)
		
		elif status == 4:
			menuSettings(game)
		
		elif status == 5:
			os.system('killall afplay')
			break
			

def test(): #Used for test drawing the Miller Library
	game = Game()
	mainPhase(game)
if __name__ == "__main__":
	main()

	