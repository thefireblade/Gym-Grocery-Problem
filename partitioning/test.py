
from DrugStoreCoffeeShopClass import DrugStoreCoffeeShops
import time 

b = DrugStoreCoffeeShops(0, 0, [0, 0])
path = "./graph_files/bench1/test_graph_n=100_k=3_stores=20_gyms=20.gml"
b.import_lgraph(path, path)
# b.partition_lgraph_louvain()
# b.G_to_disjoint()
# print(b.runScen3_1_rand())
start = time.perf_counter()
print(b.anneal())
print("time elapsed {t}(s)".format(t=time.perf_counter() - start))