from estruturas.graph import Graph
from collections import deque


def topological_sort(grafo: Graph):
    in_degree = {v: 0 for v in grafo.adj}
    for u in grafo.adj:
        for e in grafo.adj[u]:
            in_degree[e["to"]] = in_degree.get(e["to"], 0) + 1

    queue = deque([v for v in in_degree if in_degree[v] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for e in grafo.adj.get(u, []):
            in_degree[e["to"]] -= 1
            if in_degree[e["to"]] == 0:
                queue.append(e["to"])

    if len(order) == len(grafo.adj):
        return order, None
    cycle = find_cycle(grafo)
    return None, cycle


def find_cycle(grafo: Graph):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {v: WHITE for v in grafo.adj}
    parent = {}

    def _dfs(u):
        color[u] = GRAY
        for e in grafo.adj.get(u, []):
            v = e["to"]
            if color.get(v, WHITE) == WHITE:
                parent[v] = u
                result = _dfs(v)
                if result:
                    return result
            elif color.get(v) == GRAY:
                path = [u]
                cur = u
                while cur != v:
                    cur = parent[cur]
                    path.append(cur)
                path.reverse()
                return path
        color[u] = BLACK
        return None

    for v in list(grafo.adj.keys()):
        if color[v] == WHITE:
            cycle_path = _dfs(v)
            if cycle_path:
                return cycle_path
    return None
