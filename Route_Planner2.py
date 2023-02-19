from py2opt.routefinder import RouteFinder
from Lunar_planner import calculate_distance
import webbrowser

def routePlan(city_names):
    dist_mat = []
    tempArr = []
    for i in city_names:
        tempArr = []
        for j in city_names:
            tempArr.append(calculate_distance(i[1], i[0], j[1], j[0]))
        dist_mat.append(tempArr)
    print(len(dist_mat))
    route_finder = RouteFinder(dist_mat, city_names, iterations=20)
    best_distance, best_route = route_finder.solve()
    lineArray = []
    for point in best_route:
        tempStr = str(point[0]) + '%2C' + str(point[1])
        lineArray.append(tempStr)
    line = '%2C'.join(lineArray)
    url = f'https://quickmap.lroc.asu.edu/query?camera=8722239.073%2C0.000%2C0.000%2C6.283%2C-1.571%2C0.000%2C8722239.073%2C60.000&id=lroc&showTerrain=true&queryFeature=0&queryOpts=N4IgLghgRiBcIBMKRAXyA&features={line}&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0ypcOKbRFOOZLRfImqnioA&proj=22'
    webbrowser.open(url)
    return best_route