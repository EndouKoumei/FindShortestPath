import xmltodict
import time
import numpy as np
from sklearn.neighbors import KDTree
from haversine import haversine

s = time.time()
doc = {}
path = r"C:\Users\lnvanhuy\PycharmProjects\FindShortestWay\data\map.graphml"
with open(path , encoding='utf-8') as fd:
    doc = xmltodict.parse(fd.read())
print(time.time() - s)

def getLatLon(OSMId):
    nodes = doc['graphml']['graph']['node']
    for node in nodes:
        if node['@id'] == str(OSMId):
            try:
                lat = float(node['data'][0]['#text'])  # d4 key - latitude
                lon = float(node['data'][1]['#text'])  # d5 key - longitude
                print(f"Found coordinates ({lat}, {lon}) for node {OSMId}")
                return (lat, lon)
            except (KeyError, ValueError, IndexError) as e:
                print(f"Error getting coordinates for node {OSMId}: {e}")
                continue

    print(f"Warning: Could not find coordinates for node {OSMId}")
    return (0, 0)


def getOSMId(lat, lon):
    nodes = doc['graphml']['graph']['node']

    # Helper function to round coordinates for comparison
    def format_coord(val):
        return round(float(val), 7)

    target_lat = format_coord(lat)
    target_lon = format_coord(lon)

    # Find the closest node
    min_distance = float('inf')
    closest_id = None

    for node in nodes:
        try:
            node_lat = float(node['data'][0]['#text'])  # d4 key - latitude
            node_lon = float(node['data'][1]['#text'])  # d5 key - longitude

            # Calculate distance using coordinate difference
            dist = abs(node_lat - target_lat) + abs(node_lon - target_lon)

            if dist < min_distance:
                min_distance = dist
                closest_id = node['@id']

        except (KeyError, ValueError, IndexError) as e:
            continue

    if closest_id:
        print(f"Found closest node {closest_id} for coordinates ({lat}, {lon})")
        return closest_id
    else:
        print(f"Warning: Could not find any suitable node for coordinates ({lat}, {lon})")
        return "0"


def calculateHeuristic(curr, destination):
    return (haversine(curr, destination))


def getNeighbours(OSMId, destinationLetLon):
    neighbourDict = {}
    tempList = []
    edges = doc['graphml']['graph']['edge']

    for edge in edges:
        if edge['@source'] == str(OSMId):
            temp_nbr = {}
            neighbourId = edge['@target']
            neighbourLatLon = getLatLon(neighbourId)

            # Find the length/cost in the edge data
            neighbourCost = None
            for data in edge['data']:
                if data['@key'] == 'd11':  # length key
                    neighbourCost = data['#text']
                    break

            if not neighbourCost:
                print(f"Warning: No cost found for edge from {OSMId} to {neighbourId}")
                continue

            neighborHeuristic = calculateHeuristic(neighbourLatLon, destinationLetLon)

            temp_nbr[neighbourId] = [neighbourLatLon, neighbourCost, neighborHeuristic]
            tempList.append(temp_nbr)

    neighbourDict[OSMId] = tempList
    return neighbourDict


def getNeighbourInfo(neighbourDict):
    neighbourId = None
    neighbourHeuristic = 0
    neighbourCost = 0
    neighbourLatLon = None

    for key, value in neighbourDict.items():
        neighbourId = key
        neighbourLatLon = value[0]
        try:
            neighbourCost = float(value[1]) / 1000  # Convert to kilometers
            neighbourHeuristic = float(value[2])
        except (ValueError, TypeError) as e:
            print(f"Error converting cost or heuristic for node {key}: {e}")
            continue

    if not neighbourId or not neighbourLatLon:
        print("Warning: Invalid neighbour information")
        return "0", 0, 0, (0, 0)

    return neighbourId, neighbourHeuristic, neighbourCost, neighbourLatLon


# Argument should be tuple

def getKNN(pointLocation):
    nodes = doc["graphml"]["graph"]["node"]
    locations = []
    node_ids = []  # Store node IDs alongside locations

    for eachNode in range(len(nodes)):
        locations.append((float(nodes[eachNode]["data"][0]["#text"]), float(nodes[eachNode]["data"][1]["#text"])))
        node_ids.append(nodes[eachNode]["@id"])

    locations_arr = np.asarray(locations, dtype=np.float32)
    point = np.asarray(pointLocation, dtype=np.float32)

    tree = KDTree(locations_arr, leaf_size=2)
    dist, ind = tree.query(point.reshape(1, -1), k=3)

    nearestNeighbourLoc = (float(locations[ind[0][0]][0]), float(locations[ind[0][0]][1]))
    nearest_id = node_ids[ind[0][0]]

    print(f"\nNearest neighbor search for {pointLocation}:")
    print(f"Found nearest node: {nearestNeighbourLoc} (ID: {nearest_id})")
    print(f"Distance: {dist[0][0]} units")

    return nearestNeighbourLoc


def getResponsePathDict(paths, source, destination):
    finalPath = []
    child = destination
    parent = ()
    cost = 0

    print("\nStarting path reconstruction:")
    print(f"Source: {source}")
    print(f"Destination: {destination}")

    # Helper function to round coordinates to 7 decimal places
    def format_coord(coord):
        return tuple(round(x, 7) for x in coord)

    # Convert all path keys to rounded tuples for consistent lookup
    path_dict = {}
    for key in paths:
        # Convert string tuple to actual tuple of floats
        coord = tuple(float(x) for x in key.strip('()').split(','))
        rounded_coord = format_coord(coord)
        path_dict[rounded_coord] = paths[key]
        print(f"Converted path key: {key} -> {rounded_coord}")

    print("\nPath dictionary after conversion:")
    for key in path_dict:
        print(f"Key: {key}, Value: {path_dict[key]}")

    while parent != source:
        tempDict = {}
        rounded_child = format_coord(child)
        print(f"\nLooking for child: {rounded_child}")

        if rounded_child not in path_dict:
            print(f"Warning: Could not find {rounded_child} in path_dict")
            print("Available keys in path_dict:", list(path_dict.keys()))
            break

        cost = cost + float(path_dict[rounded_child]["cost"])
        parent_str = path_dict[rounded_child]["parent"]
        parent = tuple(float(x) for x in parent_str.strip('()').split(','))
        print(f"Found parent: {parent}")

        tempDict["lat"] = parent[0]
        tempDict["lng"] = parent[1]

        finalPath.append(tempDict)
        child = parent

    return finalPath, cost