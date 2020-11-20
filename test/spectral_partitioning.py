import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx

# load the karate club graph
G = nx.karate_club_graph()

# compute the best partition
partition = community_louvain.best_partition(G)
print(partition)
# draw the graph
pos = nx.spring_layout(G)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))

nx.draw_networkx_edges(G, pos, alpha=0.75)

# labels = {i : i for i in range(40)}
# nx.draw_networkx_labels(G, pos, labels, font_size=16)

plt.show()

# import numpy as np
# import networkx as nx
# from sklearn.cluster import SpectralClustering
# from sklearn import metrics
# np.random.seed(1)

# # Get your mentioned graph
# G = nx.karate_club_graph()

# # Get ground-truth: club-labels -> transform to 0/1 np-array
# #     (possible overcomplicated networkx usage here)
# gt_dict = nx.get_node_attributes(G, 'club')
# print('nodes : {nodes}'.format(nodes=len(G.nodes())))
# gt = [gt_dict[i] for i in G.nodes()]
# gt = np.array([0 if i == 'Mr. Hi' else 1 for i in gt])

# # Get adjacency-matrix as numpy-array
# adj_mat = nx.to_numpy_matrix(G)

# print('ground truth')
# print(gt)

# # Cluster
# sc = SpectralClustering(2, affinity='precomputed', n_init=100)
# sc.fit(adj_mat)

# # Compare ground-truth and clustering-results
# print('spectral clustering')
# print(sc.labels_)
# print(len(sc.labels_))
# print('just for better-visualization: invert clusters (permutation)')
# print(np.abs(sc.labels_ - 1))

# # Calculate some clustering metrics
# print(metrics.adjusted_rand_score(gt, sc.labels_))
# print(metrics.adjusted_mutual_info_score(gt, sc.labels_))