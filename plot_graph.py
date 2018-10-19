from igraph import *
import numpy as np
# from colormap import rgb2hex
import sys

graph = Graph.Read_Ncol(sys.argv[1])
graph.to_undirected(mode="collapse", combine_edges=None)

for vertex in graph.vs:
    print vertex.index, vertex['name']

layout = graph.layout('kk')
ids = [167 , 175 , 187 , 192 , 194 , 197 , 198]

visual_style = {}
# visual_style["vertex_size"] = vertex_size
# visual_style["edge_width"] = [5 + (30 * e['weight'] / max_weight) for e in graph.es()]
visual_style["vertex_color"] = ['#00ff00' if int(vertex['name']) in ids else '#ffe330' for vertex in graph.vs]
visual_style["vertex_label"] = graph.vs["name"]
visual_style["layout"] = layout
# visual_style["vertex_label_size"] = [10 + (150 * v.indegree() / float(graph.maxdegree())) for v in graph.vs()]
visual_style["bbox"] = (1366,768)
# visual_style["margin"] = 20

# print graph

plot(graph, **visual_style)