
import functions
from graph import DisjointSetGraph
from networkx import draw_networkx
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
from DrugStoreCoffeeShopClass import PlottedStoreShops
import networkx as nx
import matplotlib.pyplot as plt
import csv
import time 

def findMethod(gObj, func):
    try:
        func = getattr(gObj, func)
        func()
    except AttributeError:
        print("{func} not found".format(func = func))
    return -1

if __name__ == "__main__":
    people = 100
    gyms = 20
    stores = 20
    k = 3
    test = 200 # number of test
    # Construct graph
    b = PlottedStoreShops(0, 0, [0, 0])
    #Test graph
    function_names = [b.partition_lgraph_louvain.__name__, b.partition_lgraph_spectral.__name__]
    for b in range(1,6):
        path = "./graph_files/bench{b}/".format(b=b)
        custom_graph = "{path}test_graph_n={people}_k={k}_stores={stores}_gyms={gyms}.gml".format(
            path=path, people=people, gyms=gyms, stores=stores, k=k
        )
        data_path = "{path}location_data_n={people}_k={k}_stores={stores}_gyms={gyms}.json".format(
            path=path, people=people, gyms=gyms, stores=stores, k=k
        )
        # b = PlottedStoreShops(people, k, [gyms, stores])
        # b.setup()
        # b.export(custom_graph, data_path)
        for function_name in function_names:
            timing_results = []
            component_results = []
            headers = ['Max Component Sizes', 'Compute Time (s)', function_name]

            #Writing data
            csv_file = "{path}results_{function}_{people}_k={k}_stores={stores}_gyms={gyms}.csv".format(
                path=path, function = function_name ,people=people, gyms=gyms, stores=stores, k=k
            )

            passed = 0
            for i in range(test):
                print("Computing test {i}".format(i = i))
                c = PlottedStoreShops(0, 0, [0, 0])
                c.import_lgraph(custom_graph, custom_graph)
                start_time = time.perf_counter()
                findMethod(c, function_name)
                c.G_to_disjoint()
                result = c.runScen2_3_1_rand()
                end_time = time.perf_counter() - start_time
                del c
                if(result == -1):
                    continue
                timing_results.append(end_time)
                component_results.append(result)
                print("Finished with size {size}".format(size=result))
                passed += 1
            f = open(csv_file, "w")
            f.close
            with open(csv_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for i in range(passed):
                    writer.writerow([timing_results[i], component_results[i]])
        people *= 2
    # b.partition_lgraph_spectral()
    # b.G_to_disjoint()
    # print(b.runScen2_3_1_rand())

    # c = PlottedStoreShops(4, 4, [5,5])
    # b.setup()
    # b.import_lgraph(custom_graph, custom_graph)
    # print(b.runScen2_3_1_rand())

    # pos = nx.spring_layout(b.G)
    color_map = []
    for node in range(230):
        if node < 200:
            color_map.append('green')
        elif node < 215:
            color_map.append('blue')
        else: 
            color_map.append('red')    

    
    # nx.draw_networkx_nodes(b.gObj.graph, pos, node_color=color_map)
    # nx.draw_networkx_edges(b.gObj.graph, pos, alpha=0.75)
    # c = nx.read_gml(custom_graph)
    # nx.draw(c.gObj.graph, node_color = color_map)
    # plt.show()
    
