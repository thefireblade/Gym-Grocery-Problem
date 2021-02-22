#This file is mainly to main the functions used in the experiments
# GRAPHS HERE ARE NOT THE SAME AS THE GRAPHS IN THE DRUGSTORECOFEESHOP GRAPH, 
# the networkx graph indices might be different so be sure to properly convert the graphs after using this.
from collections import deque

# Checks if a DrugstoreCoffeeShopGraph output is valid - O(nk) runtime
# graph : networkX graph that contains all of the nodes and edges
# n : Number of people
# d : Number of Drug Stores
def valid_dc_graph(graph, n, d):
    starting_coffee = n + d
    for person in range(n):
        valid_person = False
        neighbors = graph.neighbors(person)
        has_drug_store = False
        has_coffee_shop = False
        for neighbor in neighbors:
            if neighbor >= starting_coffee:
                has_coffee_shop = True
            else: 
                has_drug_store = True
            if has_drug_store and has_coffee_shop:
                valid_person = True
        if not valid_person:
            return False
    return True

# Returns a deque stack of invalid nodes of a DrugStoreCoffeShop graph. Len is empty is valid - O(nk) runtime
# graph : networkX graph that contains all of the nodes and edges
# n : Number of people
# d : Number of Drug Stores
def invalid_nodes_dc_graph(graph, n, d):
    invalid_people = deque()
    starting_coffee = n + d
    for person in range(n):
        valid_person = False
        neighbors = graph.neighbors(person)
        has_drug_store = False
        has_coffee_shop = False
        for neighbor in neighbors:
            if neighbor >= starting_coffee:
                has_coffee_shop = True
            else: 
                has_drug_store = True
            if has_drug_store and has_coffee_shop:
                valid_person = True
        if not valid_person:
            invalid_people.append(person)
    return invalid_people

# Takes in a nx graph and determines whether the graph is valid or not based on our specifications. Works on any number of activities.
# graph = nx graph
# n = number of people
# activities = list of occurences of each activity type. ie. [3, 2] (3 stores and 2 gyms)
def valid_graph(graph, n, activities):
    activity_indices = [(n + sum(activities[0: i]), n + sum(activities[0: i + 1])) for i in range(len(activities))]
    # print(activity_indices) #DEBUG CONNECTIONS
    for person in range(n):
        has_activities = [False for _ in activity_indices]
        neighbors = [n for n in graph.neighbors(person)]
        # print("person: {person} has neighbors: {neighbors}".format(person=person, neighbors = [n for n in neighbors]) ) #DEBUG CONNECTIONS
        for neighbor in neighbors:
            for i in range(len(activity_indices)):
                if(neighbor < activity_indices[i][1] and neighbor >= activity_indices[i][0]):
                    has_activities[i] = True
                    break
        # print(has_activities) #DEBUG CONNECTIONS
        if not all(has_activities):
            return False
    return True

# Take a graph and remove all of the edges to the nodes that are not part of it's partition
# graph : DrugStoreCoffeeShop graph that contains all of the connected nodes
# partition_list : numbers that represent which partition belongs to which group, must be parsed correctly to work
def finish_partition(graph, partition_list):
    for node in graph.nodes:
        node_partition = partition_list[node]
        neighbors = graph.neighbors(node)
        neighbors_to_remove = []
        for neighbor in neighbors:
            if node_partition != partition_list[neighbor]:
                neighbors_to_remove.append(neighbor)
        for neighbor in neighbors_to_remove:
            graph.remove_edge(node, neighbor)
# Repair all broken nodes with it's original connections
def fix_graph(graph, orig_graph, illegal_nodes):
    for illegal_node in illegal_nodes:
        neighbors = orig_graph.neighbors(illegal_node)
        for neighbor in neighbors:
            graph.add_edge(illegal_node, neighbor)


            
         