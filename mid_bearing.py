import math
import Constants


#calculates the midpoint between two bearings in degrees
def midBearing(A, B):
    if math.fabs(A-B) > 180:
        return ((((A+B)/2)+180)%360, 360-math.fabs(A-B))
    else:
        return ((A+B)/2, math.fabs((A-B)))

#calculates the time required to yaw that angular distance
def deltaThetaTime(wetMass, yawChange, safetyFactor):
    alpha = (Constants.yaw_torque/(wetMass*Constants.yaw_inertia))*180/math.pi
    print(alpha)
    return 2*math.sqrt(yawChange/alpha)*safetyFactor