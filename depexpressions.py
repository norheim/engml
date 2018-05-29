#Copyright (c) 2018 Johannes Norheim
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

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
