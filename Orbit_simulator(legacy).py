import math
import matplotlib.pyplot as plt

bodyCenter = [0, 0]
spacecraftPos = [6500e3, 0]
spacecraftVel = [0, -8e3]

G = 6.67e-11
M = 5.97e24

def getGrav(r):
    return G*M/((r)**2)

xRes = []
yRes = []
tempPos = [0, 0]
for i in range(4):
    origX = spacecraftPos[0]
    origY = spacecraftPos[1]
    if spacecraftPos[0] >= 0:
        tempPos[0] = spacecraftPos[0] + spacecraftVel[0]
    else:
        tempPos[0] = spacecraftPos[0] + spacecraftVel[0]
    if spacecraftPos[1] >= 0:
        tempPos[1] = spacecraftPos[1] + spacecraftVel[1]
    else:
        tempPos[1] = spacecraftPos[1] + spacecraftVel[1]
    r = math.sqrt(spacecraftPos[0]**2 + spacecraftPos[1]**2)
    theta = math.atan2(spacecraftPos[1], spacecraftPos[0])
    if tempPos[0] <= 0:
        tempPos[0] += math.cos(theta)*getGrav(r)
    else:
        tempPos[0] -= math.cos(theta)*getGrav(r)
    if tempPos[1] <= 0:
        tempPos[1] += math.sin(theta )*getGrav(r)
    else:
        tempPos[1] -= math.sin(theta)*getGrav(r)
    spacecraftPos = tempPos
    if tempPos[0] <= 0:
        spacecraftVel[0] = spacecraftPos[0] - origX
    else:
        spacecraftVel[0] = origX - spacecraftPos[0]
    if tempPos[1] <= 0:
        spacecraftVel[1] = spacecraftPos[0] - origY
    else:
        spacecraftVel[1] = origY - spacecraftPos[1]
    xRes.append(spacecraftVel[0])
    yRes.append(spacecraftVel[1])
    print(spacecraftVel[1])
plt.scatter(xRes, yRes)
plt.show()
