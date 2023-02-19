import webbrowser
from Orbit_simulator import simulate
from Lunar_planner import *
import Elevation_margins
from Route_Planner2 import routePlan
import ast

input_path = input('Enter a list of points to visit with your starting point first: ')
input_path = ast.literal_eval(input_path)
print(input_path)
output_path = routePlan(input_path)
print(output_path)
for i in range(len(output_path)):
    if i != (len(output_path) - 1):
        point1 = output_path[i]
        point2 = output_path[i+1]
        #place1 = input('Enter your starting location: ')
        #place2 = input('Enter your desired destination: ')

        #point1 = tuple(findPoint(place1))
        #point2 = tuple(findPoint(place2))
        distance = calculate_distance(point1[1], point1[0], point2[1], point2[0])
        print(f'Your selected target is at a bearing of {round(calculate_initial_compass_bearing([point1[1], point1[0]], [point2[1], point2[0]]),2)} degrees from your current location')
        print(f'The two points are {round(distance,5)} km apart')
        #url = f'https://quickmap.lroc.asu.edu/query?camera=8722239.073%2C0.000%2C0.000%2C6.283%2C-1.571%2C0.000%2C8722239.073%2C60.000&id=lroc&showTerrain=true&queryFeature=0&queryOpts=N4IgLghgRiBcIBMKRAXyA&features={point1[0]}%2C{point1[1]}%2C{point2[0]}%2C{point2[1]}&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0ypcOKbRFOOZLRfImqnioA&proj=22'
        #webbrowser.open(url)
        launch_ele = float(input('Enter the elevation of your launching location in meters: '))
        land_ele = float(input('Enter the elevation of your landing location in meters: '))
        hover_accel1 = float(input('What is the current acceleration of your hover engines?: '))
        launch_margin = float(input('How much launch margin do you want in s?: '))
        launch_margin = Elevation_margins.launch_height(launch_margin, hover_accel1, launch_ele)
        print(round(launch_margin,2))
        landing_margin = float(input('How much landing margin do you want in m?: '))
        main_prop_mass = float(input('Enter your current main propellent mass in kg:'))
        RCS_prop_mass = float(input('Enter your current RCS propellent mass in kg:'))
        wetMass = main_prop_mass + RCS_prop_mass
        sim_data = simulate(distance, launch_ele+launch_margin, land_ele+landing_margin, False, wetMass)
        print(f'Delta-v: {round(sim_data[1],3)} m/s\nStart angle: {round(sim_data[4],2)}°\nEnd angle: {round(sim_data[5],2)}°')
        hover_accel2 = float(input('What is your hover engine acceleration?: '))
        burn_height = Elevation_margins.landing_burn_height(land_ele+landing_margin, 0, land_ele, hover_accel2)
        print(f'Set altitude hold to {land_ele} m and engage altitude hold at {round(burn_height-land_ele,2)} m above the ground')
        print('Deorbit Burn')
        sim_data2 = simulate(distance, land_ele+landing_margin, launch_ele+launch_margin, False, wetMass)
        print(f'Relight distance: {round(sim_data2[0],3)} km\nStart angle: {round(sim_data2[5],2)}°\nEnd angle: {round(sim_data2[4],2)}°')



