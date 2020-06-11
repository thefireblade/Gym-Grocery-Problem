from collections import defaultdict 
class Graph():
    def __init__(self, vertices):
        self.V= vertices #No. of vertices 
        self.graph = defaultdict(list) # default dictionary to store graph 

    def initVertices(self):
        for i in range(self.V):
            self.graph[i] = []

    #Adds the vertices u and v to each edge set for the graph
    def addEdge(self,u,v): 
        self.graph[u].append(v) 
        self.graph[v].append(u)

    #Get the connected component size of the vertex v
    def getCompSize(self, v):
        return len(self.graph[v])

    #For vertices v in set, return the vertex v with the minimum connected component size 
    def minConComp(self, locations):
        if len(locations) == 0:
            return 0
        mapped_components = list(map(self.getCompSize, locations))
        print(mapped_components.index(min(mapped_components)))
        return mapped_components.index(min(mapped_components))

    #Convert graph to Adjacency matrix
    def compileToAdjMatrix(self):
        adjMatrix = [[0 for j in self.graph] for i in self.graph]
        for i in self.graph:
            for j in self.graph[i]:
                adjMatrix[i][j] = 1
        return adjMatrix