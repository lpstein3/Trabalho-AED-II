
class Graph:
    def __init__(self, directed=True):
        self.directed = directed
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v, weight=1.0, capacity=None):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append({"to": v, "weight": weight, "capacity": capacity})
        if not self.directed:
            self.adj[v].append(
                {"to": u, "weight": weight, "capacity": capacity})

    def vertices(self):
        return list(self.adj.keys())

    def edges(self):
        result = []
        seen = set()
        for u in self.adj:
            for e in self.adj[u]:
                key = (u, e["to"]) if self.directed else tuple(
                    sorted((u, e["to"])))
                if key in seen and not self.directed:
                    continue
                seen.add(key)
                result.append((u, e["to"], e["weight"]))
        return result

    def num_vertices(self):
        return len(self.adj)

    def num_edges(self):
        return len(self.edges())

    def neighbors(self, v):
        return self.adj.get(v, [])

    def transpose(self):
        g = Graph(directed=self.directed)
        for u in self.adj:
            g.add_vertex(u)
        for u, v, w in self.edges():
            g.add_edge(v, u, w)
        return g
