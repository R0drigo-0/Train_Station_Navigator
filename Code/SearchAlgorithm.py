from TrainStationsMap import *
from utils import *
import math
import copy
import os


def expand(path, map):
    """
    It expands a SINGLE station and returns the list of class Path.
    Format of the parameter is:
       Args:
           path (object of Path class): Specific path to be expanded
           map (object of Map class):: All the information needed to expand the node
       Returns:
           path_list (list): List of paths that are connected to the given path.
    """
    path_list = []
    for i in map.connections[path.last].keys():
        aux_path = copy.deepcopy(path.route)
        path_list.append(Path(aux_path + [i]))

    for i in path_list:
        i.g = path.g
        i.h = path.h
        i.f = path.f

    return list(path_list)


def remove_cycles(path_list):
    """
    It removes from path_list the set of paths that include some cycles in their path.
    Format of the parameter is:
       Args:
           path_list (LIST of Path Class): Expanded paths
       Returns:
           path_list (list): Expanded paths without cycles.
    """

    aux = copy.deepcopy(path_list)
    for i in path_list:
        if i.route[-1] in i.route[0:-1:1]:
            aux.remove(i)

    return list(aux)


def insert_depth_first_search(expand_paths, list_of_path):
    """
    expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
           list_of_path (LIST of Path Class): The paths to be visited
       Returns:
           list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list(expand_paths + list_of_path)


def depth_first_search(origin_id, destination_id, map):
    """
    Depth First Search algorithm
    Format of the parameter is:
       Args:
           origin_id (int): Starting station id
           destination_id (int): Final station id
           map (object of Map class): All the map information
       Returns:
           list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """

    path_list = [Path(origin_id)]
    while path_list and path_list[0].last != destination_id:
        expand_paths = expand(path_list[0], map)
        expand_paths = remove_cycles(expand_paths)

        path_list.pop(0)
        path_list = insert_depth_first_search(expand_paths, path_list)

    if path_list:
        return path_list[0]
    return []


def insert_breadth_first_search(expand_paths, list_of_path):
    """
    expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
           list_of_path (LIST of Path Class): The paths to be visited
       Returns:
           list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list(list_of_path + expand_paths)


def breadth_first_search(origin_id, destination_id, map):
    """
    Breadth First Search algorithm
    Format of the parameter is:
       Args:
           origin_id (int): Starting station id
           destination_id (int): Final station id
           map (object of Map class): All the map information
       Returns:
           list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    path_list = [Path(origin_id)]
    while path_list and path_list[0].last != destination_id:
        expand_paths = expand(path_list[0], map)
        expand_paths = remove_cycles(expand_paths)

        path_list.pop(0)
        path_list = insert_breadth_first_search(expand_paths, path_list)

    if path_list:
        return path_list[0]
    return []


def calculate_cost(expand_paths, map, type_preference=0):
    """
    Calculate the cost according to type preference
    Format of the parameter is:
       Args:
           expand_paths (LIST of Paths Class): Expanded paths
           map (object of Map class): All the map information
           type_preference: INTEGER Value to indicate the preference selected:
                           0 - Adjacency
                           1 - minimum Time
                           2 - minimum Distance
                           3 - minimum Transfers
       Returns:
           expand_paths (LIST of Paths): Expanded path with updated cost
    """

    if type_preference == 0:
        for i in expand_paths:
            i.update_g(1)

    elif type_preference == 1:
        for i in expand_paths:
            i.update_g(map.connections[i.penultimate][i.last])

    elif type_preference == 2:
        for i in expand_paths:
            aux_last = map.stations[i.last]
            aux_penultimate = map.stations[i.penultimate]

            vel = 0

            if aux_last["name"] != aux_penultimate["name"]:
                vel = aux_last["velocity"]

            sec = map.connections[i.penultimate][i.last]
            i.update_g(vel * sec)

    elif type_preference == 3:
        for i in expand_paths:
            aux_last = map.stations[i.last]
            aux_penultimate = map.stations[i.penultimate]
            if aux_last["name"] == aux_penultimate["name"]:
                i.update_g(1)

    else:
        raise Exception(
            "Not a valid number for type preference in calculate cost function"
        )

    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
    expand_paths is inserted to the list_of_path according to COST VALUE
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
           list_of_path (LIST of Path Class): The paths to be visited
       Returns:
           list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """

    list_of_path.extend(expand_paths)
    aux_sorted = sorted(list_of_path, key=lambda i: i.g)
    list_of_path = aux_sorted
    return aux_sorted


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
    Uniform Cost Search algorithm
    Format of the parameter is:
       Args:
           origin_id (int): Starting station id
           destination_id (int): Final station id
           map (object of Map class): All the map information
           type_preference: INTEGER Value to indicate the preference selected:
                           0 - Adjacency
                           1 - minimum Time
                           2 - minimum Distance
                           3 - minimum Transfers
       Returns:
           list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """

    path_list = [Path(origin_id)]
    while path_list and path_list[0].last != destination_id:
        expand_paths = expand(path_list[0], map)
        expand_paths = remove_cycles(expand_paths)
        expand_paths = calculate_cost(expand_paths, map, type_preference)

        path_list.pop(0)
        path_list = insert_cost(expand_paths, path_list)

    if path_list:
        return path_list[0]
    return []


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
    Calculate and UPDATE the heuristics of a path according to type preference
    WARNING: In calculate_cost, we didn't update the cost of the path inside the function
             for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
           map (object of Map class): All the map information
           destination_id (int): Final station id
           type_preference: INTEGER Value to indicate the preference selected:
                           0 - Adjacency
                           1 - minimum Time
                           2 - minimum Distance
                           3 - minimum Transfers
       Returns:
           expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """

    if type_preference == 0:
        for i in expand_paths:
            aux = 0
            if i.last != destination_id:
                aux = 1
            i.update_h(aux)

    elif type_preference == 1:
        for i in expand_paths:
            vel = max([map.stations[j]["velocity"] for j in map.stations])

            aux_last = map.stations[i.last]
            aux_last = [aux_last["x"], aux_last["y"]]

            destination = map.stations[destination_id]
            destination = [destination["x"], destination["y"]]

            dist = euclidean_dist(destination, aux_last)

            i.update_h(dist / vel)

    elif type_preference == 2:
        for i in expand_paths:
            aux_last = map.stations[i.last]
            aux_last = [aux_last["x"], aux_last["y"]]

            destination = map.stations[destination_id]
            destination = [destination["x"], destination["y"]]

            dist = euclidean_dist(destination, aux_last)

            i.update_h(dist)

    elif type_preference == 3:
        for i in expand_paths:
            aux = 0
            if map.stations[i.last]["line"] != map.stations[destination_id]["line"]:
                aux = 1

            i.update_h(aux)
    else:
        raise Exception(
            "Not a valid number for type preference in calculate heuristic function"
        )

    return expand_paths


def update_f(expand_paths):
    """
    Update the f of a path
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
       Returns:
           expand_paths (LIST of Path Class): Expanded paths with updated costs
    """

    for i in expand_paths:
        i.update_f()

    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
    It removes the Redundant Paths. They are not optimal solution!
    If a station is visited and have a lower g-cost at this moment, we should remove this path.
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
           list_of_path (LIST of Path Class): All the paths to be expanded
           visited_stations_cost (dict): All visited stations cost
       Returns:
           new_paths (LIST of Path Class): Expanded paths without redundant paths
           list_of_path (LIST of Path Class): list_of_path without redundant paths
           visited_stations_cost (dict): Updated visited stations cost
    """
    lista = [
        i
        for i in expand_paths
        if i.last not in visited_stations_cost or i.g < visited_stations_cost[i.last]
    ]

    for i in lista:
        visited_stations_cost[i.last] = i.g

    list_of_path = [
        i
        for i in list_of_path
        if i.last not in visited_stations_cost or i.g <= visited_stations_cost[i.last]
    ]

    return lista, list_of_path, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
    expand_paths is inserted to the list_of_path according to f VALUE
    Format of the parameter is:
       Args:
           expand_paths (LIST of Path Class): Expanded paths
           list_of_path (LIST of Path Class): The paths to be visited
       Returns:
           list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    path_list = list(expand_paths + list_of_path)
    for i in path_list:
        i.update_f()

    path_list.sort(key=lambda i: [i.f, i.route])
    return path_list


def coord2station(coord, map):
    """
    From coordinates, it searches the closest stations.
    Format of the parameter is:
    Args:
        coord (list):  Two REAL values, which refer to the coordinates of a point in the city.
        map (object of Map class): All the map information
    Returns:
        possible_origins (list): List of the Indexes of stations, which corresponds to the closest station
    """

    min_distance = INF
    closest_station_list = []

    for id, stations in map.stations.items():
        aux_stations = [stations["x"], stations["y"]]
        dist = euclidean_dist(aux_stations, coord)

        if dist < min_distance:
            min_distance = dist
            closest_station_list = [id]

        elif dist == min_distance:
            closest_station_list.append(id)

    return closest_station_list


def Astar(origin_id, destination_id, map, type_preference=0):
    """
    A* Search algorithm
    Format of the parameter is:
       Args:
           origin_id (int): Starting station id
           destination_id (int): Final station id
           map (object of Map class): All the map information
           type_preference: INTEGER Value to indicate the preference selected:
                           0 - Adjacency
                           1 - minimum Time
                           2 - minimum Distance
                           3 - minimum Transfers
       Returns:
           list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    visited = {}

    path_list = [Path(origin_id)]
    while path_list and path_list[0].last != destination_id:
        expand_paths = expand(path_list[0], map)
        expand_paths = remove_cycles(expand_paths)
        expand_paths = calculate_cost(expand_paths, map, type_preference)

        path_list.pop(0)

        expand_paths, path_list, visited = remove_redundant_paths(
            expand_paths, path_list, visited
        )

        expand_paths = calculate_heuristics(
            expand_paths, map, destination_id, type_preference
        )

        path_list = insert_cost_f(expand_paths, path_list)

    if path_list:
        return path_list[0]
    return []
