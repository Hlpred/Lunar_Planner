import math

radius = 1.7374e6
G = 6.67e-11
M = 7.347e22

height = 30000
v = -480
landing_ele = -2564
grav = -((G*M)/radius**2)
ship = 10
net = ship+grav

print(grav)

def height_fun(t):
    return 0.5*(grav)*t**2 + v*t + height

a = ((grav**2/(2*net))-(grav/2))
b = (-v+((v*grav)/net))
c = -height+landing_ele+((v**2)/(2*net))
sol1 = (-b + math.sqrt(b**2-(4*a*c)))/(2*a)
sol2 = (-b - math.sqrt(b**2-(4*a*c)))/(2*a)

if sol1 >= sol2:
    print(sol1)
    print(height_fun(sol1))
else:
    print(sol2)
    print(height_fun(sol2))