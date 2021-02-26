
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
import matplotlib.pyplot as plt
import networkx as nx
import time 
from partitioning_functions import valid_graph

b = DrugStoreCoffeeShops(0, 2, [0, 0])
path = "./noise_level=1_graph_n=25_k=1_stores=5_gyms=5_opt=5.gml"

color_map = []
for node in range(35):
    if node < 25:
        color_map.append('green')
    elif node < 30:
        color_map.append('blue')
    else: 
        color_map.append('red')    
# b.import_lgraph(path, path)
graph = nx.read_gml(path)
# b.partition_lgraph_louvain()
# b.G_to_disjoint()
# print(b.runScen3_1_rand())
start = time.perf_counter()
# b.partition_lgraph_louvain()
# b.G_to_disjoint()
# print(b.runScen3_1_rand())
# print(b.get_state())
# print(b.anneal(b.get_state()))
print("time elapsed {t}(s)".format(t=time.perf_counter() - start))
# print(valid_graph(graph, 25, [5, 5]))
nx.draw(b.gObj.graph, node_color = color_map)
plt.show()