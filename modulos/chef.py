
from modulos.livro_receitas import RecipeBook


# ==================================================
# 0/1 GULOSO (do seu colega, sem alteração)
# ==================================================
def recommend_menu(recipes, budget):
    """Algoritmo guloso 0/1 — só pega receitas inteiras."""
    ordered = sorted(
        recipes,
        key=lambda r: r.ratio_rating_cost,
        reverse=True
    )
    selected = []
    total_cost = 0

    for recipe in ordered:
        if total_cost + recipe.cost <= budget:
            selected.append(recipe)
            total_cost += recipe.cost

    return selected, total_cost


# ==================================================
# FRACIONÁRIA
# ==================================================
def fractional_knapsack(recipes, budget):
    '''
        Algoritmo guloso fracionário - coleta ate acabar o orçamentos
    '''
    ordered = sorted(
        recipes,
        key=lambda r: r.ratio_rating_cost,
        reverse=True
    )
    selected = []
    total_cost = 0.0

    for recipe in ordered:
        if total_cost >= budget:
            break

        remaining = budget - total_cost

        if recipe.cost <= remaining:
            selected.append((recipe, 1.0))
            total_cost += recipe.cost
        else:
            fraction = remaining / recipe.cost
            selected.append((recipe, round(fraction, 2)))
            total_cost += remaining
            break

    return selected, round(total_cost, 2)


# ==================================================
# COMPARAÇÃO
# ==================================================
def compare_algorithms(recipes, budget):
    """Faz a comparacao entre a mochila 0/1 com a fracionaria e printa todos as receitas que foram escolhidas"""
    zero_one, cost_01 = recommend_menu(recipes, budget)
    fractional, cost_frac = fractional_knapsack(recipes, budget)

    rating_01 = sum(r.rating for r in zero_one)
    rating_frac = sum(r.rating * f for r, f in fractional)

    print(" COMPARAÇÃO: 0/1 vs Fracionária\n")
    print(f"{'Receitas selecionadas':<25} {len(zero_one):>12} {len(fractional):>12}")
    print(f"{'Custo total (R$)':<25} {cost_01:>12.2f} {cost_frac:>12.2f}")
    print(f"{'Rating total':<25} {rating_01:>12.2f} {rating_frac:>12.2f}")

    print("\n[0/1] Receitas:")
    for r in zero_one:
        print(f"  • {r.name:<30} R${r.cost:>7.2f}  rating: {r.rating:>6.2f}")

    print("\n[Fracionária] Receitas:")
    for r, f in fractional:
        frac_str = f"({f*100:.0f}%)" if f < 1.0 else ""
        print(
            f"  • {r.name:<30} R${r.cost*f:>7.2f}  rating: {r.rating*f:>6.2f}  {frac_str}")

    diff = round(rating_frac - rating_01, 2)
    print(f"\n[Diferença] Fracionária entrega {diff} pontos a mais de rating.")


# ==================================================
# CLASSE CHEF
# ==================================================
class Chef:
    def __init__(self, recipe_book: RecipeBook):
        self.book = recipe_book

    def _get_recipes(self, min_rating=0.0):
        """Filtra receitas por rating mínimo."""
        return [
            r for r in self.book.all_recipes()
            if r.cost > 0
            and r.rating >= min_rating]

    # ==================================================
    # MENU DO CHEF (máximo rating)
    # ==================================================
    def chef_menu(self, budget):
        recipes = self._get_recipes()
        if not recipes:
            print("[AVISO] Nenhuma receita disponível.")
            return
        compare_algorithms(recipes, budget)

    # ==================================================
    # MENU ECONÔMICO (rating >= 60)
    # ==================================================
    def economic_menu(self, budget):
        recipes = self._get_recipes(min_rating=60.0)
        if not recipes:
            print("[AVISO] Nenhuma receita com rating >= 60.")
            return
        compare_algorithms(recipes, budget)

    # ==================================================
    # MENU INTERATIVO
    # ==================================================
    def menu_chef(self):
        while True:
            print("\n Modo Chef")
            print("1. Menu do Chef (máximo rating).")
            print("2. Menu econômico (rating >= 60).")
            print("0. Sair")

            op = input("Escolha uma opção: ")

            match op:
                case "1":
                    budget = float(input("Orçamento (R$): "))
                    self.chef_menu(budget)

                case "2":
                    budget = float(input("Orçamento (R$): "))
                    self.economic_menu(budget)

                case "0":
                    print("Saindo do modo Chef...\n")
                    break

                case _:
                    print("[AVISO] Opção inválida.")
