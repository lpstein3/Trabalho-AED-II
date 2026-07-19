"""
Módulo 6 — Otimização de Cardápio (Menu Degustação)

Resolve o Problema da Mochila 0/1 utilizando Programação Dinâmica (Bottom-Up).
O objetivo é maximizar o lucro (ou avaliação) do cardápio sem ultrapassar
um limite rigoroso (orçamento máximo ou tempo limite de preparo).
"""


class MenuOptimizer:
    def __init__(self, recipe_book):
        self.book = recipe_book

    def optimize_01_knapsack(self, items, capacity_limit, weight_attr, value_attr):
        n = len(items)
        # Inicializa a matriz dp[n+1][W+1] com zeros
        dp = [[0] * (capacity_limit + 1) for _ in range(n + 1)]

        # Preenchimento da matriz Bottom-Up
        for i in range(1, n + 1):
            item = items[i - 1]

            # Garantir que o peso seja um valor inteiro para indexar a matriz
            weight = int(getattr(item, weight_attr))
            value = float(getattr(item, value_attr))

            for w in range(1, capacity_limit + 1):
                if weight <= w:
                    # O item cabe: escolhe o máximo entre incluir ou não incluir o item
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
                else:
                    # O item não cabe: mantém o valor anterior
                    dp[i][w] = dp[i - 1][w]

        # Reconstrução do caminho para descobrir quais itens foram selecionados
        max_value = dp[n][capacity_limit]
        w = capacity_limit
        selected_items = []

        for i in range(n, 0, -1):
            if max_value <= 0:
                break

            # Se o valor atual é diferente do valor da linha de cima, o item foi incluído
            if dp[i][w] != dp[i - 1][w]:
                item = items[i - 1]
                selected_items.append(item)
                max_value -= float(getattr(item, value_attr))
                w -= int(getattr(item, weight_attr))

        # Reverte a lista para manter a ordem original
        selected_items.reverse()

        # Retorna o valor ótimo exato da matriz e os itens escolhidos
        return dp[n][capacity_limit], selected_items

    def menu_otimizacao(self):
        while True:
            print("\n Otimização de Menu Degustação (Módulo 6)")
            print("1. Maximizar Lucro (Restrição de Orçamento)")
            print("2. Maximizar Avaliação (Restrição de Tempo de Preparo)")
            print("0. Voltar")

            op = input("Escolha uma opção: ")

            if op == "0":
                break

            if op not in ["1", "2"]:
                print("Opção inválida.")
                continue

            # Para evitar que o array fique gigantesco e estoure a RAM num computador normal,
            # nós filtramos os pratos principais para garantir que a PD rode instantaneamente
            # na hora da apresentação (sempre mantendo a integridade teórica do algoritmo).
            all_recipes = [r for r in self.book.all_recipes()
                           if r.dish_class == "principal"]

            # Pega as 100 primeiras para demonstração ágil
            demo_recipes = all_recipes[:100]

            if op == "1":
                try:
                    orcamento_maximo = int(
                        input("Informe o orçamento máximo do cardápio (ex: 150): "))
                except ValueError:
                    print("Por favor, introduza um valor numérico inteiro.")
                    continue

                print(
                    f"\nA analisar {len(demo_recipes)} receitas para encontrar o Lucro Máximo...")

                max_profit, best_menu = self.optimize_01_knapsack(
                    items=demo_recipes,
                    capacity_limit=orcamento_maximo,
                    weight_attr='cost',
                    value_attr='profit'
                )

                print("\n=== Menu Otimizado (Maior Lucro) ===")
                total_cost = 0
                for item in best_menu:
                    print(
                        f"- {item.name} (Custo: R${item.cost:.2f} | Lucro: R${item.profit:.2f})")
                    total_cost += item.cost

                print("-" * 30)
                print(
                    f"Custo Total Utilizado: R${total_cost:.2f} / R${orcamento_maximo:.2f}")
                print(f"Lucro Máximo Atingido: R${max_profit:.2f}")

            elif op == "2":
                try:
                    tempo_maximo = int(
                        input("Informe o tempo máximo de preparo acumulado em minutos (ex: 120): "))
                except ValueError:
                    print("Por favor, introduza um valor numérico inteiro.")
                    continue

                print(
                    f"\nA analisar {len(demo_recipes)} receitas para encontrar a Avaliação Máxima...")

                max_rating, best_menu = self.optimize_01_knapsack(
                    items=demo_recipes,
                    capacity_limit=tempo_maximo,
                    weight_attr='prep_time',
                    value_attr='rating'
                )

                print("\n=== Menu Otimizado (Melhor Avaliação) ===")
                total_time = 0
                for item in best_menu:
                    print(
                        f"- {item.name} (Tempo: {item.prep_time} min | Avaliação: {item.rating})")
                    total_time += item.prep_time

                print("-" * 30)
                print(
                    f"Tempo Total Utilizado: {total_time} min / {tempo_maximo} min")
                print(f"Soma de Avaliações Atingida: {max_rating:.2f}")
