#!/usr/bin/env python3
import turtle
import sys
import random
import math
from matplotlib import pyplot

def createPoint(x,y):
	p=turtle.Turtle()
	p.shape('circle')
	p.color('green')
	p.speed(0)
	p.penup()
	#p.goto(100,100)
	#p.goto(point[0],point[1])
	

	p.x=x
	p.y=y
	p.goto(x,y) 
	p.vx=random.uniform(-4,4)
	p.vy=random.uniform(-4,4)
	return p

def pointCheck(x,y, personlist, diameter):
	safe=True
	for p in personlist:
		d=math.sqrt((x-p.x)**2+(y-p.y)**2)
		if d-5 < diameter:
			safe=False
			break
	return safe

steps=10000
stepsize=1
npoints=100

circlediam=20.0
circleradius=circlediam/2
win=turtle.getscreen()
win.tracer(0)
width=400
height=400
t=turtle.Turtle()
t.hideturtle()


t.penup()
t.goto((-width-circlediam)//2,(-height-circlediam)//2)
t.pendown()
t.goto((width+circlediam)//2,(-height-circlediam)//2)
t.goto((width+circlediam)//2,(height+circlediam)//2)
t.goto((-width-circlediam)//2,(height+circlediam)//2)
t.goto((-width-circlediam)//2,(-height-circlediam)//2)
t.penup()

pointlst=[]

while len(pointlst) < npoints :
	print (len(pointlst))
	x=random.randint( (-width//2)+circleradius, (width//2)-circleradius)
	y=random.randint( (-height//2)+circleradius, (height//2)-circleradius)
	if pointCheck(x,y,pointlst,circlediam) is True:
		p=createPoint(x,y)
		pointlst.append(p)


for step in range(steps):
	for point in pointlst:
		dx=point.vx*stepsize
		dy=point.vy*stepsize
		
		point.x=point.x+dx
		point.y=point.y+dy
		if point.x > width/2:
			point.vx=point.vx*-1
			point.x=width/2
		elif point.x < -width/2:
			point.vx=point.vx*-1
			point.x=-width/2
			
		if point.y > height/2 :
			point.vy=point.vy*-1
			point.y=height/2
			
		elif point.y < -1*width/2:
			point.vy=point.vy*-1
			point.y=-height/2

		point.goto(point.x,point.y)

		#print (point.x, point.y, point.position())
	#if step%10 == 0:
		#print(step)
	#win.update()
		
	for a in range(len(pointlst)):
		for b in range (a+1, len(pointlst)):
			p1x,p1y=(pointlst[a].x,pointlst[a].y)
			p2x,p2y=(pointlst[b].x,pointlst[b].y)
			dx=p2x-p1x
			dy=p2y-p1y
			d=math.sqrt(dx**2+dy**2)
			if d <= circlediam:
				#make people bounce off of each other
				newavx=pointlst[b].vx
				newavy=pointlst[b].vy
				newbvx=pointlst[a].vx
				newbvy=pointlst[a].vy

				pointlst[a].vx=newavx
				pointlst[a].vy=newavy
				pointlst[b].vx=newbvx		
				pointlst[b].vy=newbvy
				
				
				#move back to point of contact
				scale=math.sqrt(circlediam/(dx**2+dy**2))
				newdx=dx*scale
				newdy=dy*scale
				pointlst[a].x=pointlst[a].x-newdx/2
				pointlst[a].y-pointlst[a].y-newdy/2

				pointlst[b].x=pointlst[b].x+newdx/2
				pointlst[b].y=pointlst[b].y+newdy/2

				pointlst[a].goto(pointlst[a].x,pointlst[a].y)
				pointlst[b].goto(pointlst[b].x,pointlst[b].y)
				
	win.update()
				
	
	

win.mainloop()
print "Done!"

