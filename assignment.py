import random
from itertools import permutations


def karger_min_cut(graph, iterations=100):

    def contract_edge(local_graph, u, v):
        local_graph[u].extend(local_graph[v])
        
        for neighbor in local_graph[v]:
            local_graph[neighbor] = [u if x == v else x for x in local_graph[neighbor]]
        
        local_graph[u] = [x for x in local_graph[u] if x != u]
        
        del local_graph[v]
    
    min_cut = float('inf')
    
    for _ in range(iterations):
        local_graph = {u: list(vs) for u, vs in graph.items()}
        
        while len(local_graph) > 2:
            u = random.choice(list(local_graph.keys()))
            v = random.choice(local_graph[u])
            contract_edge(local_graph, u, v)
        
        remaining_edges = list(local_graph.values())[0]
        cut_size = len(remaining_edges)
        min_cut = min(min_cut, cut_size)
    
    return min_cut



def tarjan_scc(graph):
   
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlinks = {}
    sccs = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlinks[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)

        for w in graph[v]:
            if w not in indices:
                strongconnect(w)
                lowlinks[v] = min(lowlinks[v], lowlinks[w])
            elif w in on_stack:
                lowlinks[v] = min(lowlinks[v], indices[w])
        
        if lowlinks[v] == indices[v]:
            scc = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                scc.append(w)
                if w == v:
                    break
            sccs.append(scc)
    
    for v in graph:
        if v not in indices:
            strongconnect(v)
    
    return sccs


def are_isomorphic(graph1, graph2):
   
    if len(graph1) != len(graph2):
        return False
    
    edges1 = sum(len(vs) for vs in graph1.values()) // 2
    edges2 = sum(len(vs) for vs in graph2.values()) // 2
    if edges1 != edges2:
        return False

    deg_seq1 = sorted([len(vs) for vs in graph1.values()])
    deg_seq2 = sorted([len(vs) for vs in graph2.values()])
    if deg_seq1 != deg_seq2:
        return False

    nodes1 = list(graph1.keys())
    nodes2 = list(graph2.keys())

    for perm in permutations(nodes2):
        mapping = dict(zip(nodes1, perm))
        if all(sorted([mapping[n] for n in graph1[u]]) == sorted(graph2[mapping[u]]) 
               for u in graph1):
            return True
    return False


graph = {
    'A': ['B', 'C', 'D'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['A', 'B', 'C']
}
print("Minimum Cut:", karger_min_cut(graph, iterations=50))

directed_graph = {
    'A': ['B'],
    'B': ['C', 'E', 'F'],
    'C': ['D', 'G'],
    'D': ['C', 'H'],
    'E': ['A', 'F'],
    'F': ['G'],
    'G': ['F'],
    'H': ['D', 'G']
}
print("Strongly Connected Components:", tarjan_scc(directed_graph))

g1 = {
    1: [2, 3],
    2: [1, 3],
    3: [1, 2]
}
g2 = {
    'x': ['y', 'z'],
    'y': ['x', 'z'],
    'z': ['x', 'y']
}
print("Are Isomorphic:", are_isomorphic(g1, g2))
