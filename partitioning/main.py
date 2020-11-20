
import functions
from graph import DisjointSetGraph
from networkx import draw_networkx
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
from DrugStoreCoffeeShopClass import PlottedStoreShops
import networkx as nx
import matplotlib.pyplot as plt


if __name__ == "__main__":
    custom_graph = "../data/exports/random_50people_10gym_15store_3k.gml"
    b = PlottedStoreShops(4, 4, [5,5])
    b.setup()
    b.import_lgraph(custom_graph, custom_graph)
    
    b.partition_lgraph_spectral()
    b.G_to_disjoint()
    print(b.runScen2_3_1_rand())

    # c = PlottedStoreShops(4, 4, [5,5])
    # b.setup()
    # b.import_lgraph(custom_graph, custom_graph)
    # print(b.runScen2_3_1_rand())

    # pos = nx.spring_layout(b.G)
    # color_map = []
    # for node in range(75):
    #     if node < 50:
    #         color_map.append('green')
    #     elif node < 60:
    #         color_map.append('blue')
    #     else: 
    #         color_map.append('red')    
    # nx.draw_networkx_nodes(b.gObj.graph, pos, node_color=color_map)
    # nx.draw_networkx_edges(b.gObj.graph, pos, alpha=0.75)
    # plt.show()
    
