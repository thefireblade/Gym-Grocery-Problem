#Gym-Grocery Problem Min-max connected components
#Jason Huang
import classes
import functions
from graph import Graph

############################################### VARIABLES ###########################################
n = 10 #number of people
k = 3 # k random closest (For scenario 1)
location_set = [10, 10] #Each item in this set represents the # of randomly generated locations for Coffee Shops, Drugstores, etc


############################################# COMPONENTS ################################################
S = [] #Set of people 
#Set of sets of distinct locations that people go to (C = [grocery, gym, coffee,etc.]) **Contains A and B
C = [] 
## Adjacency Matrix ##
G = [] #|C|-partite graph that contains the set locations 
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
    functions.initG(S, C, G)


###################################### SCENARIO 1 ###################################################
#### Match up each person to a location in locations in C #########
def scen1():
    for p in range(len(S)):
        i = 0
        for l in range(len(C)):
            loc_index = len(S) + i + functions.match_rand(S[p], C[l], k)
            G[p][loc_index] = 1
            G[loc_index][p] = 1
            i += len(C[l])
    ######### Get Stats #############
    stats = functions.gen_stats(n, G)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_1'] = stats


##################################### SCENARIO 1.1 ####################################################
def scen1_1():
    G = []
    functions.initG(S, C, G) # Reset G
    C_sizes = [[0 for _ in locations] for locations in C]
    #### Greedy implementation taking into account the sizes ####
    for p in range(len(S)):
        i, j = 0, 0
        for locations in C:
            lowest = C_sizes[j].index(min(C_sizes[j]))
            loc_index = lowest + i + len(S)
            C_sizes[j][lowest] += 1
            G[p][loc_index] = 1
            G[loc_index][p] = 1

            i += len(locations)
            j += 1
    stats = functions.gen_stats(n, G)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_1_1'] = stats




##################################### SCENARIO 2 ####################################################
# #### Greedy implementation that matches the min components 
def scen2():
    G = []
    functions.initG(S, C, G) # Reset G
    vertices = len(S) + sum([len(i) for i in C])
    gObj = Graph(vertices) # Graph Object
    gObj.initVertices()
    for i in range(len(S)):
        locations_index = len(S)
        for j in range(len(C)):
            min_comp_loc = gObj.minConComp([locations_index + i for i in range(len(C[j]))])
            min_comp_loc_index = min_comp_loc + locations_index
            gObj.addEdge(i, min_comp_loc_index)
            locations_index += len(C[j])
    G = gObj.compileToAdjMatrix()
    stats = functions.gen_stats(n, G)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_2'] = stats


##################################### SCENARIO 2.1 ##############################################
### Minimize the component size within the nearest k stores
def scen2_1():
    G = []
    functions.initG(S, C, G) # Reset G
    vertices = len(S) + sum([len(i) for i in C])
    gObj = Graph(vertices) # Graph Object
    gObj.initVertices()
    for i in range(len(S)):
        locations_index = len(S)
        for j in range(len(C)):
            k_closest = functions.get_k_closest(S[i], C[j], k)
            min_comp_loc = k_closest[gObj.minConComp([locations_index + k_closest[i] for i in range(len(k_closest))])]
            min_comp_loc_index = min_comp_loc + locations_index
            gObj.addEdge(i, min_comp_loc_index)
            locations_index += len(C[j])
    G = gObj.compileToAdjMatrix()
    stats = functions.gen_stats(n, G)
    stats['num_ppl'] = n
    stats['num_coffeeshops'] = len(C[0])
    stats['num_drugstores'] = len(C[1])
    data['Scenario_2_1'] = stats
    
##################################### Finalize Stats #############################################
def getStats():
    print(data)
    functions.export(data)

if __name__ == "__main__" :
    setup()
    scen1()
    scen2()
    scen2_1()
    getStats()

