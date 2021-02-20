
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
import matplotlib.pyplot as plt
import networkx as nx
import time 

b = DrugStoreCoffeeShops(0, 2, [0, 0])
path = "./graph_files/bench0/test_graph_n=20_k=2_stores=3_gyms=3.gml"

color_map = []
for node in range(140):
    if node < 100:
        color_map.append('green')
    elif node < 120:
        color_map.append('blue')
    else: 
        color_map.append('red')    
b.import_lgraph(path, path)
# b.partition_lgraph_louvain()
# b.G_to_disjoint()
# print(b.runScen3_1_rand())
start = time.perf_counter()
print(b.run_brute_force())
# print(b.get_state())
# print(b.anneal(b.get_state()))
# print("time elapsed {t}(s)".format(t=time.perf_counter() - start))
# nx.draw(b.gObj.graph, node_color = color_map)
# plt.show()