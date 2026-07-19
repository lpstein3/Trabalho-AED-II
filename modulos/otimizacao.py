class MenuOptimizer:
    def __init__(self, recipe_book):
        self.book = recipe_book

    def optimize_01_knapsack(self, items, capacity_limit, weight_attr, value_attr):
        n = len(items)
        dp = [[0] * (capacity_limit + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            item = items[i - 1]
            weight = int(getattr(item, weight_attr))
            value = float(getattr(item, value_attr))

            for w in range(1, capacity_limit + 1):
                if weight <= w:
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
                else:
                    dp[i][w] = dp[i - 1][w]

        max_value = dp[n][capacity_limit]
        w = capacity_limit
        selected_items = []

        for i in range(n, 0, -1):
            if max_value <= 0:
                break
            if dp[i][w] != dp[i - 1][w]:
                item = items[i - 1]
                selected_items.append(item)
                max_value -= float(getattr(item, value_attr))
                w -= int(getattr(item, weight_attr))

        selected_items.reverse()
        return dp[n][capacity_limit], selected_items

    def menu_otimizacao(self):
        while True:
            all_recipes = [r for r in self.book.all_recipes()
                           if r.dish_class == "principal"]
            demo_recipes = all_recipes[:100]

            print("\n Otimização de Menu Degustação")
            print("1. Maximizar Lucro (Restrição de Orçamento)")
            print("2. Maximizar Avaliação (Restrição de Tempo de Preparo)")
            print("0. Voltar")

            op = input("Escolha uma opção: ")
            match op:
                case "1":
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

                case "2":
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

                case "0":
                    break
                case _:
                    print("Opção inválida.")
