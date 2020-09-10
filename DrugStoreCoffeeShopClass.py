import functions
from graph import DisjointSetGraph
from graph import GymGroceryGraph
from networkx import draw_networkx
import networkx as nx
import time
import matplotlib.pyplot as plt
from collections import deque

class DrugStoreCoffeeShops():
    # Don't set 'S', 'C', 'G', 'data'
    def __init__(self, n = 20, k = 5, location_set = [5, 5]):
        self.n = n # Number of people
        self.k = k # Within a certain k number of shops
        self.location_set = location_set # The locations that we are working with
        self.S = [] # The set of people (To be initialized later)
        self.C = []  # The set of distinct locations. Set of sets of distinct locations that people go to (C = [grocery, gym, coffee,etc.]) **Contains A and B
        self.G = nx.Graph() # The graph that holds the connections
        self.data = {}
        self.gObj = DisjointSetGraph(0)

    def setup(self):
        functions.initS(self.S, self.n)
        functions.genC(*self.location_set)
        self.C = functions.get_data()['C']
        # functions.initG(self.S, self.C, self.G)
        self.G = nx.Graph()

    def resetGraph(self):
        self.G = nx.Graph()

    def runScen1(self):
        for p in range(len(self.S)):
            i = 0
            for l in range(len(self.C)):
                loc_index = len(self.S) + i + functions.match_rand(self.S[p], self.C[l], self.k)
                self.G.add_edge(p, loc_index)
                i += len(self.C[l])
        ######### Get Stats #############
        # stats = functions.gen_stats(self.n, self.G)
        stats = functions.gen_stats_nx(self.G)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        self.data['Scenario_1'] = stats
        return stats['max_connected_component_size']

    def runScen2(self):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object
        self.gObj.initVertices()
        for i in range(len(self.S)):
            locations_index = len(self.S)
            for j in range(len(self.C)):        
                k_closest = functions.get_k_closest(self.S[i], self.C[j], self.k)
                min_comp_loc_index = functions.getMinimizingIndex2(i, k_closest, self.gObj, locations_index)
                self.gObj.union(i, min_comp_loc_index)
                self.gObj.addEdge(i, min_comp_loc_index)
                locations_index += len(self.C[j])
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['max_connected_component_size'] = self.gObj.largestPeopleGroup
        self.data['Scenario_2'] = stats
        return stats['max_connected_component_size']

    def runScen2_2(self):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object
        self.gObj.initVertices()
        for j in range(len(self.C)):     
            locations_index = len(self.S) + (sum([len(self.C[k]) for k in range(j)]))   
            for i in range(len(self.S)): 
                k_closest = functions.get_k_closest(self.S[i], self.C[j], self.k)
                min_comp_loc_index = functions.getMinimizingIndex2(i, k_closest, self.gObj, locations_index)
                self.gObj.union(i, min_comp_loc_index)
                self.gObj.addEdge(i, min_comp_loc_index)
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['max_connected_component_size'] = self.gObj.largestPeopleGroup
        self.data['Scenario_2_2'] = stats
        return stats['max_connected_component_size']

    # Contraints : There must be at least one shop of any type
    # Perform a search on people and compare the 
    def runScen2_3(self):
        # Graph Object initialization
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object 
        self.gObj.initVertices()

        tracker_map = {}
        k_closest_map = {}
        tracker_keys = []
        # 2-D List construction
        for i in range(len(self.C)):
            shop_list = []
            for person in range(len(self.S)):
                shop_list.append(person)
            tracker_map[i] = shop_list
            tracker_keys.append(i)

        # Table every starting index of every key
        key_index_map = {}
        for key in tracker_keys:
            key_index_map[key] = sum([len(self.C[i]) for i in range(key)])

        while(tracker_map): #Check if the map is not empty
            best_pick_person = -1 #Get the first index existing in the list
            best_pick_shop = -1 #Assume there is atleast one shop to connect the person to
            best_key = tracker_keys[0]
            # Track the largest number of people in a connected component
            largestCC = len(self.S) #Worst case scenario

            for key in tracker_keys:
                for person in tracker_map[key]:
                    # Check every location for that person
                    locations_index = len(self.S) + key_index_map[key]  
                    
                    k_closest = []
                    # Tabulate the k_closest (Initially runs in O(n) time)
                    if f"{person}_{key}" not in k_closest_map.keys():
                        k_closest_map[f"{person}_{key}"] = functions.get_k_closest(self.S[person], self.C[key], self.k)
                    k_closest = k_closest_map[f"{person}_{key}"]

                    # print(locations_index)
                    # Get the optimum connection for this person and list of k_closest (Runs O(k) time)
                    min_comp_loc_index = functions.getMinimizingIndex2(person, k_closest, self.gObj, locations_index)
                    
                    # Everything here runs in O(1) time
                    # Get the largest number of people connected in tested component
                    testedCC = self.gObj.testUnion(person, min_comp_loc_index) if (
                        self.gObj.testUnion(person, min_comp_loc_index)  > self.gObj.largestPeopleGroup
                    ) else self.gObj.largestPeopleGroup
                    # Debug prints
                    # print("Person : " + str(person) + " and location " + str(key))
                    # print("testCC = " + str(testedCC))
                    # print("largestCC = " + str(largestCC))
                    if(largestCC == len(self.S) or testedCC < largestCC or best_pick_person == -1):
                        # print("The best person is now " + str(person) + " with location " + str(min_comp_loc_index))
                        largestCC = testedCC
                        best_pick_person = person
                        best_pick_shop = min_comp_loc_index 
                        best_key = key

            self.gObj.union(best_pick_person, best_pick_shop)
            self.gObj.addEdge(best_pick_person, best_pick_shop)
            tracker_map[best_key].remove(best_pick_person)
            # print("The largestCC is now : " + str(self.gObj.largestPeopleGroup))
            if(len(tracker_map[best_key]) == 0):
                # print("The key " + str(best_key) + " is now empty!")
                del tracker_map[best_key] # Delete the shoplist within the key index
                tracker_keys.remove(best_key)
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['people_in_connected_components'] = self.gObj.getPeopleInComponents()
        stats['max_connected_component_size'] = self.gObj.largestPeopleGroup
        self.data['Scenario_2_3'] = stats
        return stats['max_connected_component_size']


    def getStats(self):
        print(self.data)
        functions.export(self.data)

    #Helper function for backtracking
    def exhaustive(self, size, i, j, l1): 
        if(i == len(self.S)):
            # print("###############       The size (-1) is now " + str(size) + "     ##############")
            return size
        if(j == len(self.C)):
            return -1
        high = -1
        for l in range(l1, len(self.C[j])):    
            locations_index = len(self.S) + (sum([len(self.C[i]) for i in range(j)])) + l
            # print("Adding edge between " + str(i) + " and " + str(locations_index))
            self.exhaustG.addEdge(i, locations_index)
            max_size = -1
            if(j + 1 == len(self.C)):
                max_size = self.exhaustive(self.exhaustG.largestCC(), i + 1, 0, l)
            else:
                max_size = self.exhaustive(self.exhaustG.largestCC(), i, j + 1, l)
            if((max_size < high or high < 0) and max_size > 0):
                high = max_size
            #Backtrack
            self.exhaustG.removeEdge(i, locations_index)
            # print("Removing edge between " + str(i) + " and " + str(locations_index))
        # print("###############       The high is now " + str(high) + "     ##############")    
        return high

    #Backtracking function
    def exhaustive_main(self):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.exhaustG = DisjointSetGraph(vertices) # Graph Object
        self.exhaustG.initVertices()
        max_size = -1
        i,j = 0,0
        for l in range(len(self.C[0])):
            locations_index = len(self.S) + l
            self.exhaustG.addEdge(i, locations_index)
            # print("Adding edge between " + str(i) + " and " + str(locations_index))
            size = -1
            if(1 == len(self.C)):
                size = self.exhaustive(self.exhaustG.largestCC(), i + 1, 0, l)
            else:
                size = self.exhaustive(self.exhaustG.largestCC(), i, j + 1, l)
            if(max_size < 0 or max_size > size and size > 0):
                max_size = size
            #Backtrack
            self.exhaustG.removeEdge(0, locations_index)
            # print("Removing edge between " + str(i) + " and " + str(locations_index))
        return max_size

class PlottedStoreShops(DrugStoreCoffeeShops):
    def __init__(self, n = 20, k = 5, location_set = [5, 5]):
        super().__init__(n, k, location_set)
        self.colors = []
        # ax = plt.subplots()
        # ax.set_xlim(40.589971, 41.139365)
        # for person in self.S:
        #     plt.plot()
    def animate(self, function, timer = 0.1):
        plt.xlim(40.589971, 41.139365)
        plt.ylim(-73.768044, -72.225494)
        plt.title("Drug Stores, Coffee Shops, and People")
        plt.ylabel("Longitude")
        plt.xlabel("Latitude")
        plt.plot(self.S[0][0], self.S[0][1], color='green', marker='o',
            label="Person")
        # Plot all of the people onto the graph
        for person in self.S:
            plt.plot(person[0], person[1], color='green', marker='o')

        
        plt.plot(self.C[0][0][0], self.C[0][0][1], color='blue', marker='o',
            label="Drug Store")
        # Plot all of the drug stores
        for loc_1 in self.C[0]:
            plt.plot(loc_1[0], loc_1[1], color='blue', marker='o')

        
        plt.plot(self.C[1][0][0], self.C[1][0][1], color='red', marker='o',
            label="Coffee Shop")
        # Plot all of the coffee shops
        for loc_1 in self.C[1]:
            plt.plot(loc_1[0], loc_1[1], color='red', marker='o')
        
        plt.legend(loc="upper left")
        function(timer)
        self.getStats()
        plt.show()

    def animateConcurrent(self, function, function2, timer = 0.1):
        plt.figure(1)
        plt.xlim(40.589971, 41.139365)
        plt.ylim(-73.768044, -72.225494)
        plt.title("Function 1")
        plt.ylabel("Longitude")
        plt.xlabel("Latitude")
        plt.plot(self.S[0][0], self.S[0][1], color='green', marker='o',
            label="Person")
        # Plot all of the people onto the graph
        for person in self.S:
            plt.plot(person[0], person[1], color='green', marker='o')

        
        plt.plot(self.C[0][0][0], self.C[0][0][1], color='blue', marker='o',
            label="Drug Store")
        # Plot all of the drug stores
        for loc_1 in self.C[0]:
            plt.plot(loc_1[0], loc_1[1], color='blue', marker='o')

        
        plt.plot(self.C[1][0][0], self.C[1][0][1], color='red', marker='o',
            label="Coffee Shop")
        # Plot all of the coffee shops
        for loc_1 in self.C[1]:
            plt.plot(loc_1[0], loc_1[1], color='red', marker='o')
        
        plt.legend(loc="upper left")
        function(timer)
        self.getStats()

        plt.figure(2)
        plt.xlim(40.589971, 41.139365)
        plt.ylim(-73.768044, -72.225494)
        plt.title("Function 2")
        plt.ylabel("Longitude")
        plt.xlabel("Latitude")
        plt.plot(self.S[0][0], self.S[0][1], color='green', marker='o',
            label="Person")
        # Plot all of the people onto the graph
        for person in self.S:
            plt.plot(person[0], person[1], color='green', marker='o')

        
        plt.plot(self.C[0][0][0], self.C[0][0][1], color='blue', marker='o',
            label="Drug Store")
        # Plot all of the drug stores
        for loc_1 in self.C[0]:
            plt.plot(loc_1[0], loc_1[1], color='blue', marker='o')

        
        plt.plot(self.C[1][0][0], self.C[1][0][1], color='red', marker='o',
            label="Coffee Shop")
        # Plot all of the coffee shops
        for loc_1 in self.C[1]:
            plt.plot(loc_1[0], loc_1[1], color='red', marker='o')
        
        plt.legend(loc="upper left")
        function2(timer)
        self.getStats()
        plt.show()

    def connectPLTNodes(self, point_1, point_2, clr="black"):
        x_values = [point_1[0], point_2[0]]
        y_values = [point_1[1], point_2[1]]
        plt.plot(x_values, y_values, color=clr)

    def updateComponentGraph(self):
        for i in range(len(self.S)):
            for j in range(len(self.C)):
                for k in range(len(self.C[j])):
                    shop_index = len(self.S) + (sum([len(self.C[l]) for l in range(j)])) + k
                    if(self.gObj.graph.has_edge(i, shop_index)):
                        self.connectPLTNodes(self.S[i], self.C[j][k], '#' + str(self.gObj.find(i).color))
                
    #Go through every person and pair up a store and a coffee shop that works
    def runScen2_with_plt(self, timer = 0.1):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object
        self.gObj.initVertices()
        for i in range(len(self.S)):
            locations_index = len(self.S)
            for j in range(len(self.C)):        
                k_closest = functions.get_k_closest(self.S[i], self.C[j], self.k)
                min_comp_loc_index = functions.getMinimizingIndex2(i, k_closest, self.gObj, locations_index)
                self.gObj.union(i, min_comp_loc_index)
                self.gObj.addEdge(i, min_comp_loc_index)
                self.connectPLTNodes(self.S[i], self.C[j][min_comp_loc_index - locations_index])
                locations_index += len(self.C[j])
            plt.pause(timer)    
        self.updateComponentGraph()
        plt.pause(timer)
        # G = gObj.compileToAdjMatrix()
        # g_random2 = nx.read_gml("./data/random2_25_05_04_05.gml")
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['people_in_connected_components'] = self.gObj.getPeopleInComponents()
        self.data['Scenario_2'] = stats
    
    #The most ideal scenario for scen 2
    def runScen2Ideal_with_plt(self, timer = 1):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = DisjointSetGraph(vertices) # Graph Object
        self.gObj.initVertices()
        for i in range(len(self.S)):
            locations_index = len(self.S)
            prev_loc_index = -1
            for j in range(len(self.C)):        
                location_indices = [i for i in range(len(self.C[j]))]
                min_comp_loc_index = functions.getMinimizingIndex(i, location_indices, self.gObj, locations_index)
                if prev_loc_index > 0:
                    self.gObj.union(prev_loc_index, min_comp_loc_index)
                self.gObj.union(i, min_comp_loc_index)
                prev_loc_index = min_comp_loc_index
                self.gObj.addEdge(i, min_comp_loc_index)
                self.connectPLTNodes(self.S[i], self.C[j][min_comp_loc_index - locations_index])
                locations_index += len(self.C[j])
            plt.pause(timer)
            self.gObj.addPersonToShop(i, prev_loc_index)
        self.updateComponentGraph()
        plt.pause(timer)
        # G = gObj.compileToAdjMatrix()
        # g_random2 = nx.read_gml("./data/random2_25_05_04_05.gml")
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        self.data['Scenario_2Ideal'] = stats

    #Pair up each of the people separately with shops
    def runScen2_2_with_plt(self, timer = 0.1):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object
        self.gObj.initVertices()
        for j in range(len(self.C)):     
            locations_index = len(self.S) + (sum([len(self.C[k]) for k in range(j)]))   
            for i in range(len(self.S)): 
                k_closest = functions.get_k_closest(self.S[i], self.C[j], self.k)
                min_comp_loc_index = functions.getMinimizingIndex2(i, k_closest, self.gObj, locations_index)
                self.gObj.union(i, min_comp_loc_index)
                self.gObj.addEdge(i, min_comp_loc_index)
                self.connectPLTNodes(self.S[i], self.C[j][min_comp_loc_index - locations_index])
                plt.pause(timer)
        self.updateComponentGraph()
        plt.pause(timer)
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['people_in_connected_components'] = self.gObj.getPeopleInComponents()
        self.data['Scenario_2_2'] = stats
        
    #Maximize the connected component
    def runScen0_2_with_plt(self, timer = 0.1):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = DisjointSetGraph(vertices) # Graph Object
        self.gObj.initVertices()
        for j in range(len(self.C)):     
            locations_index = len(self.S) + (sum([len(self.C[k]) for k in range(j)]))   
            prev_loc_index = -1
            for i in range(len(self.S)): 
                k_closest = functions.get_k_closest(self.S[i], self.C[j], self.k)
                min_comp_loc_index = functions.getMaximizingIndex(i, k_closest, self.gObj, locations_index)
                if prev_loc_index > 0:
                    self.gObj.union(prev_loc_index, min_comp_loc_index)
                prev_loc_index = min_comp_loc_index
                self.gObj.addEdge(i, min_comp_loc_index)
                self.connectPLTNodes(self.S[i], self.C[j][min_comp_loc_index - locations_index])
                plt.pause(timer)
        self.updateComponentGraph()
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        self.data['Scenario_0_2'] = stats

    # Contraints : There must be at least one shop of any type
    # Perform a search on people and compare the 
    def runScen2_3_with_plt(self, timer):
        # Graph Object initialization
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object 
        self.gObj.initVertices()

        tracker_map = {}
        k_closest_map = {}
        tracker_keys = []
        # 2-D List construction
        for i in range(len(self.C)):
            shop_list = []
            for person in range(len(self.S)):
                shop_list.append(person)
            tracker_map[i] = shop_list
            tracker_keys.append(i)

        # Table every starting index of every key
        key_index_map = {}
        for key in tracker_keys:
            key_index_map[key] = sum([len(self.C[i]) for i in range(key)])

        while(tracker_map): #Check if the map is not empty
            best_pick_person = -1 #Get the first index existing in the list
            best_pick_shop = -1 #Assume there is atleast one shop to connect the person to
            best_loc_index = -1
            best_key = tracker_keys[0]
            # Track the largest number of people in a connected component
            largestCC = len(self.S) #Worst case scenario

            for key in tracker_keys:
                for person in tracker_map[key]:
                    # Check every location for that person
                    locations_index = len(self.S) + key_index_map[key]  
                    
                    k_closest = []
                    # Tabulate the k_closest (Initially runs in O(n) time)
                    if f"{person}_{key}" not in k_closest_map.keys():
                        k_closest_map[f"{person}_{key}"] = functions.get_k_closest(self.S[person], self.C[key], self.k)
                    k_closest = k_closest_map[f"{person}_{key}"]

                    # print(locations_index)
                    # Get the optimum connection for this person and list of k_closest (Runs O(k) time)
                    min_comp_loc_index = functions.getMinimizingIndex2(person, k_closest, self.gObj, locations_index)
                    
                    # Everything here runs in O(1) time
                    # Get the largest number of people connected in tested component
                    testedCC = self.gObj.testUnion(person, min_comp_loc_index) if (
                        self.gObj.testUnion(person, min_comp_loc_index)  > self.gObj.largestPeopleGroup
                    ) else self.gObj.largestPeopleGroup
                    # Debug prints
                    # print("Person : " + str(person) + " and location " + str(key))
                    # print("testCC = " + str(testedCC))
                    # print("largestCC = " + str(largestCC))
                    if(largestCC == len(self.S) or testedCC < largestCC or best_pick_person == -1):
                        # print("The best person is now " + str(person) + " with location " + str(min_comp_loc_index))
                        largestCC = testedCC
                        best_pick_person = person
                        best_pick_shop = min_comp_loc_index 
                        best_loc_index = locations_index
                        best_key = key

            self.gObj.union(best_pick_person, best_pick_shop)
            self.gObj.addEdge(best_pick_person, best_pick_shop)
            self.connectPLTNodes(self.S[best_pick_person], self.C[best_key][best_pick_shop - best_loc_index])
            plt.pause(timer)
            tracker_map[best_key].remove(best_pick_person)
            # print("The largestCC is now : " + str(self.gObj.largestPeopleGroup))
            if(len(tracker_map[best_key]) == 0):
                # print("The key " + str(best_key) + " is now empty!")
                del tracker_map[best_key] # Delete the shoplist within the key index
                tracker_keys.remove(best_key)
        self.updateComponentGraph()
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['people_in_connected_components'] = self.gObj.getPeopleInComponents()
        self.data['Scenario_2_3'] = stats

    def runScen2_3_1_with_plt(self, timer):
        # Graph Object initialization
        vertices = len(self.S) + sum([len(i) for i in self.C])
        # The list cannot be empty
        if(vertices < 0) :
            print("The num of vertices must be >= 0")
            return
        # Initialize the graph object
        self.gObj = GymGroceryGraph(vertices, len(self.S)) # Graph Object 
        self.gObj.initVertices()
        #init the first row for the list_queue, runs in O(n*k*|m|)
        list_queue = [deque() for i in range(vertices)]
        for person in range(len(self.S)):
            locations_index = len(self.S)
            for locations in range(len(self.C)):
                k_closest = functions.get_k_closest(self.S[person], self.C[locations], self.k)
                mapped_shoplist = [k_closest[i] + locations_index for i in range(len(k_closest))]
                person_map = {
                    'shoplist': mapped_shoplist,
                    'person': person,
                    'location_index': locations_index,
                    'shop_type': locations
                }
                # Add the valid list of shops - person combos to the first stack
                list_queue[0].append(person_map)
                locations_index += len(self.C[locations])

        for i in range(len(list_queue)):
            goal = i + 1
            stack = list_queue[i]
            # Runs until the stack is empty
            while(stack):
                person_map = stack.pop()
                # Checking the shop in the person map
                person = person_map['person']
                shoplist = person_map['shoplist']
                goal_found = False
                goal_index = 0
                # Check the returned component sizes (in our case, people) to see if it matches the current goal O(k)
                shoplist_component_sizes = []
                for shop in shoplist:
                    size = self.gObj.testUnionLargestComp(person, shop)
                    # check if the resulting component size is equal to the goal
                    if(size == goal):
                        goal_found = True
                        break
                    shoplist_component_sizes.append(size)
                    goal_index += 1
                # Evaluate the goal and check if we found it or not.
                if(goal_found):
                    # Make the connection immediately with the person and shop
                    location_index = person_map['location_index']
                    shop_type = person_map['shop_type']
                    self.gObj.union(person, shoplist[goal_index])
                    self.gObj.addEdge(person, shoplist[goal_index])
                    self.connectPLTNodes(self.S[person], self.C[shop_type][shoplist[goal_index] - location_index])
                    plt.pause(timer)
                else:
                    # Goal failed, re-evaluate the component sizes and move the map to a different index
                    min_size = min(shoplist_component_sizes) - 1 # -1 since the goal is always index + 1
                    list_queue[min_size].append(person_map)
        self.updateComponentGraph()
        stats = functions.gen_stats_nx(self.gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        stats['people_in_connected_components'] = self.gObj.getPeopleInComponents()
        self.data['Scenario_2_3_1'] = stats
