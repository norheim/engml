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

import networkx as nx
import warnings

def dfs(G, topo, start, bound=None, forward=True):
    visited, stack = set(), [start]
    if bound==None:
        bound = len(topo)+1
    if forward:
        adj, comp = G.successors, lambda w: topo[w] < bound
    else:
        adj, comp = G.predecessors, lambda w: topo[w] > bound
    while stack:
        w = stack.pop()
        #print(w)
        if topo[w] == bound:
            return False
        if w not in visited and comp(w):
            visited.add(w)
            stack.extend(set(adj(w)) - visited)
    return sorted(list(visited), key=lambda w: topo[w])


def nx_add_edge(G, x, y, topo):
    lb = topo[y]
    ub = topo[x]
    new_topo = dict(topo)
    if lb < ub:
        dxyF = dfs(G, topo, y, ub, forward=True)
        dxyB = dfs(G, topo, x, lb, forward=False)
        if dxyB and dxyF:
            new_list = dxyB + dxyF #reordered
            old_order = sorted([topo[elt] for elt in new_list])
            #print(old_order)
            #print(new_list)
            for idx, w in enumerate(new_list):
                #print(w, old_order[idx])
                new_topo[w] = old_order[idx]
        else:
            warnings.warn("Cycle detected", UserWarning)
    return new_topo

def print_topo(topo):
    return [key for key,value in sorted(topo.items(),
    key=lambda kv: (kv[1],kv[0]))]

class DynamicGraph:
    def __init__(self, G):
        self.G = G
        self.topo = self.topo_sort(G)

    @staticmethod
    def topo_sort(G):
        topo_list = nx.topological_sort(G)
        topo = {elt: idx for idx, elt in enumerate(topo_list)}
        return topo

    def propagate(self, v):
        return dfs(self.G, self.topo, v)

    def remove_edge(self, x, y):
        self.G.remove_edge(x, y)
        return self.topo

    def add_node(self, x):
        self.G.add_node(x)
        neword = len(self.topo.values())+1
        self.topo[x] = neword

    def add_edge(self, x, y):
        if x not in self.G.nodes():
            self.add_node(x)
        if y in self.G[x]: # edge already exists
            return self.topo
        elif x in self.G.nodes() and y not in self.G.nodes():
            self.G.add_edge(x, y)
            neword = len(self.topo.values())+1
            self.topo[y] = neword
        elif x in self.G.nodes() and y in self.G.nodes():
            self.G.add_edge(x, y)
            new_topo = nx_add_edge(self.G, x, y, self.topo)
            self.topo = new_topo
        return self.topo
