from collections import defaultdict 
import networkx as nx

class DisjointNode():
    def __init__(self, rank, index, components = 1):
        self.parent = self
        self.rank = rank
        self.components = components
        self.index = index

class DisjointSetGraph():
    def __init__(self, vertices):
        self.V = vertices #No. of vertices 
        self.graph = nx.Graph()
        self.nodes = [] # List of DisjointNodes

    def initVertices(self):
        self.graph.add_nodes_from([i for i in range(self.V)])
        self.nodes = [DisjointNode(0, i) for i in range(self.V)] 

    #Adds the vertices u and v to each edge set for the graph
    def addEdge(self,u,v): 
        self.graph.add_edge(u, v)
        self.graph.add_edge(v, u)

    #Get the parent Node of specified node at index i
    def find(self, i):
        if(self.nodes[i].parent == self.nodes[i].parent.parent):
            return self.nodes[i].parent
        parent = self.find(self.nodes[i].parent.index)
        self.nodes[i].parent = parent
        return parent

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
        top_parent.rank += 1
        top_parent.components += bot_parent.components
    
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
    def addPersonToShop(self, p, s):
        parent_s = self.find(s)
        parent_s.components += 1

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