#Gym-Grocery Problem Min-max connected components
#Jason Huang
import classes
import functions

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
functions.initS(S, n)
functions.genC(*location_set)
C = functions.get_data()['C']
functions.initG(S, C, G)


###################################### SCENARIO 1 ###################################################
#### Match up each person to a location in locations in C #########
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


##################################### SCENARIO 2 ####################################################
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
data['Scenario_2'] = stats

##################################### Finalize Stats #############################################
print(data)
functions.export(data)