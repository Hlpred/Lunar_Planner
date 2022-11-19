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

def launch_vector_angle(distance):
    o = math.sin((math.pi*distance)/(r*2*math.pi))
    y1 = math.sqrt(1 - o**2)
    m1 = (math.sqrt(y1**2 + o**2) + o)/y1
    slope1 = math.degrees(atan(m1))
    slope2 = math.degrees(atan2(o, y1))
    return slope1-slope2

def angle_of_attack(distance):
  Aoa = launch_vector_angle(distance)*(math.pi/180)
  engine_accel = 22
  v = velocity(distance)
  t = v/engine_accel
  grav_vel = t*((G*M)/radius**2)
  def f(x):
    return Aoa-atan2(v*math.sin(x)-grav_vel, v*math.cos(x))
  x0 = Aoa
  x = fsolve(f, x0)
  return(x[0]*(180/math.pi))

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

def velocity(distance):
  semi_major_axis = (math.sin((math.pi*distance)/(r*2*math.pi)) + 1)/2
  return math.sqrt(2*((-(G*M)/(2*(semi_major_axis*radius)))+((G*M)/radius)))

quad1 = ''
quad2 = ''

place1 = input('Enter your starting location: ')
place2 = input('Enter your desired destination: ')

point1 = tuple(findPoint(place1))
point2 = tuple(findPoint(place2))


distance = calculate_distance(point1[0], point1[1], point2[0], point2[1])
print(f'Your selected target is at a bearing of {round(calculate_initial_compass_bearing(point1, point2),2)} degrees from your current location')
print(f'The two points are {round(distance,5)} km apart')
print(f'The optimal launch vector to reach this distance is {round(launch_vector_angle(distance),5)} degrees above horizontal')
print(f'The optimal angle of attack to for this launch vector is {round(angle_of_attack(distance),5)}')
print(f'The optimal velocity for this path is {round(velocity(distance),5)}')
print('Have a safe flight commander')

#url1 = 'https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/Lunar/lac_' + quad1[4:] + '_wac.pdf'
#url2 = 'https://asc-planetarynames-data.s3.us-west-2.amazonaws.com/Lunar/lac_' + quad2[4:] + '_wac.pdf'
#webbrowser.open(url1)
#webbrowser.open(url2)

url = f'https://quickmap.lroc.asu.edu/query?camera=8722239.073%2C0.000%2C0.000%2C6.283%2C-1.571%2C0.000%2C8722239.073%2C60.000&id=lroc&showTerrain=true&queryFeature=0&queryOpts=N4IgLghgRiBcIBMKRAXyA&features={point1[1]}%2C{point1[0]}%2C{point2[1]}%2C{point2[0]}&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0ypcOKbRFOOZLRfImqnioA&proj=22'
webbrowser.open(url)
