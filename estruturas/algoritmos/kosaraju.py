from estruturas.graph import Graph


def kosaraju(grafo):
    visited = set()
    stack = []

    def dfs_pass1(u):
        visited.add(u)
        for e in grafo.adj.get(u, []):
            if e["to"] not in visited:
                dfs_pass1(e["to"])
        stack.append(u)

    for v in grafo.vertices():
        if v not in visited:
            dfs_pass1(v)

    transposed = grafo.transpose()
    visited.clear()
    sccs = []

    def dfs_pass2(u, current_scc):
        visited.add(u)
        current_scc.append(u)
        for e in transposed.adj.get(u, []):
            if e["to"] not in visited:
                dfs_pass2(e["to"], current_scc)

    while stack:
        v = stack.pop()
        if v not in visited:
            current_scc = []
            dfs_pass2(v, current_scc)
            sccs.append(current_scc)

    return [scc for scc in sccs if len(scc) > 1]
