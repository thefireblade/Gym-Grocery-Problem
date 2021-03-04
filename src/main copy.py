
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
        return func()
    except AttributeError:
        print("{func} not found".format(func = func))
    return -1

if __name__ == "__main__":
    b = PlottedStoreShops(0, 0, [0, 0])
    function_names = [b.runScen2_2Random.__name__, b.runScen3_1_rand.__name__]
    files = [
        # "./graph_files/bench0_1/harder_graph_n=25_k=2_stores=5_gyms=5_opt=5.gml",
        # "./graph_files/bench0_1/harder_graph_n=30_k=2_stores=5_gyms=5_opt=6.gml",
        # "./graph_files/bench0_1/harder_graph_n=35_k=2_stores=6_gyms=6_opt=6.gml",
        # "./graph_files/bench0_1/harder_graph_n=40_k=2_stores=7_gyms=7_opt=6.gml",
        # "./graph_files/bench0_1/harder_graph_n=50_k=2_stores=8_gyms=8_opt=7.gml",
        # "./graph_files/bench0_1/harder_graph_n=100_k=2_stores=10_gyms=10_opt=10.gml",
        # "./graph_files/bench0_1/harder_graph_n=200_k=2_stores=20_gyms=20_opt=10.gml",
        # "./graph_files/bench0_1/harder_graph_n=400_k=2_stores=20_gyms=20_opt=20.gml",
        # "./graph_files/bench0_1/harder_graph_n=800_k=2_stores=40_gyms=40_opt=20.gml",
        # "./graph_files/bench0_1/harder_graph_n=1600_k=2_stores=40_gyms=40_opt=40.gml",
        # "./graph_files/bench0_2/test_graph_n=25_k=3_stores=5_gyms=5_opt=5.gml",
        # "./graph_files/bench0_2/test_graph_n=30_k=3_stores=5_gyms=5_opt=6.gml",
        # "./graph_files/bench0_2/test_graph_n=35_k=3_stores=5_gyms=5_opt=7.gml",
        # "./graph_files/bench0_2/test_graph_n=40_k=3_stores=6_gyms=6_opt=7.gml",
        # "./graph_files/bench0_2/test_graph_n=45_k=3_stores=6_gyms=6_opt=8.gml",
        # "./graph_files/bench0_2/test_graph_n=50_k=3_stores=6_gyms=6_opt=9.gml",
        # "./graph_files/bench0_2/test_graph_n=100_k=3_stores=10_gyms=10_opt=10.gml",
        # "./graph_files/bench0_2/test_graph_n=150_k=3_stores=10_gyms=10_opt=15.gml",
        # "./graph_files/bench0_2/test_graph_n=200_k=3_stores=15_gyms=15_opt=14.gml",
        # "./graph_files/bench0_2/test_graph_n=250_k=3_stores=20_gyms=20_opt=13.gml",
        # "./graph_files/bench0_2/test_graph_n=400_k=3_stores=20_gyms=20_opt=20.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=1000_k=2_stores=40_gyms=40_opt=25.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=2000_k=2_stores=40_gyms=40_opt=50.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=4000_k=2_stores=40_gyms=40_opt=100.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=8000_k=2_stores=40_gyms=40_opt=200.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=16000_k=2_stores=40_gyms=40_opt=400.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=32000_k=2_stores=80_gyms=80_opt=400.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=64000_k=2_stores=160_gyms=160_opt=400.gml",
        "./graph_files/bench0_3/noise_level=1_graph_n=128000_k=2_stores=160_gyms=160_opt=800.gml",
        './graph_files/bench0_4/noise_level=1_graph_n=100_k=1_stores=10_gyms=10_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=150_k=1_stores=15_gyms=15_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=1600_k=1_stores=160_gyms=160_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=200_k=1_stores=20_gyms=20_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=25_k=1_stores=5_gyms=5_opt=5.gml', './graph_files/bench0_4/noise_level=1_graph_n=30_k=1_stores=5_gyms=5_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=35_k=1_stores=6_gyms=6_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=4000_k=1_stores=200_gyms=200_opt=20.gml', './graph_files/bench0_4/noise_level=1_graph_n=400_k=1_stores=40_gyms=40_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=40_k=1_stores=7_gyms=7_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=45_k=1_stores=8_gyms=8_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=50_k=1_stores=9_gyms=9_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=800_k=1_stores=80_gyms=80_opt=10.gml'
    ]
    bench_4 = ['./graph_files/bench0_4/noise_level=1_graph_n=100_k=1_stores=10_gyms=10_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=150_k=1_stores=15_gyms=15_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=1600_k=1_stores=160_gyms=160_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=200_k=1_stores=20_gyms=20_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=25_k=1_stores=5_gyms=5_opt=5.gml', './graph_files/bench0_4/noise_level=1_graph_n=30_k=1_stores=5_gyms=5_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=35_k=1_stores=6_gyms=6_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=4000_k=1_stores=200_gyms=200_opt=20.gml', './graph_files/bench0_4/noise_level=1_graph_n=400_k=1_stores=40_gyms=40_opt=10.gml', './graph_files/bench0_4/noise_level=1_graph_n=40_k=1_stores=7_gyms=7_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=45_k=1_stores=8_gyms=8_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=50_k=1_stores=9_gyms=9_opt=6.gml', './graph_files/bench0_4/noise_level=1_graph_n=800_k=1_stores=80_gyms=80_opt=10.gml']
    path = './graph_files/bench0_3/'
    tb = 0
    for graph in files:
        if(tb == 8):
            path = './graph_files/bench0_4/'
            # function_names.append(b.partition_lgraph_louvain.__name__)
        test = 200
        b = PlottedStoreShops(0, 0, [0, 0])
        b.import_lgraph(graph, graph)
        people = b.n
        stores = len(b.C[0])
        k = 2
        gyms = len(b.C[1])
        tb += 1
        # Writing data
        for function_name in function_names:
            headers = ['Max Component Size', 'Compute Time (s)', function_name]
            csv_file = "{path}results_{function}_{people}_k={k}_stores={stores}_gyms={gyms}.csv".format(
                path=path, function = function_name ,people=people, gyms=gyms, stores=stores, k=k
            )
            passed = 0
            component_results = []
            timing_results = []
            for i in range(test):
                print("Computing test {i} of function {function}".format(i = i, function=function_name))
                c = PlottedStoreShops(0, 0, [0, 0])
                c.import_lgraph(graph, graph)
                start_time = time.perf_counter()
                # findMethod(c, function_name)
                result = findMethod(c, function_name)
                # c.G_to_disjoint()
                # result = c.runScen3_1_rand()
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
                for i in range(len(timing_results)):
                    writer.writerow([component_results[i], timing_results[i]])


    # people = 1600
    # gyms = 20
    # stores = 20
    # k = 3
    # test = 200 # number of test
    # # Construct graph
    # b = PlottedStoreShops(0, 0, [0, 0])
    # #Test graph
    # function_names = [b.runScen3Random.__name__]
    #  b.partition_lgraph_spectral.__name__, b.partition_lgraph_louvain.__name__]
    # for b in range(5,6):
    #     path = "./graph_files/bench{b}/".format(b=b)
    #     custom_graph = "{path}test_graph_n={people}_k={k}_stores={stores}_gyms={gyms}.gml".format(
    #         path=path, people=people, gyms=gyms, stores=stores, k=k
    #     )
    #     data_path = "{path}location_data_n={people}_k={k}_stores={stores}_gyms={gyms}.json".format(
    #         path=path, people=people, gyms=gyms, stores=stores, k=k
    #     )
    #     # b = PlottedStoreShops(people, k, [gyms, stores])
    #     # b.setup()
    #     # b.export(custom_graph, data_path)
    #     for function_name in function_names:
    #         timing_results = []
    #         component_results = []
    #         headers = ['Max Component Sizes', 'Compute Time (s)', function_name]

    #         #Writing data
    #         csv_file = "{path}results_{function}_{people}_k={k}_stores={stores}_gyms={gyms}.csv".format(
    #             path=path, function = function_name ,people=people, gyms=gyms, stores=stores, k=k
    #         )

    #         passed = 0
    #         for i in range(test):
    #             print("Computing test {i}".format(i = i))
    #             c = PlottedStoreShops(0, 0, [0, 0])
    #             c.import_lgraph(custom_graph, custom_graph)
    #             start_time = time.perf_counter()
    #             result = findMethod(c, function_name)
    #             # findMethod(c, function_name)
    #             # c.G_to_disjoint()
    #             # result = c.runScen3_1_rand()
    #             end_time = time.perf_counter() - start_time
    #             del c
    #             if(result == -1):
    #                 continue
    #             timing_results.append(end_time)
    #             component_results.append(result)
    #             print("Finished with size {size}".format(size=result))
    #             passed += 1
    #         f = open(csv_file, "w")
    #         f.close
    #         with open(csv_file, 'w', newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow(headers)
    #             for i in range(passed):
    #                 writer.writerow([timing_results[i], component_results[i]])
    #     people *= 2
    #     stores *= 2
    #     gyms *=2
    # b.partition_lgraph_spectral()
    # b.G_to_disjoint()
    # print(b.runScen2_3_1_rand())

    # c = PlottedStoreShops(4, 4, [5,5])
    # b.setup()
    # b.import_lgraph(custom_graph, custom_graph)
    # print(b.runScen2_3_1_rand())
    # path = "./graph_files/bench2/"
    # pos = nx.spring_layout(b.G)
    # custom_graph = "{path}test_graph_n=200_k=3_stores=40_gyms=40.gml".format(path=path)
    # color_map = []
    # for node in range(280):
    #     if node < 200:
    #         color_map.append('green')
    #     elif node < 240:
    #         color_map.append('blue')
    #     else: 
    #         color_map.append('red')    

    
    # nx.draw_networkx_nodes(b.gObj.graph, pos, node_color=color_map)
    # nx.draw_networkx_edges(b.gObj.graph, pos, alpha=0.75)
    # c = nx.read_gml(custom_graph)
    # c = PlottedStoreShops(0, 0, [0,0])
    # c.import_lgraph(custom_graph, custom_graph)
    # c.partition_lgraph_louvain()
    # c.G_to_disjoint()
    # print('Max Component size result:' + str(c.runScen3_1_rand()))
    # nx.draw(c.gObj.graph, node_color = color_map)
    # plt.show()

    # compute the best partition
    # import community as community_louvain
    # import matplotlib.cm as cm

    # # load the karate club graph
    # G = nx.karate_club_graph()

    # # compute the best partition
    # partition = community_louvain.best_partition(G)

    # # draw the graph
    # pos = nx.spring_layout(G)
    # # color the nodes according to their partition
    # cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    # nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=200,
    #                     cmap=cmap, node_color=list(partition.values()))
    # nx.draw_networkx_edges(G, pos, alpha=0.5)
    # plt.show()

    ######################################### GENERATE GRAPH CODE ############################################
    # k = 2
    # path = "./graph_files/bench{b}/".format(b=0)
    # people = 40
    # stores = 4
    # gyms = 4
    # custom_graph = "{path}test_graph_n={people}_k={k}_stores={stores}_gyms={gyms}.gml".format(
    #     path=path, people=people, gyms=gyms, stores=stores, k=k
    # )
    # data_path = "{path}location_data_n={people}_k={k}_stores={stores}_gyms={gyms}.json".format(
    #     path=path, people=people, gyms=gyms, stores=stores, k=k
    # )
    # b = PlottedStoreShops(people, k, [gyms, stores])
    # b.setup()
    # b.export(custom_graph, data_path)