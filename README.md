## Python Engineering Modeling library

### Philosophy
The purpose of this library is to provide the right abstraction building blocks for engineers to write models.

### Progress
Current work:

#### 1. DAGs

Turns out a lot of procedural work that relies on models can be represented as a directed acyclic graphs(DAG). The DAG representation can also be used to abstract away coding module dependencies(during code building and re-building process), or work/task dependencies. Actually, even code evaluation by a compiler can be abstracted as a very complex DAG.

Here we don't try to argue that DAGs are the best representation; just that they are useful, and certain properties, like topological sorting, can be useful independent of application. Sometimes, custom representations for the application at hand might be better. This is just a starting point.

So far there is an implementation of dynamic topological sort from the [PK05a] reference available at http://homepages.ecs.vuw.ac.nz/~djp/dts.html. This can be useful, especially when DAGs are continuously constructed(and not loaded into memory just once), and get larger. This will prevent the reconstruction from scratch of the topological evaluation order of the graph.

Simultaneously there is also a *propagate* function, that finds the direct dependencies of a certain node in the graph.

TODOs:
- Add testing coverage;
- Make the dynamic graph interface more user friendly

**Why topo sort is needed:**
The most naïve approach to propagate dependencies would be to evaluate the successors of a node, and if they can't be evaluated yet, put them on hold until they can. This however, might turn into nested conditional(if) statements, which might deteriorate the performance over large "dependency" graphs. 

#### 2. Beyond DAGs

So what happens when we have cycles in the system? How do we resolve it.
