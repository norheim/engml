from dyanmictopo import DynamicGraph, print_topo
from itertools import count
import networkx as nx

class Expression():
    #G = DynamicGraph(nx.DiGraph())
    #counter = count()
    def __init__(self):
        self.G = DynamicGraph(nx.DiGraph())

    def propagate(self, exprname):
        return self.G.propagate(exprname)

    # Adding and updating currently are the same thing
    def add(self, name, dependencies=[]):
        if len(dependencies) == 0 and name not in self.G.G.nodes():
            self.G.add_node(name)
            return self.propagate(name)
        else:
            if name in self.G.G.nodes():
                existing_deps = list(self.G.G.predecessors(name))
            else:
                existing_deps = []
            # print(existing_deps)
            # Remove existing dependencies
            for dep in existing_deps:
                if dep not in dependencies:
                    self.G.remove_edge(dep, name)
            # Add new dependencies
            for dep in dependencies:
                if dep not in existing_deps:
                    self.G.add_edge(dep, name)
            # Finish by propagating changes
            return self.propagate(name)
class System():
    def __init__(self):
        pass
