from collections import deque
from estruturas.graph import Graph


def max_flow(grafo: Graph, source, sink):
    residual = {}
    for u in grafo.adj:
        residual[u] = {}
    for u in grafo.adj:
        for e in grafo.adj[u]:
            cap = e["capacity"] if e["capacity"] is not None else e["weight"]
            residual[u][e["to"]] = residual[u].get(e["to"], 0) + cap
            residual.setdefault(e["to"], {})
            residual[e["to"]].setdefault(u, 0)

    def bfs_augmenting_path():
        parent = {source: None}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            if u == sink:
                break
            for v, cap in residual.get(u, {}).items():
                if cap > 0 and v not in parent:
                    parent[v] = u
                    queue.append(v)
        if sink not in parent:
            return None
        path = []
        cur = sink
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path

    max_flow_value = 0
    while True:
        path = bfs_augmenting_path()
        if path is None:
            break
        bottleneck = min(residual[path[i]][path[i + 1]]
                         for i in range(len(path) - 1))
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck
        max_flow_value += bottleneck

    return max_flow_value, residual


def min_cut_edges(grafo: Graph, source, sink):
    _, residual = max_flow(grafo, source, sink)
    visited = {source}
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v, cap in residual.get(u, {}).items():
            if cap > 0 and v not in visited:
                visited.add(v)
                queue.append(v)

    cut_edges = []
    for u in grafo.adj:
        if u in visited:
            for e in grafo.adj[u]:
                if e["to"] not in visited:
                    cut_edges.append(
                        (u, e["to"], e["capacity"] or e["weight"]))
    return cut_edges
