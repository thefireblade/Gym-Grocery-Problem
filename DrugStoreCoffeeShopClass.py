import functions
from graph import DisjointSetGraph
from graph import GymGroceryGraph
from networkx import draw_networkx
import networkx as nx
import time
import matplotlib.pyplot as plt

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
        self.data['Scenario_2_2'] = stats
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
    def runScen0_2_with_plt(self, timer):
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

    # Perform a search on people and compare the 
    def runScen2_3_with_plt(self, timer):
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
