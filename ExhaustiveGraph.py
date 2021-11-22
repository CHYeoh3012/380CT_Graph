import networkx as nx
import random
import matplotlib.pyplot as plt
from itertools import combinations
import timeit

# VARIABLE: Number of nodes
n = 50
# VARIABLE: Probability of edges
p = 0.5
# VARIABLE: Exact num of edges (possible variable, but using probability is easier)
e = 20
# VARIABLE: Desired k-clique size to find
size_k = 5
# Generate graph with probability
g = nx.erdos_renyi_graph(n, p)
# Generate graph with specifying num of edges
# g = nx.gnm_random_graph(n, e)

# Exact method for searching for size_k cliques
def exhaustive(graph, size_k):
    num = 0
    for c in combinations(graph.nodes(), size_k):
        num += 1
        miniGraph = graph.subgraph(c)
        if size_k*(size_k-1)/2 == len(miniGraph.edges()):
            return print('%d-clique exists' % size_k)
    print('%d-clique does not exist' % size_k)

# Returns max clique size (int)
def foo(graph):
    max = 0
    for c in nx.find_cliques(graph):
        if len(c) > max:
            max = len(c)

    return max

### Running the algorithms ###

# Exhaustive algorithm function
start = timeit.default_timer()
print('Exhaustive Search')
exhaustive(g, size_k)
exactStop = timeit.default_timer()
print('Time: ', exactStop - start)

##### Display Graph #####
pos = nx.spring_layout(g)
nx.draw_networkx(g, pos)
plt.title("Random Graph Generation Example")
plt.show()
