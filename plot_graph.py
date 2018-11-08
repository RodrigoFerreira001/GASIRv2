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
names = [232, 167, 179, 137, 231, 237, 25, 1, 64, 215, 21, 52, 178, 207, 20, 118, 60, 89, 102, 58, 24, 128, 51, 131, 78, 121, 15, 152, 177, 54, 48, 23, 136, 2, 218, 144, 61, 29, 133, 59]

# Olhar isso daqui
ids = [name_id_dict[i] for i in names]

visual_style = {}
# visual_style["vertex_size"] = vertex_size
# visual_style["edge_width"] = [5 + (30 * e['weight'] / max_weight) for e in graph.es()]
visual_style["vertex_color"] = ['#00ff00' if int(vertex['name']) in names else '#ffe330' for vertex in graph.vs]
visual_style["vertex_label"] = graph.vs["name"]
visual_style["layout"] = layout
# visual_style["vertex_label_size"] = [10 + (150 * v.indegree() / float(graph.maxdegree())) for v in graph.vs()]
visual_style["bbox"] = (1366,768)
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

print sys.argv[1], ":"
print "id\tbetweenness\tpagerank\tcloseness\tdegree"
for id in ids:
    print id_name_dict[id],'\t', betweenness_tmp[id], '\t', pagerank_tmp[id], '\t', closeness_tmp[id], '\t', degree_tmp[id]


plot(graph, **visual_style)