#!/usr/bin/env python3
import turtle
import sys
import random
import math
import numpy as np
from matplotlib import pyplot as plt

def createPerson(height,width,circleradius):
	#create a person and move them to a point
	p=turtle.Turtle()
	p.shape('circle')
	p.color('green')
	p.speed(0)
	p.penup()
	p.goto(random.randint( (-width//2)+circleradius, (width//2)-circleradius), random.randint( (-height//2)+circleradius, (height//2)-circleradius) )

	#define velocity in x and y
	#vx=random.uniform(-15,15)
	#vy=random.uniform(-15,15)
	vx=random.choice([-10,10])
	vy=random.choice([-10,10])


	#this block of code sets up a dictionary of characteristics for a person
	person={}
	person['point']=p
	person['vx']=vx
	person['vy']=vy
	person['infected']=False
	person['immune']=False
	person['tinfected']=0
	person['alive']=True
	#print (p.get_shapepoly())
	#the function above on my computer shows that a circle has a diameter of 20
	return(person)
	
steps=10000
stepsize=1

#variables that influence the outbreak
npeople=350
circlediam=20.0
circleradius=circlediam/2
infectionduration=14
transmission_chance=0.5	
hospital_beds=30
mortality_rate=0.06

#create a window 
win=turtle.getscreen()
win.tracer(0)
### Uncomment below to have window be proportional to screen
#width=win.window_width()
#height=win.window_height()
#print (width, height)
width=800
height=800
t=turtle.Turtle()
t.hideturtle()

t.penup()
t.goto((-width-circlediam)//2,(-height-circlediam)//2)
t.pendown()
t.goto((width+circlediam)//2,(-height-circlediam)//2)
t.goto((width+circlediam)//2,(height+circlediam)//2)
t.goto((-width-circlediam)//2,(height+circlediam)//2)
t.goto((-width-circlediam)//2,(-height-circlediam)//2)

# t.penup()
# t.goto((-width)//2,(-height)//2)
# t.pendown()
# t.goto((width)//2,(-height)//2)
# t.goto((width)//2,(height)//2)
# t.goto((-width)//2,(height)//2)
# t.goto((-width)//2,(-height)//2)
t.penup()

#set up the population in personlist
personlist=[]
for person in range(npeople):
	personlist.append(createPerson(height,width,circleradius))

#make one person infected
personlist[-1]['infected']=True
personlist[-1]['point'].color('red')
currentinfected=1

#do a loop where the circle moves according to the velocity
infectedlist=[]
dailyinfections=[]
totalinfections=[currentinfected]
for n in range(steps):
	infectedlist.append(currentinfected)
	if currentinfected == 0:
		break
	
	#take a step
	currentinfected=0 #use this variable as an infection counter that we update every iteration
	for person in personlist:
		if person['alive']:
			x,y=person['point'].position()
			dx=person['vx']*stepsize
			dy=person['vy']*stepsize
			newx=x+dx
			newy=y+dy
			#person['point'].setx(newx)
			#person['point'].sety(newy)
		

			#make circle bounce if it "hits" a wall. One conditional for each wall. I think there's a more efficient way to do this with just one conditional.
			if newx-circleradius > width/2: #positive x wall
				newx=width-newx
				person['vx']=person['vx']*-1
			elif  newx+circleradius < -width/2:
				newx=-width-newx
				person['vx']=person['vx']*-1
			elif newy-circleradius > height/2:
				newy=height-newy
				person['vy']=person['vy']*-1
			elif newy+circleradius < -width/2:
				newy=-height-newy
				person['vy']=person['vy']*-1

			person['point'].goto(newx,newy)
			
			#make person get better over infectionduration
			if person['infected']:
				currentinfected+=1
				#print ("here")
				person['tinfected']+=1
				if person['tinfected'] > infectionduration:
					person['immune']=True
					person['infected']=False
					if random.uniform(0,1)< mortality_rate:
						person['alive']=False
						person['vx']=0
						person['vy']=0
						person['point'].color('black')
					else:
						person['point'].color('orange')

		
	#check for interaction
	#this is the slow step because for every step in the simulation, you have to check the distance between every pair of people (N^2/2).
	#can you think of a way to speed this up?
	newinfections=0
	for a in range(len(personlist)):
		for b in range (a+1, len(personlist)):
			p1x,p1y=personlist[a]['point'].position()
			p2x,p2y=personlist[b]['point'].position()
			d=math.sqrt((p2x-p1x)**2+(p2y-p1y)**2)
			if d < circlediam:
				#make people bounce off of each other
				newax=personlist[b]['vx']
				newbx=personlist[a]['vx']
				neway=personlist[b]['vy']
				newby=personlist[a]['vy']
				personlist[a]['vx']=newax
				personlist[b]['vx']=newbx
				personlist[a]['vy']=neway
				personlist[b]['vy']=newby

				if personlist[a]['infected'] and personlist[b]['infected']:
					continue
				elif (personlist[a]['infected'] or personlist[b]['infected']) and random.uniform(0,1) < transmission_chance :
					#skip infection if either is immune
					if personlist[a]['immune'] or personlist[b]['immune']:
						continue
					personlist[a]['point'].color('red')
					personlist[b]['point'].color('red')
					personlist[a]['infected']=True
					personlist[b]['infected']=True
					newinfections+=1
				
			
	dailyinfections.append(newinfections)
	tot=totalinfections[-1]+newinfections
	totalinfections.append(tot)
	#print(tot)
	win.update()
win.mainloop()

#calculate statistics
totalinfected=0
totaldead=0
for person in personlist:
	if person['immune'] or not person['alive']:
		totalinfected+=1
	if not person['alive']:
		totaldead+=1
print ("Total infected = %d/%d or %.2f%%" % (totalinfected, npeople, totalinfected/npeople*100))
print ("Total dead = %d/%d or %.2f%%" % (totaldead, npeople, totaldead/npeople*100))
print ("Total days of pandemic %d" % (n))



y1 = np.array(dailyinfections)
n = len(dailyinfections)
x = range(0,n,1)
del totalinfections[n]
y2 = np.array(totalinfections)



fig, ax1 = plt.subplots()
color = 'tab:red'
ax1.set_xlabel('Length of Pandemic (days)')
ax1.set_ylabel('Daily Infections', color=color)
ax1.plot(x, y1, color=color)
ax1.set_ylim([0,300])
ax1.tick_params(axis='y')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color= 'tab:blue'
ax2.set_ylabel('Total Infections', color=color)  # we already handled the x-label with ax1
ax2.plot(x, y2, color=color)
ax2.set_ylim([0,300])
ax2.tick_params(axis='y')

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
