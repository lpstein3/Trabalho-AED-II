import random
from estruturas.graph import Graph
from estruturas.algoritmos.dijkstra import dijkstra, shortest_path
from estruturas.algoritmos.kruskal import minimum_spanning_tree
from estruturas.algoritmos.fluxo import max_flow, min_cut_edges
from estruturas.algoritmos.kosaraju import kosaraju

FONTE = "FONTE"
SUMIDOURO = "SUMIDOURO"


class LogisticsNetwork:
    def __init__(self, recipe_book, n_kitchens=8, n_regions=24, seed=42):
        self.book = recipe_book
        self.rng = random.Random(seed)

        self.kitchens = [f"Cozinha {i}" for i in range(1, n_kitchens + 1)]
        self.regions = [f"Região {i}" for i in range(1, n_regions + 1)]

        self.time_graph = Graph(directed=False)
        self.flow_graph = Graph(directed=True)

        self._build()

    def _build(self, target_edges=55):
        nodes = self.kitchens + self.regions
        for n in nodes:
            self.time_graph.add_vertex(n)

        shuffled = nodes[:]
        self.rng.shuffle(shuffled)
        for i in range(1, len(shuffled)):
            j = self.rng.randint(0, i - 1)
            weight = self.rng.randint(5, 30)
            self.time_graph.add_edge(shuffled[i], shuffled[j], weight)

        edge_keys = {tuple(sorted((u, v)))
                     for u, v, _ in self.time_graph.edges()}
        attempts = 0
        while len(edge_keys) < target_edges and attempts < 5000:
            a, b = self.rng.sample(nodes, 2)
            key = tuple(sorted((a, b)))
            if key not in edge_keys:
                self.time_graph.add_edge(a, b, self.rng.randint(5, 30))
                edge_keys.add(key)
            attempts += 1

        self.flow_graph.add_vertex(FONTE)
        self.flow_graph.add_vertex(SUMIDOURO)

        self.kitchen_capacity = {}
        for k in self.kitchens:
            capacidade_producao = self.rng.randint(15, 40)
            self.kitchen_capacity[k] = capacidade_producao
            self.flow_graph.add_edge(FONTE, k, capacity=capacidade_producao)

        self.route_capacity = {}
        for k in self.kitchens:
            atendidas = self._regioes_mais_proximas(k, n=5)
            for reg in atendidas:
                capacidade_rota = self.rng.randint(3, 10)
                self.route_capacity[(k, reg)] = capacidade_rota
                self.flow_graph.add_edge(k, reg, capacity=capacidade_rota)

            self.region_limit = {}
        for reg in self.regions:
            limite = self.rng.randint(5, 20)
            self.region_limit[reg] = limite
            self.flow_graph.add_edge(reg, SUMIDOURO, capacity=limite)

    def _regioes_mais_proximas(self, origem, n=5):
        dist, _ = dijkstra(self.time_graph, origem)
        candidatas = [(r, dist.get(r, float("inf"))) for r in self.regions]
        candidatas.sort(key=lambda x: x[1])
        return [r for r, _ in candidatas[:n]]

    def stats(self):
        return {
            "vertices_rede_tempo": self.time_graph.num_vertices(),
            "arestas_rede_tempo": self.time_graph.num_edges(),
            "cozinhas": len(self.kitchens),
            "regioes": len(self.regions),
        }

    def rota(self, origem, destino):
        if origem not in self.time_graph.vertices() or destino not in self.time_graph.vertices():
            return None, None
        return shortest_path(self.time_graph, origem, destino)

    def caminhos_alternativos(self, origem, destino, k=3):
        rotas = []
        removed = []
        graph_copy = self.time_graph

        for _ in range(k):
            path, dist = shortest_path(graph_copy, origem, destino)
            if path is None or path in [p for p, _ in rotas]:
                break
            rotas.append((path, dist))

            if len(path) < 2:
                break
            heaviest = max(
                range(len(path) - 1),
                key=lambda i: next(
                    (e["weight"] for e in graph_copy.neighbors(
                        path[i]) if e["to"] == path[i + 1]),
                    0,
                ),
            )
            u, v = path[heaviest], path[heaviest + 1]
            removed.append((u, v))

            new_graph = Graph(directed=False)
            for uu, vv, w in graph_copy.edges():
                if {uu, vv} == {u, v}:
                    continue
                new_graph.add_edge(uu, vv, w)
            graph_copy = new_graph

        return rotas

    def infraestrutura_minima(self):
        return minimum_spanning_tree(self.time_graph)

    def capacidade_maxima_atendimento(self):
        valor, _ = max_flow(self.flow_graph, FONTE, SUMIDOURO)
        return valor

    def gargalos_operacionais(self):
        return min_cut_edges(self.flow_graph, FONTE, SUMIDOURO)

    def bolhas_logisticas(self):
        return kosaraju(self.time_graph)

    def menu_logistica(self):
        while True:
            print("\n Modo Logística")
            print(f"rede: {self.stats()}\n")
            print("1. Consultar rota e tempo estimado entre dois pontos")
            print("2. Caminhos alternativos entre dois pontos")
            print("3. Infraestrutura mínima (AGM via Kruskal)")
            print("4. Capacidade máxima de atendimento simultâneo (Fluxo Máximo)")
            print("5. Identificar gargalos operacionais (Corte Mínimo)")
            print("6. Identificar bolhas logísticas (CFCs via Kosaraju)")
            print("0. Voltar")

            op = input("Escolha uma opção: ")
            match op:
                case "1":
                    o = input(f"Origem (ex: {self.kitchens[0]}): ").strip()
                    d = input(f"Destino (ex: {self.regions[0]}): ").strip()
                    path, dist = self.rota(o, d)
                    if path is None:
                        print("Rota não encontrada.")
                    else:
                        print(f"\nRota: {' -> '.join(path)}")
                        print(f"Tempo estimado: {dist} min")

                case "2":
                    o = input("Origem: ").strip()
                    d = input("Destino: ").strip()
                    rotas = self.caminhos_alternativos(o, d)
                    if not rotas:
                        print("Nenhuma rota encontrada.")
                    for i, (path, dist) in enumerate(rotas, 1):
                        print(
                            f"   Opção {i} ({dist} min): {' -> '.join(path)}")

                case "3":
                    mst, custo = self.infraestrutura_minima()
                    print(
                        f"\nInfraestrutura mínima ({len(mst)} conexões, custo total: {custo} min):")
                    for u, v, w in mst:
                        print(f"  • {u} — {v} ({w} min)")

                case "4":
                    valor = self.capacidade_maxima_atendimento()
                    print(
                        f"\nCapacidade máxima de atendimento simultâneo: {valor} pedidos/ciclo")

                case "5":
                    cortes = self.gargalos_operacionais()
                    if not cortes:
                        print("\nNenhum gargalo identificado.")
                    else:
                        print(
                            f"\n{len(cortes)} gargalo(s) operacional(is) (Corte Mínimo):")
                        for u, v, cap in cortes:
                            print(f"  • {u} -> {v} (capacidade: {cap})")

                case "6":
                    bolhas = self.bolhas_logisticas()
                    if not bolhas:
                        print(
                            "\nNenhuma bolha logística identificada (rede sem ciclos de dependência conexos).")
                    else:
                        print(
                            f"\n{len(bolhas)} bolha(s) logística(s) encontrada(s) (Kosaraju):")
                        for i, comp in enumerate(bolhas, 1):
                            print(f"  Bolha {i}: {', '.join(comp)}")

                case "0":
                    break

                case _:
                    print("Opção inválida.")
