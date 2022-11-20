# Python 3 program to calculate Distance Between Two Points on the Moon
from math import *
import math
from lxml import etree
import difflib
import webbrowser
from scipy.optimize import fsolve

ns = {"kml": "http://www.opengis.net/kml/2.2"}

tree = etree.parse("MOON_nomenclature_center_pts.kml")

nameList = []
nameListLower = []
for simple_data in tree.xpath("/kml:kml/kml:Document/kml:Folder/kml:Placemark/kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name='clean_name']", namespaces=ns):
  nameList.append(simple_data.text)
  nameListLower.append(simple_data.text.lower())
latList = []
for simple_data in tree.xpath("/kml:kml/kml:Document/kml:Folder/kml:Placemark/kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name='center_lat']", namespaces=ns):
  latList.append(simple_data.text)
lonList = []
for simple_data in tree.xpath("/kml:kml/kml:Document/kml:Folder/kml:Placemark/kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name='center_lon']", namespaces=ns):
  lonList.append(simple_data.text)
quadList = []
for simple_data in tree.xpath("/kml:kml/kml:Document/kml:Folder/kml:Placemark/kml:ExtendedData/kml:SchemaData/kml:SimpleData[@name='quad_code']", namespaces=ns):
  quadList.append(simple_data.text)

r = 1737.4
radius = 1.7374e6
G = 6.67e-11
M = 7.347e22

#def calculate_distance(lat1 = 33.438, lon1 = 41.125,  lat2, lon2):

def calculate_distance(lat1, lon1,  lat2, lon2):
	
	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

	c = 2 * asin(sqrt(a))
	
	# calculate the result
	return(c * r)

def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)* math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below

    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def ellipse_slope(point, x1, y1):
  #-(point[0]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[0]-x1)*math.sqrt(point[0]**2+point[1]**2)))/(point[1]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[1]-y1)*math.sqrt(point[0]**2+point[1]**2)))
  return -(point[0]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[0]-x1)*math.sqrt(point[0]**2+point[1]**2)))/(point[1]*(math.sqrt((point[1]-y1)**2+(point[0]-x1)**2))+((point[1]-y1)*math.sqrt(point[0]**2+point[1]**2)))

def slope_to_angle(slope, point):
  return math.fabs(atan(slope)*(180/math.pi)-atan(-point[0]/point[1])*(180/math.pi))

def ele_adjustment(distance, launch_ele, land_ele):
  angle_from_vertical = distance/(2*math.pi*r)*math.pi
  inital_x_coord = math.sin(angle_from_vertical)
  inital_y_coord = math.cos(angle_from_vertical)
  point1 = [(-inital_x_coord)-(inital_x_coord*(launch_ele/radius)), inital_y_coord+(inital_y_coord*(launch_ele/radius))]
  point2 = [(inital_x_coord+(inital_x_coord*(land_ele/radius))), inital_y_coord+(inital_y_coord*(land_ele/radius))]
  straight_dist = math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)
  double_a = (straight_dist+math.sqrt(point1[0]**2+point1[1]**2)+math.sqrt(point2[0]**2+point2[1]**2))/2
  m = ((point1[1]-point2[1])/(point1[0]-point2[0]))
  x1 = (math.cos(atan(m))*(double_a-math.sqrt(point1[0]**2+point1[1]**2)))+point1[0]
  y1 = (math.sin(atan(m))*(double_a-math.sqrt(point1[0]**2+point1[1]**2)))+point1[1]
  slope1 = ellipse_slope(point1, x1, y1)
  slope2 = ellipse_slope(point2, x1, y1)
  angle1 = slope_to_angle(slope1, point1)
  angle2 = slope_to_angle(slope2, point2)
  v1 = math.sqrt(2*(((-G*M))/(double_a*radius)+(G*M)/(radius+launch_ele)))
  v2 = math.sqrt(2*(((-G*M))/(double_a*radius)+(G*M)/(radius+land_ele)))
  """
  grav_result1 = grav_adjustment(angle1, v1, engine_accel1)
  aoa1 = grav_result1[0]
  delta_v1 = grav_result1[1]
  grav_result2 = grav_adjustment(angle2, v2, engine_accel2)
  aoa2 = grav_result2[0]
  delta_v2 = grav_result2[1]
  x_vel = math.cos(aoa2*(math.pi/180))*delta_v2
  """
  return angle1, angle2, v1, v2

def grav_adjustment(target_aoa, v, engine_accel):
  target_aoa = target_aoa*(math.pi/180)
  grav_accel = -((G*M)/radius**2)
  def f(x):
    return target_aoa-atan2(math.sin(x)+(grav_accel/engine_accel), math.cos(x))
  x0 = target_aoa
  x = fsolve(f, x0)
  res_angle = x[0]
  return(res_angle*(180/math.pi), (v*math.cos(target_aoa))/math.cos(res_angle))

def findPoint(place):
  point = []
  if ',' in place:
    point = place.split(', ')
    point = [float(i) for i in point]
  else:
    if place == 'base' or place == 'Base':
      point = (41.125, 326.562)
    else:
      foundLoc = False
      for i, name in enumerate(nameListLower):
        if place.lower() == name:
          point.append(float(latList[i]))
          point.append(float(lonList[i]))
          foundLoc = True
          quad1 = quadList[i]
      if foundLoc == False:
        matchList = difflib.get_close_matches(place.lower(), nameListLower)
        i = nameListLower.index(matchList[0])
        print(f'We couldn\'t find the location {place}. Did you mean {nameList[i]}?')
        acceptSuggestion = input('Y/N: ')
        if acceptSuggestion == 'Y' or 'y':
          point.append(float(latList[i]))
          point.append(float(lonList[i]))
  return point

quad1 = ''
quad2 = ''

place1 = input('Enter your starting location: ')
place2 = input('Enter your desired destination: ')

point1 = tuple(findPoint(place1))
point2 = tuple(findPoint(place2))

distance = calculate_distance(point1[0], point1[1], point2[0], point2[1])
print(f'Your selected target is at a bearing of {round(calculate_initial_compass_bearing(point1, point2),2)} degrees from your current location')
print(f'The two points are {round(distance,5)} km apart')
url = f'https://quickmap.lroc.asu.edu/query?camera=8722239.073%2C0.000%2C0.000%2C6.283%2C-1.571%2C0.000%2C8722239.073%2C60.000&id=lroc&showTerrain=true&queryFeature=0&queryOpts=N4IgLghgRiBcIBMKRAXyA&features={point1[1]}%2C{point1[0]}%2C{point2[1]}%2C{point2[0]}&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0ypcOKbRFOOZLRfImqnioA&proj=22'
webbrowser.open(url)
launch_ele = float(input('Enter the elevation of your launching location in meters: '))
land_ele = float(input('Enter the elevation of your landing location in meters: '))
maneuver_data = ele_adjustment(distance, launch_ele, land_ele)
engine_accel1 = float(input('Enter the current acceleration of your engine: '))
grav_data1 = grav_adjustment(maneuver_data[0], maneuver_data[2], engine_accel1)
print('Adjusted for burn time:')
print(f'The optimal angle of attack for launch is {round(grav_data1[0],5)} degrees above horizontal')
print(f'The optimal delta V for launch is {round(grav_data1[1],5)} m/s')
print('After first burn:')
engine_accel2 = float(input('Enter the current acceleration of your engine: '))
grav_data2 = grav_adjustment(maneuver_data[1], maneuver_data[3], engine_accel2)
print('Adjusted for burn time:')
print(f'The optimal angle of attack for landing is {round(grav_data2[0],5)} degrees above horizontal')
print(f'The optimal delta V for landing is {round(grav_data2[1],5)} m/s')

#url1 = 'https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/Lunar/lac_' + quad1[4:] + '_wac.pdf'
#url2 = 'https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/Lunar/lac_' + quad2[4:] + '_wac.pdf'
#webbrowser.open(url1)
#webbrowser.open(url2)
