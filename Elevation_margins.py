import math
import Constants

radius = Constants.radius
G = Constants.G
M = Constants.M

def height_fun(a, t, v, h):
    return 0.5*(a)*t**2 + v*t + h

def launch_height(t1, ship_accel, launch_ele):
    grav = -((G*M)/((radius+launch_ele)**2))
    net = ship_accel+grav
    v = net*t1
    t2 = math.fabs(v/grav)
    powered_height = height_fun(net, t1, 0, 0)
    coast_height = height_fun(grav, t2, v, 0)
    return(powered_height + coast_height)

def landing_burn_height(height, v, landing_ele, ship_accl):
    grav = -((G*M)/((radius+landing_ele)**2))
    net = ship_accl+grav

    a = ((grav**2/(2*net))-(grav/2))
    b = (-v+((v*grav)/net))
    c = -height+landing_ele+((v**2)/(2*net))
    sol1 = (-b + math.sqrt(b**2-(4*a*c)))/(2*a)
    sol2 = (-b - math.sqrt(b**2-(4*a*c)))/(2*a)

    if sol1 >= sol2:
        return height_fun(grav, sol1, v, height)
    else:
        return height_fun(grav, sol2, v, height)