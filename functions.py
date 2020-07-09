import math
import random
import classes
import copy
import json
import numpy as np
from scipy.sparse.csgraph import connected_components
import networkx as nx
###### CONSTANTS ##########
# Long Island Longitude
x_lower = 40.589971
x_upper = 41.139365
# Long Island Lattitude
y_lower = -73.768044
y_upper = -72.225494

dof = 6  # Degrees of freedom

###### Point functions #######


def distP(point1, point2):  # Deprecated
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)


def dist(x1, x2, y1, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

###### Generate random long island coordinates with 6 degrees of precision #######


def gen_rand_XLI():
    return round(random.uniform(x_lower, x_upper), dof)


def gen_rand_YLI():
    return round(random.uniform(y_lower, y_upper), dof)

###### Matching Functions ########
# gets the k closests locations of a person


def get_k_closest(person, locations, k):
    dists = []
    for loc in locations:
        dists.append(dist(person[0], loc[0], person[1], loc[1]))
    # Make copy of distances
    orig_dists = copy.deepcopy(dists)
    dists.sort()
    indices = []
    for i in range(k):
        indices.append(orig_dists.index(dists[i]))
    return indices

# Matches the random k locations closest to person, returns the index of the location
# Sample person = [40.24112, -73.12412]
# Sample locations = [person, person, person]


def match_rand(person, locations, k):
    return get_k_closest(person, locations, k)[random.randrange(0, k)]


####### Data Functions #########
def get_data():
    with open('data.json', 'r') as f:
        return json.load(f)
# Exports a JSON to results.json


def export(data):
    with open('results.json', 'w') as fp:
        json.dump(data, fp,  indent=4, sort_keys=True)

####### Main Functions ##########
# S = set of people coords
# n = # of people to randomly init


def initS(S, n):
    for _ in range(n):
        S.append([gen_rand_XLI(), gen_rand_YLI()])
# S = set of people
# C = Set of set of locations
# G = Adjacency matrix


def initG(S, C, G):
	size = len(S)
	print(size)
	for locations in C:
		size += len(locations)
	for _ in range(size):
		lst = [0 for j in range(size)]
		G.append(lst)
# C = Set of set of locations
# n = set of n where each n = |C[i]| for any i in |C|


def genC(*n):
    data = {}
    try:
        data = get_data()
    except:
	    print("Could not load previous data")
    data['C'] = []
    for i in n:
        locations = []
        for _ in range(i):
            locations.append([gen_rand_XLI(), gen_rand_YLI()])
        data['C'].append(locations)
    with open('data.json', 'w') as fp:
        json.dump(data, fp,  indent=4, sort_keys=True)
# Computes the number of connected components and stats 
# n = number of people
# G = Adjacency matrix
# returns a JSON
def gen_stats(n, G):
    stats = {}
    result = connected_components(np.asarray(G))
    # stats['connected_array'] = result[1]
    stats['connected_components_count'] = result[0]

    con_array = copy.deepcopy(result[1])
    con_array.sort()
    highest = con_array[len(con_array) - 1]
    counting_dict = {i:int((con_array == i).sum()) for i in range(highest + 1)}
    stats['connected_component_sizes'] = counting_dict
    
    infected_groups = {i:0 for i in range(highest + 1)}
    for i in range(n):
        infected_groups[result[1][i]] += 1
    stats['num_people_in_components'] = infected_groups

    return stats
def gen_stats_nx(nxG):
    stats = {}
    con_components = [len(c) for c in sorted(nx.connected_components(nxG), key=len, reverse=True)]
    stats['connected_component_sizes'] = con_components
    stats['connected_components_count'] = len(con_components)
    stats['max_connected_component_size'] = max(con_components)
    return stats
