"""
Módulo 5 — Oficina de Produção

Modela as dependências entre preparações como um grafo dirigido. As 
dependências são geradas automaticamente a partir do dataset real: 
identificamos receitas-base (ver BASE_PREP_KEYWORDS em modelos.py) e 
ligamos uma aresta base -> receita sempre que o nome da base aparece 
mencionado nos ingredientes da receita dependente.
"""

import re
from estruturas.graph import Graph
from estruturas.algoritmos.topologico import topological_sort
from estruturas.algoritmos.buscas import ancestors_of


def _simplify_name(name):
    """
    Reduz o nome de uma receita-base à sua forma mais 'nua' para casar
    com menções dentro de listas de ingredientes.
    Não corta em " and "/" or ", pois esses conectivos costumam fazer parte
    do próprio nome do prato.
    """
    name = name.lower()
    name = re.split(r" with |,", name)[0]
    name = re.sub(r"[^a-z ]", "", name)
    return name.strip()


class ProductionWorkshop:
    def __init__(self, recipe_book):
        self.book = recipe_book
        self.graph = Graph(directed=True)
        self.base_names = {}
        self.injected_inconsistency = False
        self._build()

    def _build(self, max_bases=40, max_dependents_per_base=4, min_name_len=8):
        recipes = self.book.all_recipes()
        bases = [r for r in recipes if r.is_base_prep]

        used_bases = 0
        for base in bases:
            if used_bases >= max_bases:
                break

            simplified = _simplify_name(base.name)
            if len(simplified) < min_name_len or " " not in simplified:
                continue

            dependents_found = 0

            for r in recipes:
                if r.id == base.id or r.is_base_prep:
                    # Dependência só flui de um preparo-base para uma receita final.
                    # Base-para-base gera falsos ciclos devido a prefixos similares.
                    continue
                if dependents_found >= max_dependents_per_base:
                    break
                for ing in r.ingredients:
                    if simplified in ing.lower():
                        self.graph.add_edge(base.id, r.id)
                        dependents_found += 1
                        break

            if dependents_found > 0:
                self.base_names[base.id] = base.name
                self.graph.add_vertex(base.id)
                used_bases += 1

    def stats(self):
        return {
            "vertices": self.graph.num_vertices(),
            "arestas": self.graph.num_edges(),
            "receitas_base": len(self.base_names),
        }

    def inject_demo_inconsistency(self):
        edges = self.graph.edges()
        if not edges:
            return False
        u, v, _ = edges[0]
        self.graph.add_edge(v, u)
        self.injected_inconsistency = True
        return True

    def remove_demo_inconsistency(self):
        self.graph = Graph(directed=True)
        self.base_names = {}
        self.injected_inconsistency = False
        self._build()

    def sequencia_producao(self):
        order, cycle = topological_sort(self.graph)
        return order, cycle

    def existe_erro_dependencia(self):
        _, cycle = topological_sort(self.graph)
        return cycle

    def preparos_antes_de(self, recipe_id):
        if recipe_id not in self.graph.vertices():
            return None
        return ancestors_of(self.graph, recipe_id)

    def _nome(self, recipe_id):
        r = self.book.search_by_id(recipe_id)
        return r.name if r else recipe_id

    def menu_producao(self):
        while True:
            print("\n Oficina de Produção (Módulo 5)")
            stats = self.stats()
            print(f"   grafo: {stats['vertices']} vértices | {stats['arestas']} arestas | "
                  f"{stats['receitas_base']} receitas-base identificadas")
            print("1. Sequência válida de produção (ordenação topológica)")
            print("2. Existe erro de dependência? (detectar ciclos)")
            print("3. Quais preparos precisam ser concluídos antes da receita X?")
            print("4. Injetar inconsistência de demonstração (cria um ciclo)")
            print("5. Remover inconsistência de demonstração")
            print("0. Voltar")

            op = input("Escolha uma opção: ")

            if op == "1":
                order, cycle = self.sequencia_producao()
                if order is not None:
                    print(f"\nSequência válida ({len(order)} etapas):")
                    for i, rid in enumerate(order, 1):
                        print(f"  {i}. {self._nome(rid)}")
                else:
                    print(
                        "\nNão existe sequência válida — dependência circular encontrada:")
                    print("  " + " -> ".join(self._nome(rid) for rid in cycle))

            elif op == "2":
                cycle = self.existe_erro_dependencia()
                if cycle:
                    print("\nSim! Ciclo de dependência detectado:")
                    print("  " + " -> ".join(self._nome(rid) for rid in cycle))
                else:
                    print(
                        "\nNão há inconsistências. Todas as dependências formam um DAG válido.")

            elif op == "3":
                rid = input("ID da receita: ").strip()
                result = self.preparos_antes_de(rid)
                if result is None:
                    print("Receita não encontrada no grafo de dependências.")
                elif not result:
                    print(
                        "Nenhum preparo intermediário depende disso — pode ser produzida diretamente.")
                else:
                    print(
                        f"\nPreparos que precisam ser concluídos antes de '{self._nome(rid)}':")
                    for pid in result:
                        print(f"  • {self._nome(pid)}")

            elif op == "4":
                ok = self.inject_demo_inconsistency()
                print(
                    "Inconsistência injetada." if ok else "Grafo sem arestas suficientes.")

            elif op == "5":
                self.remove_demo_inconsistency()
                print("Grafo reconstruído sem inconsistências.")

            elif op == "0":
                break

            else:
                print("Opção inválida.")
