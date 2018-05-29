from dyanmictopo import DynamicGraph, print_topo
import networkx as nx

def to_nx(graph):
    G = nx.DiGraph()
    for key, val in graph.items():
        for node in val:
            G.add_edge(key, node)
    return G

graph = {5: [11],
    7: [11,8],
    3: [8,10],
    11:[2,9,10],
    8: [9]}
graph2 = dict(graph)
graph2.update({2: [9]})
G = DynamicGraph(to_nx(graph))
#G2 = DynamicGraph(to_nx(graph2))
#print_topo(G.topo)
#print_topo(G2.topo)
#print_topo(G.add_edge(2, 9))
#print_topo(G.add_edge(9, 4))
print_topo(G.add_edge(3, 1))
print_topo(G.add_edge(1, 7))
G.propagate(8)
print_topo(G.remove_edge(3, 1))
G.propagate(3)
print_topo(G.remove_edge(11, 10))
G.propagate(11)
print_topo(G.add_edge(10, 5))
G.propagate(7)
print_topo(G.add_edge(11, 8))
G.propagate(3)
