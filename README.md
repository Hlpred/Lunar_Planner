# Lunar Planner

## What is the Lunar Planner?
The Lunar Planner is a Python program that simulates an efficient way to get between a set of points on the lunar surface with a spacecraft. This means calculating an efficient route between a set of latitude and longitude points, calculating the orbital path that connects adjacent points, and simulating the burns that put the spacecraft into and out of orbit. It was designed for planning lunar flights in the spaceflight simulator Orbiter 2016, but in principle, it could be used for any similar simulator. 

## How do I use the Lunar Planner?
Once you've cloned the repository, simply run main.py. The terminal will ask you for various pieces of information like the locations you want to visit and the status of your spacecraft during the flight. Note that simulating the burns and the orbit itself could take a little while depending on the performance of your computer. Also, note that this program will open your browser and show
a map of the route it comes up with. This is done with a website called Lunar QuickMap (https://quickmap.lroc.asu.edu/?extent=-90%2C-26.928829%2C90%2C26.928829&id=lroc&showTerrain=true&queryOpts=N4XyA&trailType=0&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0yioA&proj=10).
