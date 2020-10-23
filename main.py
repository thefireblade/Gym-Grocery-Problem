#Gym-Grocery Problem Min-max connected components
#Jason Huang
import classes
import functions
from graph import DisjointSetGraph
from networkx import draw_networkx
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
from DrugStoreCoffeeShopClass import PlottedStoreShops
import networkx as nx
import matplotlib.pyplot as plt

############################################### Constants ###########################################
test_graph = "./data/exports/text.gml"
imported_graph = "./data/expandingCircle/random2_25_05_04_05_bgm.gml"
original_graph = "./data/expandingCircle/random2_25_05_04_05.gml"
export_filepath = './data/exports/random_400people_20gym_20store_5k_2.gml'
n = 40 # number of people
k = 4 # k random closest (For scenario 1)
location_set = [20, 20] #Each item in this set represents the # of randomly generated locations for Coffee Shops, Drugstores, etc


############################################# COMPONENTS ################################################
S = [] #Set of people 
#Set of sets of distinct locations that people go to (C = [grocery, gym, coffee,etc.]) **Contains A and B
C = [] 
## Adjacency Matrix ##
G = nx.Graph() #|C|-partite graph that contains the set locations 
## indices ###########################################
# 0 -> |S| - 1 = people 
# |S| -> |S| + Row-Major Order |locations| - 1 = shops/locations
######################################################
data = {}

############################################# SETUP ###################################################
def setup():
    global n, location_set, S, C, G
    functions.initS(S, n)
    functions.genC(*location_set)
    C = functions.get_data()['C']
    # functions.initG(S, C, G)


###################################### SCENARIO 1 ###################################################
#### Match up each person to a location in locations in C #########
def scen1():
    G = nx.Graph()
    for p in range(len(S)):
        i = 0
        for l in range(len(C)):
            loc_index = len(S) + i + functions.match_rand(S[p], C[l], k)
            # G[p][loc_index] = 1
            # G[loc_index][p] = 1
            G.add_edge(p, loc_index)
            i += len(C[l])
    ######### Get Stats #############
    stats = functions.gen_stats_nx(G) #functions.gen_stats(n, G)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_1'] = stats


##################################### SCENARIO 1.1 ####################################################
def scen1_1():
    G = nx.Graph()
    #functions.initG(S, C, G) # Reset G
    C_sizes = [[0 for _ in locations] for locations in C]
    #### Greedy implementation taking into account the sizes ####
    for p in range(len(S)):
        i, j = 0, 0
        for locations in C:
            lowest = C_sizes[j].index(min(C_sizes[j]))
            loc_index = lowest + i + len(S)
            C_sizes[j][lowest] += 1
            # G[p][loc_index] = 1
            # G[loc_index][p] = 1
            G.add_edge(p, loc_index)
            i += len(locations)
            j += 1
    # stats = functions.gen_stats(n, G)
    stats = functions.gen_stats_nx(G)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_1_1'] = stats

def exhaustive_scen():
    obj = DrugStoreCoffeeShops(n, k, location_set)
    obj.setup()
    solution = obj.exhaustive_main()
    print("Exhaustive best scenario: " + str(solution))




##################################### SCENARIO 2 ####################################################
# #### Greedy implementation that matches the min components 
def scen2():
    # G = []
    # functions.initG(S, C, G) # Reset G
    vertices = len(S) + sum([len(i) for i in C])
    gObj = DisjointSetGraph(vertices) # Graph Object
    gObj.initVertices()
    for i in range(len(S)):
        locations_index = len(S)
        prev_loc_index = -1
        for j in range(len(C)):
            location_indices = [i for i in range(len(C[j]))]
            min_comp_loc_index = functions.getMinimizingIndex(i, location_indices, gObj, locations_index)
            if prev_loc_index > 0:
                gObj.union(prev_loc_index, min_comp_loc_index)
            prev_loc_index = min_comp_loc_index
            gObj.addEdge(i, min_comp_loc_index)
            locations_index += len(C[j])
        gObj.addPersonToShop(i, prev_loc_index)
    # G = gObj.compileToAdjMatrix()
    # g_random2 = nx.read_gml("./data/random2_25_05_04_05.gml")
    stats = functions.gen_stats_nx(gObj.graph)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_2'] = stats
    # draw_networkx(gObj.graph)

##################################### SCENARIO 2.1 ##############################################
### Minimize the component size within the nearest k stores
def scen2_1():
    # G = []
    # functions.initG(S, C, G) # Reset G
    vertices = len(S) + sum([len(i) for i in C])
    gObj = DisjointSetGraph(vertices) # Graph Object
    gObj.initVertices()
    for i in range(len(S)):
        locations_index = len(S)
        prev_loc_index = -1
        for j in range(len(C)):
            k_closest = functions.get_k_closest(S[i], C[j], k)
            min_comp_loc_index = functions.getMinimizingIndex(i, k_closest, gObj, locations_index)
            if prev_loc_index > 0:
                gObj.union(prev_loc_index, min_comp_loc_index)
            gObj.union(i, min_comp_loc_index)
            prev_loc_index = min_comp_loc_index
            gObj.addEdge(i, min_comp_loc_index)
            locations_index += len(C[j])
        gObj.addPersonToShop(i, prev_loc_index)
    stats = functions.gen_stats_nx(gObj.graph)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_2_1'] = stats

##################################### Finalize Stats #############################################
def getStats():
    print(data)
    functions.export(data)

if __name__ == "__main__" :
    # setup()
    # scen1()
    # scen2()
    # scen2_1()
    # exhaustive_scen()
    # getStats()
    # b = PlottedStoreShops(n, k, location_set)
    # b.setup()
    # b.runScen2_3_1()
    # b.animateConcurrent(b.runScen2_3_with_plt, b.runScen2_3_1_with_plt, 0.2)
    # b.resetGraph()
    # b.animate(b.runScen2_3_1_with_plt, 1)
    # b.runScen2()
    # b.runScen2_2()
    # b.getStats()

    #Color Maps
    
    color_map = []
    for node in range(140):
        if node < 100:
            color_map.append('green')
        elif node < 120:
            color_map.append('blue')
        else: 
            color_map.append('red')     

    #Test for Imports
    b = PlottedStoreShops(n, k, location_set)
    b.setup()
    # b.export(export_filepath)
    b.import_lgraph(original_graph, original_graph)
    # b.runScen2_2Random()
    print("the best result is {s}".format(s=b.iterateMe(b.runScen2_2Random.__name__, 3000)))
    # nx.draw(b.gObj.graph, node_color = color_map)
    # plt.show()
    # print('Max Component size result:' + str(b.runScen2_3_1()))
    # b.getStats()
    # nx.draw(b.gObj.graph, node_color = color_map)
    # plt.show()

    # c = PlottedStoreShops(n, k, location_set)
    # c.import_lgraph(original_graph, original_graph)
    # print('Max Component size result:' + str(c.runScen2_3_1()))
    # c.getStats()