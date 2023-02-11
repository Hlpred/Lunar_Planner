import math
import matplotlib.pyplot as plt
import numpy as np
import Constants
import Lunar_planner

step = 0.0005
radius = Constants.radius
G = Constants.G
M = Constants.M

def engineAccel(wetMass, burnRate, thrust, time, offset):
    return thrust / (wetMass - burnRate*(time+offset))

def ellipse_slope(point, x1, y1):
  return -(point[0]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[0]-x1)*math.sqrt(point[0]**2+point[1]**2)))/(point[1]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[1]-y1)*math.sqrt(point[0]**2+point[1]**2)))

def slope_to_angle(slope, point):
  return math.fabs(math.atan(slope)-math.atan(-point[0]/point[1]))

def grav_adjustment(r, foc_x, foc_y, pos, a, vel, a_s, path_angle):
    a_g = ((G*M)/r**2)
    a /= 2
    b = math.sqrt(a**2-(math.sqrt(foc_x**2+foc_y**2)/2)**2)
    x_axis_angle = math.pi-(math.atan(foc_y/foc_x)-math.atan((pos[1]/radius-(foc_y)/2)/(pos[0]/radius-(foc_x)/2)))
    t = math.atan(a*math.tan(x_axis_angle)/b)
    K = (a*b)/(math.sqrt((a*math.sin(t))**2+(b*math.cos(t))**2))**3
    v_mag = math.sqrt(vel[0]**2+vel[1]**2)/step
    alpha = -path_angle
    y = -(K*v_mag**2)/radius
    b_1 = 2*a_g*math.sin(-alpha)
    c_1 = (a_g*math.sin(-alpha))**2+(y+a_g*math.cos(alpha))**2-a_s**2
    angle_above_path = math.atan((y+a_g*math.cos(alpha))/(((-b_1+math.sqrt(b_1**2-4*(c_1)))/2)+a_g*math.sin(-alpha)))
    return (angle_above_path+path_angle)

def simulate(distance, startingEle, landingEle, fullFlight, timeOffset):
    manuver_data = Lunar_planner.ele_adjustment(distance, startingEle, landingEle)
    #launchAngle = launchAngle*(math.pi/180)
    #burnAngle = burnAngle*(math.pi/180)
    spacecraftPos = [0, radius + startingEle]
    #spacecraftVel = [math.cos(launchAngle)*totalVel, math.sin(launchAngle)*totalVel]
    #spacecraftVel = [component*step for component in spacecraftVel]
    spacecraftVel = [0, 0]

    xRes = []
    yRes = []
    crash = False
    crashCheck = False
    burnDone = False
    goingGown = False
    Hit = [0, 0]
    firstAngle = 0
    lastAngle = 0
    #1/step is the time of one step in seconds
    foc_x = manuver_data[4]
    foc_y = manuver_data[5]
    half_center_angle = distance/(2*radius/1000)
    focus_len = math.sqrt(manuver_data[4]**2 + manuver_data[5]**2)
    focus_theta = math.atan2(manuver_data[5], manuver_data[4])
    new_theta = focus_theta - half_center_angle
    foc_x = focus_len*math.cos(new_theta)
    foc_y = focus_len*math.sin(new_theta)
    prev_vel = 0
    dv = 0
    for i in range(round((1/step)*100000)):
        spacecraftPos[0] += spacecraftVel[0]
        spacecraftPos[1] += spacecraftVel[1]
        r = math.sqrt(spacecraftPos[0]**2 + spacecraftPos[1]**2)
        slope = ellipse_slope([spacecraftPos[0]/radius, spacecraftPos[1]/radius], foc_x, foc_y)
        burnAngle = slope_to_angle(slope, [spacecraftPos[0]/radius, spacecraftPos[1]/radius])
        orig_angle = burnAngle
        if burnDone == False:
            burnAngle = grav_adjustment(r, foc_x, foc_y, spacecraftPos, manuver_data[6], spacecraftVel, engineAccel(2.45e4, 8, 3.2e5, i*step, timeOffset), orig_angle)
        if spacecraftPos[0] != 0:
            theta = math.atan2(spacecraftPos[1], spacecraftPos[0])
        else:
            theta = math.pi/2
        burnTheta = (theta - math.pi/2) + burnAngle
        spacecraftVel[0] -= math.cos(theta)*(G*M/((r)**2))*step**2
        spacecraftVel[1] -= math.sin(theta)*(G*M/((r)**2))*step**2
        #burnDone = True
        if burnDone and not goingGown:
            if prev_vel < math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2):
                goingGown = True       
                arc_angle = math.atan2(spacecraftPos[0], spacecraftPos[1])
                dist = ((arc_angle*radius)/1000)
                print(f'Apoapsis Info {(r - radius)/1000} km, {i*step} s, {math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step} m/s, {math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r)))} required m/s, {burnAngle*(180/math.pi)} degrees, {orig_angle*(180/math.pi)} degrees, {dist} km downrange, {(2*(r)/radius)-focus_len} a, {spacecraftPos}, {[foc_x, foc_y]}')

        if not burnDone:
            if i == 0:
                firstAngle = burnAngle*(180/math.pi)
            #step is squared because you first convert into steps by multiplying by step. Then multiply by time (also step)
            spacecraftVel[0] += math.cos(burnTheta)*engineAccel(2.45e4, 8, 3.2e5, i*step, timeOffset)*step**2
            spacecraftVel[1] += math.sin(burnTheta)*engineAccel(2.45e4, 8, 3.2e5, i*step, timeOffset)*step**2
            dv += engineAccel(2.45e4, 8, 3.2e5, i*step, timeOffset)*step
            if ((math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step) > math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r)))):
                burnDone = True
                arc_angle = math.atan2(spacecraftPos[0], spacecraftPos[1])
                dist = ((arc_angle*radius)/1000)
                lastAngle = burnAngle*(180/math.pi)
                if not fullFlight:
                    break

        if i % 8000 == 0:
            xRes.append(spacecraftPos[0])
            yRes.append(spacecraftPos[1])
        
        prev_vel = math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)

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
            final_dist = ((radAngle*radius)/1000)
            break
    if fullFlight:
        return(final_dist)
    else:
        arc_angle = math.atan2(spacecraftPos[0], spacecraftPos[1])
        dist = ((arc_angle*radius)/1000)
        return(dist, dv, (r - radius)/1000, i*step, firstAngle, lastAngle)

