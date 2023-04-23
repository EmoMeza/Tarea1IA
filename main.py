#create a search tree structure, using:
#1. Greedy Search
#2. Search by uniform cost
#3. Search by depth
#4. A* search

#for each search, print the path and the quantity of nodes visited(times per node and total)

#first we create a class named Graph, which will be used to create the search tree

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.heuristic = {}