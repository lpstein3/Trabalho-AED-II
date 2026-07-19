from estruturas.graph import Graph


def minimum_spanning_tree(grafo: Graph):
    parent = {v: v for v in grafo.adj}
    rank = {v: 0 for v in grafo.adj}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    mst_edges = []
    total_cost = 0.0
    sorted_edges = sorted(grafo.edges(), key=lambda e: e[2])

    for u, v, w in sorted_edges:
        if union(u, v):
            mst_edges.append((u, v, w))
            total_cost += w
    return mst_edges, total_cost
