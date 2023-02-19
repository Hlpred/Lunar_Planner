from itertools import permutations
import Lunar_planner
import webbrowser

def shortest_distance(points, closed_loop=False, fixed_start=True):
    """
    Find the shortest path that visits all the points in a set on a sphere.

    Args:
    points: list of tuples, each representing a point on the sphere as a latitude and longitude pair (in degrees)

    Returns:
    float, the length of the shortest path that visits all the points (in kilometers)
    list, the original list of points in their new order after finding the shortest path
    """
    min_distance = float("inf")
    min_path = []
    for path in permutations(points):
        if path[0] == points[0] or not fixed_start:
            distance = 0
            for i in range(len(path) - 1):
                distance += Lunar_planner.calculate_distance(path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])
            if closed_loop:
                distance += Lunar_planner.calculate_distance(path[-1][0], path[-1][1], path[0][0], path[0][1])
            if distance < min_distance:
                min_distance = distance
                min_path = list(path)

    output_path = min_path
    lineArray = []
    for point in output_path:
        tempStr = str(point[0]) + '%2C' + str(point[1])
        lineArray.append(tempStr)
    line = '%2C'.join(lineArray)
    if closed_loop:
        line += '%2C' + str(points[0][0]) + '%2C' + str(points[0][1])
    url = f'https://quickmap.lroc.asu.edu/query?camera=8722239.073%2C0.000%2C0.000%2C6.283%2C-1.571%2C0.000%2C8722239.073%2C60.000&id=lroc&showTerrain=true&queryFeature=0&queryOpts=N4IgLghgRiBcIBMKRAXyA&features={line}&layers=NrBsFYBoAZIRnpEBmZcAsjYIHYFcAbAyAbwF8BdC0ypcOKbRFOOZLRfImqnioA&proj=22'
    return url

webbrowser.open(shortest_distance(points, False, False))

