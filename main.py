import webbrowser
import Orbit_simulator
from Lunar_planner import *
import Elevation_margins
from Route_Planner import routePlan
import ast
import Constants
import mid_bearing

input_path = input('Enter a list of lattitude and longitude points to visit with your starting point first (e.g. [[-73.663998,34.04992],[45.57348,-34.835811]]): ')
input_path = ast.literal_eval(input_path)
print(input_path)
#reorders the locations to shorten the distance of the path
output_path = routePlan(input_path)
#does the launch and landing procedure for every location in the optimized path
for i in range(len(output_path)):
    if i != (len(output_path) - 1):
        point1 = output_path[i]
        point2 = output_path[i+1]
        distance = calculate_distance(point1[1], point1[0], point2[1], point2[0])
        target_heading = calculate_initial_compass_bearing([point1[1], point1[0]], [point2[1], point2[0]])
        print(f'Your selected target is at a bearing of {round(target_heading,2)} degrees from your current location')
        print(f'The two points are {round(distance,5)} km apart')
        
        #Opens a new map every time you start a new segment of the path
        #url = f'https://quickmap.lroc.asu.edu/query?camera=8722239.073%2C0.000%2C0.000%2C6.283%2C-1.571%2C0.000%2C8722239.073%2C60.000&id=lroc&showTerrain=true&queryFeature=0&queryOpts=N4IgLghgRiBcIBMKRAXyA&features={point1[0]}%2C{point1[1]}%2C{point2[0]}%2C{point2[1]}&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0ypcOKbRFOOZLRfImqnioA&proj=22'
        #webbrowser.open(url)
        
        #Adds 20 meters to account for hovering above the ground before the main burn (gives the spacecraft time to reorient and pitch up)
        launch_ele = float(input('Enter the elevation of your launching location in meters: ')) + 20
        land_ele = float(input('Enter the elevation of your landing location in meters: '))
        landing_margin = float(input('How much landing margin (height above the ground when deorbit burn finishes) do you want in m?: '))
        main_prop_mass = float(input('Enter your current main propellent mass in kg: '))
        RCS_prop_mass = float(input('Enter your current RCS propellent mass in kg: '))
        heading = float(input('What\'s your current heading in degrees: '))
        print('Calculating Launch Values')
        totalMass = main_prop_mass + RCS_prop_mass + Constants.Dry_mass
        hover_accel1 = Elevation_margins.hover_accel(totalMass)
        sim_data1 = Orbit_simulator.simulate(distance, [launch_ele, land_ele+landing_margin], False, totalMass, True)
        bearing = mid_bearing.midBearing(heading, target_heading)
        print(f'Delta-v: {round(sim_data1[1],3)} m/s\nHeading Alignment Midpoint: {round(bearing[0],2)}°\nEnding Heading: {round(target_heading,2)}°\nStart angle: {round(sim_data1[4],2)}°\nEnd angle: {round(sim_data1[5],2)}°')
        input('Press enter when ready for deorbit')
        print('Calculating Deorbit Values')
        sim_data2 = Orbit_simulator.land_estimate(distance, [launch_ele, land_ele+landing_margin], sim_data1[6], sim_data1[1])
        print(f'Range: {round(sim_data2[0],3)} km\nDelta-v: {round(sim_data2[1],3)} m/s\nStart angle: {round(sim_data2[5],2)}°\nEnd angle: {round(sim_data2[4],2)}°')
        print('Landing Procedure: ')
        landing_margin = float(input('How far are you above the ground in meters: '))
        vertical_vel = float(input('What\'s your current vertical velocity in m/s: '))
        hover_accel2 = Orbit_simulator.engineAccel(totalMass, Constants.hover_burn_rate, Constants.hover_thrust, sim_data1[7] + sim_data2[7], True)
        burn_height = Elevation_margins.landing_burn_height(land_ele+landing_margin, vertical_vel, land_ele, hover_accel2)
        print(f'Set altitude hold to {land_ele} m and engage altitude hold at {round(burn_height-land_ele,2)} m above the ground')



