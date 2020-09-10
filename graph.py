from collections import defaultdict 
import networkx as nx
import secrets

class DisjointNode():
    def __init__(self, rank, index, components = 0):
        self.parent = self
        self.rank = rank
        self.components = components
        self.index = index
        self.color = secrets.token_hex(3) #Generate a random 6 digit Hex for color

class DisjointSetGraph():
    def __init__(self, vertices):
        self.V = vertices #No. of vertices 
        self.graph = nx.Graph()
        self.nodes = [] # List of DisjointNodes
        self.largestPeopleGroup = 0

    def initVertices(self):
        self.graph.add_nodes_from([i for i in range(self.V)])
        self.nodes = [DisjointNode(0, i) for i in range(self.V)] 

    #Adds the vertices u and v to each edge set for the graph
    def addEdge(self,u,v): 
        self.graph.add_edge(u, v)
        # self.graph.add_edge(v, u)

    def removeEdge(self, u, v): 
        self.graph.remove_edge(u, v)

    #Get the parent Node of specified node at index i
    def find(self, i):
        if(self.nodes[i].parent == self.nodes[i].parent.parent):
            return self.nodes[i].parent
        parent = self.find(self.nodes[i].parent.index)
        self.nodes[i].parent = parent
        return parent

    def largestCC(self):
        return len(max(nx.connected_components(self.graph), key=len))

    #Part of the design, people aren't unioned to the shops but shops are unioned to a shop
    #Get the shop index 's1' and shop index 's2' and perform a union on the nodes 
    def union(self, s1, s2):
        top_parent = self.find(s1)
        bot_parent = self.find(s2)
        if(top_parent == bot_parent):
            return
        if(bot_parent.rank > top_parent.rank):
            temp = bot_parent
            bot_parent = top_parent
            top_parent = temp
        bot_parent.parent = top_parent
        bot_parent.color = top_parent.color
        top_parent.rank += 1
        top_parent.components += bot_parent.components
        if(self.largestPeopleGroup < top_parent.components):
            self.largestPeopleGroup = top_parent.components 
        
    #Get the size of the specified node 'node'
    def getNodeSize(self, node):
        return node.components

    #Get the smallest connected component in graph 
    #given a list of shop indexes 'lst' from |S| (num of people) to self.V
    def getSmallestComponent(self, lst): 
        mapped_parents = list(map(self.find, lst))
        mapped_components = list(map(self.getNodeSize, mapped_parents))
        return mapped_components.index(min(mapped_components))
        
    #Adds a person at index 'p' to shop at index 's'
    #Makes a call to addEdge
    def addPersonToShop(self, p, s): #Currently doesn't use p anymore
        parent_s = self.find(s)
        parent_s.components += 1
    
    def getPeopleInComponents(self):
        countList = []
        trackerList = []
        for i in range(self.V):
            parent = self.find(i)
            if(parent.components == 0):
                continue
            try:
                trackerList.index(parent)
            except:
                trackerList.append(parent)
                countList.append(parent.components)
        return countList

    # deprecated code
    # #For vertices v in set, return the vertex v with the minimum connected component size 
    # def minConComp(self, locations):
    #     if len(locations) == 0:
    #         return 0
    #     mapped_components = list(map(self.getCompSize, locations))
    #     print(mapped_components)
    #     return mapped_components.index(min(mapped_components))

    # #Convert graph to Adjacency matrix
    # def compileToAdjMatrix(self):
    #     adjMatrix = [[0 for j in self.graph] for i in self.graph]
    #     for i in self.graph:
    #         for j in self.graph[i]:
    #             adjMatrix[i][j] = 1
    #     return adjMatrix

# This class 
# -removes the need to addPersonToShop
# -Adds the ability to test a union of two nodes at indexes s1, s2
class GymGroceryGraph(DisjointSetGraph):
    def __init__(self, vertices, numPeople):
        super().__init__(vertices)
        self.numPeople = numPeople

    # Initializes the graph except all people nodes have a component size of 1
    def initVertices(self):
        self.graph.add_nodes_from([i for i in range(self.V)])
        self.nodes = [DisjointNode(0, i, 1) for i in range(self.numPeople)]  #People count as 1 component
        self.nodes.extend([DisjointNode(0, i) for i in range(self.numPeople, self.V)]) # Shops
    
    # Returns the component size after a theoretical union of two nodes at index s1, and s2.
    def testUnion(self, s1, s2):
        top_parent = self.find(s1)
        bot_parent = self.find(s2)
        if(top_parent == bot_parent):
            return top_parent.components
        else:
            return top_parent.components + bot_parent.components

    # Returns the largest component size after a theoretical union of two nodes at index s1, and s2.
    def testUnionLargestComp(self, s1, s2):
        testUnion = self.testUnion(s1, s2)
        testedCC = testUnion if (
            testUnion  > self.largestPeopleGroup
        ) else self.largestPeopleGroup
        return testedCC