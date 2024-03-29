from igraph import *
import numpy as np
# from colormap import rgb2hex
import sys

graph = Graph.Read_Ncol(sys.argv[1])
graph.to_undirected(mode="collapse", combine_edges=None)

id_name_dict = {}
name_id_dict = {}

for vertex in graph.vs:
    id_name_dict.update({vertex.index: int(vertex['name'])})
    name_id_dict.update({int(vertex['name']): vertex.index})

layout = graph.layout('kk')
# names = [9, 4, 5, 3, 32, 61, 25, 27, 19, 20]
# names = [232, 231, 179, 167, 207, 215, 237, 1, 137, 102, 58, 20, 25, 64, 178, 21, 89, 60, 52, 51, 118, 24, 15, 78, 48, 121, 54, 61, 177, 70, 2, 218, 217, 152, 128]
names = [6, 9, 127, 113, 45, 90, 48, 196, 2, 111, 69, 65, 43, 14, 7, 44, 102, 53, 71, 143, 172, 42, 46, 17, 175, 114, 177, 64, 171, 179]

# Olhar isso daqui
ids = [name_id_dict[i] for i in names]
print ids

visual_style = {}
# visual_style["vertex_size"] = vertex_size
# visual_style["edge_width"] = [5 + (30 * e['weight'] / max_weight) for e in graph.es()]
visual_style["vertex_color"] = ['#00ff00' if int(vertex['name']) in names else '#ffe330' for vertex in graph.vs]
visual_style["vertex_label"] = graph.vs["name"]
visual_style["layout"] = layout
# visual_style["vertex_label_size"] = [10 + (150 * v.indegree() / float(graph.maxdegree())) for v in graph.vs()]
visual_style["bbox"] = (800,600)
# visual_style["margin"] = 20

# print graph



# print graph.betweenness()
# print graph.pagerank()
# print graph.closeness()
# print graph.vs.degree()

betweenness_tmp = graph.betweenness()
pagerank_tmp = graph.pagerank()
closeness_tmp = graph.closeness()
degree_tmp = graph.vs.degree()

# print sys.argv[1], ":"
# print "id\tbetweenness\tpagerank\tcloseness\tdegree"
# for id in ids:
#     print id_name_dict[id],'\t', betweenness_tmp[id], '\t', pagerank_tmp[id], '\t', closeness_tmp[id], '\t', degree_tmp[id]


plot(graph, **visual_style)