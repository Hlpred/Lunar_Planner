import math
import matplotlib.pyplot as plt
import numpy as np

step = 0.0005
radius = 1.7374e6
G = 6.67e-11
M = 7.347e22
startingEle = -2565
landingEle = -3125.3
totalVel = 1447.67661
launchAngle = 26.91521 * (math.pi/180)

bodyCenter = [0, 0]
spacecraftPos = [0, radius+startingEle]
spacecraftVel = [math.cos(launchAngle)*totalVel, math.sin(launchAngle)*totalVel]
spacecraftVel = [component*step for component in spacecraftVel]

def getGrav(r):
    return (step**2)*(G*M/((r)**2))

xRes = []
yRes = []
tempPos = [0, 0]
halfTempPos = [0, 0]
crash = False
crashCheck = False
rPrev = 0
Hit = [0, 0]
for i in range(round((1/step)*3000)):
    origX = spacecraftPos[0]
    origY = spacecraftPos[1]
    tempPos[0] = spacecraftPos[0] + spacecraftVel[0]
    tempPos[1] = spacecraftPos[1] + spacecraftVel[1]
    r = math.sqrt(spacecraftPos[0]**2 + spacecraftPos[1]**2)
    if spacecraftPos[1] != 0:
        theta = math.atan2(spacecraftPos[1], spacecraftPos[0])
    else:
        theta = math.pi/2
    tempPos[0] -= math.cos(theta)*getGrav(r)
    tempPos[1] -= math.sin(theta)*getGrav(r)
    spacecraftPos = tempPos
    spacecraftVel[0] = spacecraftPos[0] - origX
    spacecraftVel[1] = spacecraftPos[1] - origY
    if i % 15 == 0:
        xRes.append(spacecraftPos[0])
        yRes.append(spacecraftPos[1])
    if (r > radius+landingEle) and crashCheck == False:
        crashCheck = True
    if r < (radius+landingEle) and crash == False and crashCheck == True:
        crash = True
        initAngle = math.atan2(spacecraftPos[0], spacecraftPos[1])
        radAngle = 0
        if spacecraftPos[0] > 0:
            radAngle = initAngle
        else:
            radAngle = initAngle + 2*math.pi
        Hit[0] = spacecraftPos[0]
        Hit[1] = spacecraftPos[1]
        print((radAngle/(2*math.pi))*(radius*2*math.pi)/1000)
        break
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(xRes, yRes)
ax.plot(0, radius+startingEle, marker='*')
ax.plot(Hit[0], Hit[1], marker='*')
ax.set_aspect('equal', adjustable='box')
angle = np.linspace( 0 , 2 * np.pi , 2000 ) 
x = radius * np.cos( angle ) 
y = radius * np.sin( angle ) 
ax.plot( x, y ) 
plt.show()
