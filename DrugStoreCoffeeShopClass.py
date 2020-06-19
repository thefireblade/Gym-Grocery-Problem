import functions
from graph import DisjointSetGraph
class DrugStoreCoffeeShops():
    # Don't set 'S', 'C', 'G', 'data'
    def __init__(self, n = 20, k = 5, location_set = [5, 5]):
        self.n = n
        self.k = k
        self.location_set = location_set
        self.S = []
        self.C = []
        self.G = []
        self.data = {}

    def setup(self):
        functions.initS(self.S, self.n)
        functions.genC(*self.location_set)
        self.C = functions.get_data()['C']
        functions.initG(self.S, self.C, self.G)

    def runScen1(self):
        for p in range(len(self.S)):
            i = 0
            for l in range(len(self.C)):
                loc_index = len(self.S) + i + functions.match_rand(self.S[p], self.C[l], self.k)
                self.G[p][loc_index] = 1
                self.G[loc_index][p] = 1
                i += len(self.C[l])
        ######### Get Stats #############
        stats = functions.gen_stats(self.n, self.G)
        stats['num_ppl'] = self.n
        stats['num_coffeeshops'] = len(self.C[0])
        stats['num_drugstores'] = len(self.C[1])
        self.data['Scenario_1'] = stats

    def runScen2(self):
        self.G = []
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