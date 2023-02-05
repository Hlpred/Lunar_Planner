import math
import matplotlib.pyplot as plt
import numpy as np
import Constants
import Lunar_planner

step = 0.0005
radius = Constants.radius
G = Constants.G
M = Constants.M

manuver_data = Lunar_planner.ele_adjustment(2564.25579, -2565 + 1331.86, -2375)

def engineAccel(wetMass, burnRate, thrust, time):
    return thrust / (wetMass - burnRate*time)

def ellipse_slope(point, x1, y1):
  return -(point[0]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[0]-x1)*math.sqrt(point[0]**2+point[1]**2)))/(point[1]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[1]-y1)*math.sqrt(point[0]**2+point[1]**2)))

def slope_to_angle(slope, point):
  return math.fabs(math.atan(slope)-math.atan(-point[0]/point[1]))

def grav_adjustment(target_aoa, r, engine_accel, centp_accel, correction):
  grav_accel = -((G*M)/r**2)
  #just go with it, I don't get it either
  net_accel = centp_accel + grav_accel
  a = net_accel/engine_accel
  b = math.tan(target_aoa)
  return 2*math.atan((math.sqrt(-a**2+b**2+1)-1)/(a+b))

def grav_adjustment2(target_aoa, r, engine_accel, centp_accel, v, v_angle):
    v_mag = math.sqrt((v[0]/step)**2 + (v[1]/step)**2)
    grav_accel = -((G*M)/r**2)
    net_accel = grav_accel + centp_accel
    a = 1 + (math.tan(target_aoa))**2
    b = 2*v_mag*math.cos(v_angle) + (net_accel + v_mag*math.sin(v_angle))*2*math.tan(target_aoa)
    c = (v_mag*math.cos(v_angle))**2 + (net_accel + v_mag*math.sin(v_angle))**2 - engine_accel**2
    quad_res = (b+math.sqrt((b**2)-4*a*c))/(2*a)
    y = math.tan(target_aoa)*quad_res - net_accel - v_mag*math.sin(v_angle)
    x = quad_res - v_mag*math.cos(v_angle)
    return math.atan(y/x)

def grav_adjustment3(r, foc_x, foc_y, pos, a, vel, a_s, path_angle):
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
#print(grav_adjustment(0, radius+10000, 10, (math.cos(0)*(math.sqrt(1675**2 + 0**2)))**2/(radius+10000))*(180/math.pi))
#startingEle, landingEle, totalVel, launchAngle

def simulate(startingEle, landingEle):
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
    #1/step is the time of one step in seconds
    foc_x = manuver_data[4]
    foc_y = manuver_data[5]
    half_center_angle = 2564.25579/(2*radius/1000)
    focus_len = math.sqrt(manuver_data[4]**2 + manuver_data[5]**2)
    focus_theta = math.atan2(manuver_data[5], manuver_data[4])
    new_theta = focus_theta - half_center_angle
    foc_x = focus_len*math.cos(new_theta)
    foc_y = focus_len*math.sin(new_theta)
    prev_vel = 0
    origPos = [0, radius + startingEle]
    origVel = [0, 0]
    for i in range(round((1/step)*100000)):
        spacecraftPos[0] += spacecraftVel[0]
        spacecraftPos[1] += spacecraftVel[1]
        r = math.sqrt(spacecraftPos[0]**2 + spacecraftPos[1]**2)
        slope = ellipse_slope([spacecraftPos[0]/radius, spacecraftPos[1]/radius], foc_x, foc_y)
        burnAngle = slope_to_angle(slope, [spacecraftPos[0]/radius, spacecraftPos[1]/radius])
        orig_angle = burnAngle
        #print((math.cos(burnAngle)*(math.sqrt((spacecraftVel[0]/step)**2 + (spacecraftVel[1]/step)**2))**2/(r)))
        #((math.cos(prev_angle)*math.sqrt(spacecraftVel[0]**2+spacecraftVel[1]**2)*math.tan(prev_angle))-(math.cos(prev_angle)*math.sqrt(spacecraftVel[0]**2+spacecraftVel[1]**2)*math.tan(orig_angle)))/step**2
        if not i == 0 and burnDone == False:
            #burnAngle = grav_adjustment(orig_angle, r, engineAccel(2.45e4, 8, 3.2e5, i*step), ((((math.sqrt((spacecraftVel[0]/step)**2 + (spacecraftVel[1]/step)**2)))**2)/(r)), (((theta - math.pi/2) + orig_angle)-math.atan((spacecraftVel[1])/(spacecraftVel[0]))))
            burnAngle = grav_adjustment3(r, foc_x, foc_y, spacecraftPos, manuver_data[6], spacecraftVel, engineAccel(2.45e4, 8, 3.2e5, i*step), orig_angle)
        else:
            #burnAngle = grav_adjustment(orig_angle, r, engineAccel(2.45e4, 8, 3.2e5, i*step), (((((math.sqrt((spacecraftVel[0]/step)**2 + (spacecraftVel[1]/step)**2)))**2)/(r))), 0)
            burnAngle = grav_adjustment3(r, foc_x, foc_y, spacecraftPos, manuver_data[6], spacecraftVel, engineAccel(2.45e4, 8, 3.2e5, i*step), orig_angle)
        if spacecraftPos[1] != 0:
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
                #print(f'Apoapsis hit at {(r-radius)/1000} km')
                #print(math.atan(spacecraftPos[1]/spacecraftPos[0]) - math.atan(foc_y/foc_x))
                arc_angle = math.atan2(spacecraftPos[0], spacecraftPos[1])
                dist = ((arc_angle*radius)/1000)
                print(f'Apoapsis Info {(r - radius)/1000} km, {i*step} s, {math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step} m/s, {math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r)))} required m/s, {burnAngle*(180/math.pi)} degrees, {orig_angle*(180/math.pi)} degrees, {dist} km downrange, {(2*(r)/radius)-focus_len} a, {spacecraftPos}, {[foc_x, foc_y]}')

        if (i*step == 58 or i*step == 29 or i == 1):
            arc_angle = math.atan2(spacecraftPos[0], spacecraftPos[1])
            dist = ((arc_angle*radius)/1000)
            print(f'Update {(r - radius)/1000} km, {i*step} s, {math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step} m/s, {math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r)))} required m/s, {burnAngle*(180/math.pi)} degrees, {orig_angle*(180/math.pi)} degrees, {dist} km downrange, {spacecraftPos}, {[foc_x, foc_y]}, {spacecraftVel}, {slope}, {orig_angle}, {prev_angle} {burnAngle}, {((math.cos(orig_angle)**2)*(math.sqrt((spacecraftVel[0]/step)**2 + (spacecraftVel[1]/step)**2))**2/(r))}, {engineAccel(2.45e4, 8, 3.2e5, i*step)}, {-((G*M)/r**2)}, {(theta - math.pi/2) + orig_angle}, {(((theta - math.pi/2) + orig_angle)-math.atan((spacecraftVel[1])/(spacecraftVel[0])))*(180/math.pi)}')

        if not burnDone:
            #step is squared because you first convert into steps by multiplying by step. Then multiply by time (also step)
            spacecraftVel[0] += math.cos(burnTheta)*engineAccel(2.45e4, 8, 3.2e5, i*step)*step**2
            spacecraftVel[1] += math.sin(burnTheta)*engineAccel(2.45e4, 8, 3.2e5, i*step)*step**2
            if ((math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step) > math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r)))):
                #spacecraftVel[0] += 0.48816*step
                #spacecraftVel[1] += 0.87275*step
                burnDone = True
                arc_angle = math.atan2(spacecraftPos[0], spacecraftPos[1])
                dist = ((arc_angle*radius)/1000)
                print(f'Cutoff at {(r - radius)/1000} km, {i*step} s, {math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step} m/s, {math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r)))} required m/s, {burnAngle*(180/math.pi)} degrees, {orig_angle*(180/math.pi)} degrees, {dist} km downrange, {spacecraftPos}, {[foc_x, foc_y]}, {spacecraftVel}, {slope}, {(((theta - math.pi/2) + orig_angle)-math.atan((spacecraftVel[1])/(spacecraftVel[0])))*(180/math.pi)}')
        
        if i % 8000 == 0:
            #print(spacecraftVel[0]/step)
            #print(math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)/step)
            #print(spacecraftVel[0]/step, spacecraftVel[1]/step)
            #print(burnAngle*(180/math.pi))
            #print(slope)
            #print(orig_angle*180/math.pi)
            #print(burnTheta*180/math.pi)
            if not i==0:
                #print((((math.cos(orig_angle)*(math.sqrt((spacecraftVel[0]/step)**2 + (spacecraftVel[1]/step)**2)))**2)/(r)))
                print((((theta - math.pi/2) + orig_angle)-math.atan((origVel[1])/(origVel[0]))))
                #print(grav_adjustment3(r, foc_x, foc_y, spacecraftPos, manuver_data[6], spacecraftVel, engineAccel(2.45e4, 8, 3.2e5, i*step), orig_angle))
                #print((math.sqrt((spacecraftVel[0]/step)**2 + (spacecraftVel[1]/step)**2))/math.sqrt(2*(((-G*M))/(manuver_data[6]*radius)+(G*M)/(r))))
                #print((math.sqrt(spacecraftVel[0]**2+spacecraftVel[1]**2)*math.tan(prev_angle)-math.sqrt(spacecraftVel[0]**2+spacecraftVel[1]**2)*math.tan(orig_angle))/step)
                #this one
                #print((math.atan((spacecraftVel[1])/(spacecraftVel[0]))-math.atan((spacecraftPos[1] - origPos[1])/(spacecraftPos[0] - origPos[0])))*180/math.pi)
                #print((spacecraftPos[1]-origPos[1])-spacecraftVel[1])
                #print((math.atan((spacecraftVel[1]-origVel[1])/(spacecraftVel[0]-origVel[0]))-orig_angle)*(180/math.pi))
                #print((math.atan((spacecraftVel[1]-origVel[1])/(spacecraftVel[0]-origVel[0]))-((theta - math.pi/2) + orig_angle))*(180/math.pi))
                #print(math.atan((spacecraftPos[1]-origPos[1])/(spacecraftPos[0]-origPos[0])))
                #print(burnTheta)

            xRes.append(spacecraftPos[0])
            yRes.append(spacecraftPos[1])
        prev_angle = orig_angle
        prev_vel = math.sqrt(spacecraftVel[0]**2 + spacecraftVel[1]**2)
        origPos = [spacecraftPos[0], spacecraftPos[1]]
        origVel = [spacecraftVel[0], spacecraftVel[1]]

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
    #return(final_dist+76.94652849853868)
    return(final_dist)

#print(simulate(-2565+1330, -1875, 0, 0, 30.1, 116.932))
#print(simulate(40000-8000-1875, -1875, -24, 1400, 151.9, 110))
#print(simulate(347480, -1875, 0, 138.127, 150, 100, 15))
#print(simulate(1333, -1875, 0, 0, 30, 119.21, 13.061))
print(simulate(-2565 + 1331.86, -3375 + 1000))
#Cutoff at 33.02987388779363 km, 116.4745 s, 1469.71914192943 m/s, 1469.7175295840195 required m/s, 24.889021989871136 degrees, 23.174841310680733 degrees, 76.94652849853868 km downrange
#print(simulate(33.02987388779363*1000, -2375, 1469.71914192943, 23.174841310680733))
#Cutoff at 33.02987388779363 km, 116.4745 s, 1469.71914192943 m/s, 1469.7175295840195 required m/s, 24.889021989871136 degrees, 23.174841310680733 degrees, 76.94652849853868 km downrange, [78383.73591669081, 1768693.848097542], [0.4968276407264363, 0.5471707456184456]
