from collections import deque
from estruturas.graph import Graph


def bfs(grafo: Graph, start):
    visited = {start}
    order = []
    queue = deque([start])
    while queue:
        u = queue.popleft()
        order.append(u)
        for e in grafo.adj.get(u, []):
            if e["to"] not in visited:
                visited.add(e["to"])
                queue.append(e["to"])
    return order


def dfs(grafo: Graph, start):
    visited = set()
    order = []

    def _visit(u):
        visited.add(u)
        order.append(u)
        for e in grafo.adj.get(u, []):
            if e["to"] not in visited:
                _visit(e["to"])
    _visit(start)
    return order


def ancestors_of(grafo: Graph, target):
    reverse = grafo.transpose()
    visited = {target}
    queue = deque([target])
    result = []
    while queue:
        u = queue.popleft()
        for e in reverse.adj.get(u, []):
            if e["to"] not in visited:
                visited.add(e["to"])
                result.append(e["to"])
                queue.append(e["to"])
    return result
