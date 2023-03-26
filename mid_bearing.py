import math
import Constants

def midBearing(A, B):
    if math.fabs(A-B) > 180:
        return ((((A+B)/2)+180)%360, 360-math.fabs(A-B))
    else:
        return ((A+B)/2, math.fabs((A-B)))

def deltaThetaTime(wetMass, yawChange, safetyFactor):
    alpha = (Constants.yaw_torque/(wetMass*Constants.yaw_inertia))*180/math.pi
    print(alpha)
    return 2*math.sqrt(yawChange/alpha)*safetyFactor

bearing = midBearing(90, 0)
print(bearing[0])
print(deltaThetaTime(24385.66, bearing[1], 1))