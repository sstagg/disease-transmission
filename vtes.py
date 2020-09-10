#!/usr/bin/env python3
import turtle
import sys
import random
import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import transforms

def createPerson(height,width,circleradius,point,maxvelocity):
	#create a person and move them to a point
	p=turtle.Turtle()
	p.shape('circle')
	p.color('green')
	p.speed(0)
	p.penup()

	#this block of code sets up a dictionary of characteristics for a person
	person={}
	person['x']=point[0]
	person['y']=point[1]
	p.goto(person['x'],person['y'])

	#define velocity in x and y
	vx=random.uniform(-maxvelocity,maxvelocity)
	vy=random.uniform(-maxvelocity,maxvelocity)
	#r=list(range(-10,-6))+list(range(6,10))
	#vx=random.choice(r)
	#vy=random.choice(r)

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

def pointCheck(point, personlist, diameter):
	#check to see if a point overlaps within one diameter of another point
	p1x,p1y=point
	safe=True
	for personb in personlist:
		p2x,p2y=personb['point'].position()
		d=math.sqrt((p2x-p1x)**2+(p2y-p1y)**2)
		if d < diameter:
			safe=False
			break
	return safe
	
steps=10000
stepsize=1

#variables that influence the outbreak
npeople=375
circlediam=20.0
infectionduration=14
transmission_chance=0.9 #0.9 and 0.7 are good values to show how small changes to transmission makes dramatic effects on spread
hospital_beds=30
mortality_rate=0.06
width=700
height=700
maxvelocity=6

record_contacts=False #set to 'True' to calculate the contact rate fo noninfected individuals with the first infected person.
circleradius=circlediam/2

#create a window 
win=turtle.getscreen()
win.tracer(0)
### Uncomment below to have window be proportional to screen
#width=win.window_width()
#height=win.window_height()
t=turtle.Turtle()
t.hideturtle()

#draw bounding box
t.penup()
t.goto((-width-circlediam)//2,(-height-circlediam)//2)
t.pendown()
t.goto((width+circlediam)//2,(-height-circlediam)//2)
t.goto((width+circlediam)//2,(height+circlediam)//2)
t.goto((-width-circlediam)//2,(height+circlediam)//2)
t.goto((-width-circlediam)//2,(-height-circlediam)//2)
t.penup()

#set up the population in personlist
personlist=[]
print ("Populating simulation")
initpoint=(random.randint( (-width//2)+circlediam, (width//2)-circlediam), random.randint( (-height//2)+circlediam, (height//2)-circlediam))
personlist.append(createPerson(height,width,circleradius,initpoint,maxvelocity))
while len(personlist) < npeople:
	#keep adding points until npeople is reached. Reject points if overlap another.
	print (len(personlist), end=' ')
	testpoint=(random.randint( (-width//2)+circleradius, (width//2)-circleradius), random.randint( (-height//2)+circleradius, (height//2)-circleradius))
	if pointCheck(testpoint, personlist, circlediam) is True:
		personlist.append(createPerson(height,width,circleradius,testpoint,maxvelocity))
	else:
		print ("\nPoint rejected")
print("\nPopulating complete")

#make one person infected
personlist[-1]['infected']=True
personlist[-1]['point'].color('red')
personlist[-1]['contacts']=0
currentinfected=1

#do a loop where the circle moves according to the velocity
infectedlist=[]
dailyinfections=[]
totalinfections=[currentinfected]

# if record_contacts is True, only iterate for infectionduration times
if record_contacts:
	steps=infectionduration
	transmission_chance=1
	
for n in range(steps):
	infectedlist.append(currentinfected)
	if currentinfected == 0:
		break
	
	#take a step
	currentinfected=0 #use this variable as an infection counter that we update every iteration
	for person in personlist:
		if person['alive']:
			dx=person['vx']*stepsize
			dy=person['vy']*stepsize
			
			newx=person['x']+dx
			newy=person['y']+dy
		
			#make circle bounce if it "hits" a wall. 
			if newx > width/2: #positive x wall
				newx=width/2
				person['vx']=person['vx']*-1
			elif newx < -width/2:
				newx=-width/2
				person['vx']=person['vx']*-1

			if newy > height/2:
				newy=height/2
				person['vy']=person['vy']*-1
			elif newy < -height/2:
				newy=-height/2
				person['vy']=person['vy']*-1

			person['x']=newx
			person['y']=newy
			person['point'].goto(newx,newy)
			
			#make person get better over infectionduration
			if person['infected']:
				currentinfected+=1
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
			p1x=personlist[a]['x']
			p1y=personlist[a]['y']
			p2x=personlist[b]['x']
			p2y=personlist[b]['y']
			
			dx=p2x-p1x
			dy=p2y-p1y
			d=math.sqrt(dx**2+dy**2)
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

				#move back to point of contact
				scale=math.sqrt(circlediam/(dx**2+dy**2))
				newdx=dx*scale
				newdy=dy*scale

				personlist[a]['x']=personlist[a]['x']-newdx/2
				personlist[a]['y']=personlist[a]['y']-newdy/2

				personlist[b]['x']=personlist[b]['x']+newdx/2
				personlist[b]['y']=personlist[b]['y']+newdy/2

				personlist[a]['point'].goto(personlist[a]['x'],personlist[a]['y'])
				personlist[b]['point'].goto(personlist[b]['x'],personlist[b]['y'])
				
				if personlist[a]['infected'] and personlist[b]['infected']:
					continue
				elif (personlist[a]['infected'] or personlist[b]['infected']) and random.uniform(0,1) < transmission_chance :
					if record_contacts and (a == npeople-1 or b == npeople-1 ):
						personlist[npeople-1]['contacts']+=1
					#skip infection if either is immune
					if personlist[a]['immune'] or personlist[b]['immune']:
						continue
					personlist[a]['point'].color('red')
					personlist[b]['point'].color('red')
					personlist[a]['infected']=True
					personlist[b]['infected']=True
					newinfections+=1
	win.update()
				
			
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
print ("Total days of pandemic %d" % (n+1))
if record_contacts:
	c=personlist[npeople-1]['contacts']/infectionduration
	print ("Contact rate for uninfected individuals with patient zero = %f" % ( c ))
	sys.exit()


y1 = np.array(dailyinfections)
n = len(dailyinfections)
x = range(0,n,1)
del totalinfections[n]
y2 = np.array(totalinfections)


fig, ax1 = plt.subplots()
color= 'blue'
ax1.set_ylabel('Total Infections', color=color)  # we already handled the x-label with ax1
ax1.plot(x, y2, label="Cumulative Infections", color=color, linewidth=3)
ax1.plot(x, infectedlist[1:], label="Current Infected", color='tab:blue', linewidth=3)
ax1.set_ylim([0,y2[-1]*1.25])
ax1.tick_params(axis='y')

ax1.plot([0, n], [30, 30], 'k-', label="Available Hospital Beds")

ax1.legend(loc="upper left", frameon=False)


ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color1 = 'red'
ax2.set_xlabel('Length of Pandemic (days)')
ax2.set_ylabel('Daily Infections', color=color1)
ax2.plot(x, y1, label="New Infections", color=color1, alpha=0.2, linestyle='dashed')
# ax1.set_ylim([0,npeople])
ax2.set_ylim(0,15)
ax2.tick_params(axis='y')

ax2.legend(loc="upper right", frameon=False)

plt.show()
