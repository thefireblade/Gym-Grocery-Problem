'''
Jason Huang @ SBU Algorithms Reading Breakout Group
'''

import networkx as nx
import numpy as np
import random
import math
from graph import GymGroceryGraph
from partitioning_functions import valid_graph

################################## Constants ###################################
activity_definitions = ['store', 'gym', 'school', 'library', 'park', 'hospital']
people_type = "people"
################################################################################

def export_graph(graph, n, activities, filename):
    graph_to_export = nx.Graph()
    # Add all people to the graph
    for person in range(n):
        graph_to_export.add_node(person, type=people_type)
    # Add all locations to the graph
    location_index = n
    for i in range(len(activities)):
        for _ in range(activities[i]):
            graph_to_export.add_node(location_index, type=activity_definitions[i])
            location_index += 1
    graph_to_export.add_edges_from(graph.edges)
    graph_to_export = nx.relabel_nodes(graph_to_export, lambda x: x + 1)
    nx.write_gml(graph_to_export, filename)
        

# Connects all people of indices in a certain range (length 2 tuple) to activities
# of indices in a certain range (length 2 tuple). Each person has a random degree of 
# range activity_per_person (length 2 tuple). Outer part of the range is exclusive. Inner is inclusive.
def interconnect_activity(graph_obj, people_range, activity_range, activity_per_person):
    num_activity = activity_range[1] - activity_range[0]
    # print("people range: {people}".format(people = people_range)) # DEBUG CONNECTIONS
    # print("activity range: {people}".format(people = activity_range)) # DEBUG CONNECTIONS
    for person in range(*people_range):
        choice = random.randrange(*activity_per_person)
        choices = ([1] * choice) + ([0] * (num_activity - choice) )
        random.shuffle(choices)
        for i in range(len(choices)):
            activity = activity_range[0] + i if num_activity > 1 else activity_range[0]
            if choices[i] > 0:
                # print("person : {person}, activity: {act}".format(person = person, act=activity_range[0] + i)) #DEBUG CONNECTIONS
                graph_obj.union(person, activity)
                graph_obj.addEdge(person, activity)

# A function that generates a simple pandemic activity graph with optimal connections. 
# This function will return a dictionary in the format:
# {
#   graph : generated graph,
#   graph_obj: disjoint set custom data structure (GymGroceryGraph),
#   opt   : int of smallest possible connected people size
# }
# The function has the following parameters: 
# people = number of people to be generated from a graph 
# activities = list of numbers representing the occurence of each type of activity created (less the len(activities_definitions)).
# activities_per_person = list of tuples of size 2 representing the range of number of activities each person has per activity.
def generate_simple_graph(people, activities, activities_per_person):
    nodes = people + sum(activities)
    new_graph_obj = GymGroceryGraph(nodes, people)
    new_graph_obj.initVertices()
    opt = -1
    smallest_activity = min(activities)
    community = people // smallest_activity
    max_community_size = smallest_activity
    exception = people % smallest_activity
    people_communities = [community if exception == 0 or exception <= i else community + 1 for i in range(max_community_size)]
    # print(people_communities) # DEBUG CONNECTIONS
    activity_index = people
    for i in range(len(activities)):
        activity_per_person = activities[i] // smallest_activity
        people_index = 0
        current_activity_index = activity_index
        remainder = activities[i] % smallest_activity
        for j in range(len(people_communities)):
            add_1 = remainder == 0 or remainder <= j 
            num_activity = activity_per_person if add_1 else activity_per_person + 1
            interconnect_activity(
                new_graph_obj, 
                (people_index, people_index + people_communities[j]), 
                (current_activity_index, current_activity_index + num_activity), 
                (activities_per_person[i][0], activities_per_person[i][1] + 1)
            )
            current_activity_index += num_activity
            people_index += people_communities[j]
        activity_index += activities[i]
    opt = max(people_communities)
    return {
        "graph": new_graph_obj.graph,
        "opt": opt,
        "graph_obj": new_graph_obj
    }

# Randomly add num_edges edges to a graph if possible. Distributes the number of edges to add per person evenly.
# graph_obj = disjoint set custom graph object
# num_edges = Number of edges to add. Must be less than or equal to number of edges to add.
def add_noise_evenly(graph_obj, num_edges):
    edges_per_person = num_edges // graph_obj.numPeople
    remainder_edges = num_edges % graph_obj.numPeople
    for person in range(graph_obj.numPeople):
        if(edges_per_person == 0 and remainder_edges < person):
            break
        neighbors = [n for n in graph_obj.graph.neighbors(person)]
        # print("person: {person} has neighbors:{neighbors}".format(person = person, neighbors = neighbors)) # DEBUG CONNECTIONS
        activities = [i for i in range(graph_obj.numPeople, graph_obj.V)]
        potential_edges = [i for i in activities if i not in neighbors]
        num_edges_added = edges_per_person if remainder_edges == 0 or remainder_edges <= person else edges_per_person + 1
        # print("Edges added : {num_edges_added} and potential edges: {potential}".format(num_edges_added = num_edges_added, potential = potential_edges)) # DEBUG CONNECTIONS
        activities = np.random.choice(potential_edges, num_edges_added, replace=len(potential_edges) > num_edges_added)
        # print("person: {person} has new activities: {activities}".format(person = person, activities = activities)) # DEBUG CONNECTIONS
        for activity in activities:
            graph_obj.union(person, activity)
            graph_obj.addEdge(person, activity)
        
# A function that generates a pandemic activity graph. This function will return a dictionary in the format:
# {
#   graph : generated graph,
#   graph_obj: disjoint set custom data structure (GymGroceryGraph),
#   opt   : int of smallest possible connected people size
# }
# The function has the following parameters: 
# people = number of people to be generated from a graph 
# activities = list of numbers representing the occurence of each type of activity created (less the len(activities_definitions)).
# activities_per_person = list of tuples of size 2 representing the range of number of activities each person has per activity.
def generate_graph(people, activities, activities_per_person, num_edges):
    result = generate_simple_graph(people, activities, activities_per_person)
    add_noise_evenly(result['graph_obj'], num_edges)
    return result

def main():
    n = 4000
    activities = [200, 200]
    ranges = [(1,1), (1,1)] # Range of values f
    noise = n
    obj = generate_graph(n, activities, ranges, noise)
    print("opt: {opt} score: {score}".format(opt=obj['opt'], score = obj['graph_obj'].largestPeopleGroup)) # DEBUG CONNECTIONS
    print(valid_graph(obj['graph_obj'].graph, n, activities)) # DEBUG CONNECTIONS
    export_graph(obj['graph'], n, activities, 
    './noise_level={noise}_graph_n={n}_k={k}_stores={stores}_gyms={gyms}_opt={opt}.gml'.format(
        noise = noise // n, n=n, stores=activities[0], gyms=activities[1], k=1, opt=obj['opt']
    ))
if __name__ == "__main__":
    main()