from estruturas.graph import Graph
import heapq


def dijkstra(grafo: Graph, source):
    dist = {v: float("inf") for v in grafo.adj}
    prev = {v: None for v in grafo.adj}
    dist[source] = 0
    heap = [(0, source)]
    visited = set()

    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)

        for e in grafo.adj.get(u, []):
            v, w = e["to"], e["weight"]
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                prev[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, prev


def shortest_path(grafo: Graph, source, target):
    dist, prev = dijkstra(grafo, source)
    if dist.get(target, float("inf")) == float("inf"):
        return None, float("inf")

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path, dist[target]
