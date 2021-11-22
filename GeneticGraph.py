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
e = 30
# VARIABLE: Desired k-clique size to find
# size_k = 4
# Generate graph with probability
# g = nx.erdos_renyi_graph(n, p)
# Generate graph with specifying num of edges
g = nx.gnm_random_graph(n, e)

def foo(graph):
    max = 0
    for c in nx.find_cliques(graph):
        if len(c) > max:
            max = len(c)

    return max

# Fitness function for genetic algorithm, returns the max clique (array of nodes)
def foo2(graph):
    max = []
    for c in nx.find_cliques(graph):
        if len(c) > len(max):
            max = c

    return max

def genetic(g, n):
    solutions = []
    improvementLimit = 10                 # VARIABLE: Number of times algorithm will repeat after no new improvements
    populationSize = 40                   # VARIABLE: Population size, number of subgraphs to create in each generation
    maxSize = 20                          # VARIABLE: Max sample size of subgraph
    if n < maxSize:
        maxSize = n / 2

    print('Creating initial samples')
    for s in range(populationSize):
        print('Creating sample: ', s)

        newGraph = g.subgraph(random.sample(g.nodes, int(random.uniform(2, maxSize))))
        secondGraph = g.subgraph(random.sample(g.nodes, int(random.uniform(2, maxSize))))
        solutions.append(nx.disjoint_union(newGraph, secondGraph))

    finalTuple = 0
    noImprovement = 0
    i = 0
    while noImprovement < improvementLimit:
        i += 1
        rankedSolutions = []
        for s in solutions:
            print('Gen: ', i, ' Solution: ', s)
            rankedSolutions.append((len(foo2(s)), foo2(s), s))

        rankedSolutions = sorted(rankedSolutions, key=lambda x:x[0])
        rankedSolutions.reverse()

        if rankedSolutions[0][0] > finalTuple:
            print('Current max:', rankedSolutions[0][0])
            finalTuple = rankedSolutions[0][0]
        else:
            noImprovement += 1

        bestSolutions = rankedSolutions[:10]

        newGen=[]
        for _ in range(int(populationSize / 2)):
            randomBest = random.choice(bestSolutions)
            newGenGraphNodes = (randomBest[1] + random.sample(g.nodes, int(random.uniform(2, maxSize))))
            newGenGraph = g.subgraph(list(newGenGraphNodes))
            newGen.append(newGenGraph)

        for _ in range(int(populationSize / 2)):
            newGraph = g.subgraph(random.sample(g.nodes, int(random.uniform(2, maxSize))))
            secondGraph = g.subgraph(random.sample(g.nodes, int(random.uniform(2, maxSize))))
            newGen.append(nx.disjoint_union(newGraph, secondGraph))

        solutions = newGen

    return finalTuple

### Running the algorithms ###

# Genetic algorithm function
start = timeit.default_timer()
print('Genetic Algorithm')
print('Maximum found: %d-clique' % genetic(g, n))
nonexactStop = timeit.default_timer()
nonexactStopTime = nonexactStop - start
print('Time: ', nonexactStopTime)          # the running time exclude the running time for exhaustive

# Exact max clique found (to check how accurate genetic algorithm is, takes a long time)
print('Exact Max clique: ', foo(g))
checker = timeit.default_timer()
checkerTime = checker - nonexactStop
print('Exact Max Time: ', checkerTime)          # the checking time

# Calculates percentage of improvement of runtime for genetic algorithm compared to exact max clique function
print("Improvement: ", (checkerTime/nonexactStopTime)*100)


##### Display Graph #####
pos = nx.spring_layout(g)
nx.draw_networkx(g, pos)
plt.title("Random Graph Generation Example")
plt.show()
