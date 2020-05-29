#Jason Huang
import classes
import functions

n = 0 #number of people
S = [] #Set of people 
D = [] #Set of sets of distinct locations that people go to (D = [grocery, gym, coffee,etc.])
## Adjacency Matrix ##
G = [] #|D|-partite graph that contains the set locations, 
## indices ###########################################
# 0 -> |S| - 1 = people, 
# |S| -> |S| + Row-Major Order |locations| - 1 = shops/locations
######################################################

###################################### SCENARIO 1 ###################################################
k = 0 #The kth closest location a person will be at 

