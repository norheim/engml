from dyanmictopo import DynamicGraph, print_topo
from itertools import count
import networkx as nx

class Expression():
    #G = DynamicGraph(nx.DiGraph())
    #counter = count()
    def __init__(self):
        self.G = DynamicGraph(nx.DiGraph())

    # Adding and updating currently are the same thing
    def add(self, name, dependencies=[]):
        if len(dependencies) == 0 and name not in self.G.G.nodes():
            self.G.add_node(name)
        else:
            if name in self.G.G.nodes():
                existing_deps = list(self.G.G.predecessors(name))
            else:
                existing_deps = []
            print(existing_deps)
            #Remove existing dependencies
            for dep in existing_deps:
                if dep not in dependencies:
                    self.G.remove_edge(dep, name)
            #Add new dependencies
            for dep in dependencies:
                if dep not in existing_deps:
                    self.G.add_edge(dep, name)

e = Expression()
e.add(5)
e.add(7)
e.add(3)
print_topo(e.G.topo)
e.add(11, [5, 7])
e.add(8, [7, 3])
e.add(2, [11])
e.add(9, [11])
e.add(10, [3])
e.add(7, [10])
e.add(7, [])
e.G.propagate(10)
# technically an update

class System():
    def __init__(self):
        pass
