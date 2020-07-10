import functions
from graph import DisjointSetGraph
from networkx import draw_networkx
import networkx as nx
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

    def setup(self):
        functions.initS(self.S, self.n)
        functions.genC(*self.location_set)
        self.C = functions.get_data()['C']
        # functions.initG(self.S, self.C, self.G)
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

    def runScen2(self):
        # self.G = []
        vertices = len(self.S) + sum([len(i) for i in self.C])
        gObj = DisjointSetGraph(vertices) # Graph Object
        gObj.initVertices()
        for i in range(len(self.S)):
            locations_index = len(self.S)
            prev_loc_index = -1
            for j in range(len(self.C)):
                min_comp_loc = gObj.getSmallestComponent([locations_index + i for i in range(len(self.C[j]))])
                min_comp_loc_index = min_comp_loc + locations_index
                if prev_loc_index > 0:
                    gObj.union(prev_loc_index, min_comp_loc_index)
                prev_loc_index = min_comp_loc_index
                gObj.addEdge(i, min_comp_loc_index)
                locations_index += len(self.C[j])
            gObj.addPersonToShop(i, prev_loc_index)
        # G = gObj.compileToAdjMatrix()
        # g_random2 = nx.read_gml("./data/random2_25_05_04_05.gml")
        stats = functions.gen_stats_nx(gObj.graph)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        self.data['Scenario_2'] = stats

    def getStats(self):
        print(self.data)
        functions.export(self.data)

    #Helper function for backtracking
    def exhaustive(self, size, i, j, l1): 
        if(i == len(self.S) or j == len(self.C)):
            return -1
        high = -1
        for l in range(l1, len(self.C[j])):    
            locations_index = len(self.S) + (sum([len(self.C[i]) for i in range(j)])) + l
            self.exhaustG.addEdge(i, locations_index)
            max_size = -1
            if(j + 1 == len(self.C)):
                max_size = self.exhaustive(self.exhaustG.largestCC(), i + 1, 0, l)
            else:
                max_size = self.exhaustive(self.exhaustG.largestCC(), i, j + 1, l)
            if(max_size < high or high < 0 and max_size > 0):
                high = max_size
            #Backtrack
            self.exhaustG.removeEdge(i, locations_index)
        if(high < 0):
            return size
        return high

    #Backtracking function
    def exhaustive_main(self):
        vertices = len(self.S) + sum([len(i) for i in self.C])
        self.exhaustG = DisjointSetGraph(vertices) # Graph Object
        self.exhaustG.initVertices()
        max_size = -1
        for l in range(len(self.C[0])):
            locations_index = len(self.S) + l
            self.exhaustG.addEdge(0, locations_index)
            size = -1
            if(1 == len(self.C)):
                size = self.exhaustive(self.exhaustG.largestCC(), 1, 0, l)
            else:
                size = self.exhaustive(self.exhaustG.largestCC(), 0, 1, l)
            if(max_size < 0 or max_size > size and size > 0):
                max_size = size
            #Backtrack
            self.exhaustG.removeEdge(0, locations_index)
        return max_size
