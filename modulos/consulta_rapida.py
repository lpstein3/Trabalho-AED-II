from modulos.livro_receitas import RecipeBook


class QuickSearch:
    def __init__(self, recipe_book: RecipeBook):
        self.book = recipe_book

    # ==================================================
    # BUSCA POR ID
    # ==================================================
    def by_id(self, recipe_id):
        result = self.book.search_by_id(recipe_id)
        if result is None:
            print(f"[AVISO] Nenhuma receita com ID '{recipe_id}'.")
            return None
        return result

    # ==================================================
    # BUSCA POR PREFIXO (Total ou parcial)
    # ==================================================
    def by_name(self, query: str) -> list:
        results = self.book.search_by_prefix(query.strip())
        if not results:
            print(f"[AVISO] Nenhuma receita com nome '{query}'.")
        return results

    # ==================================================
    # BUSCA POR INGREDIENTE
    # ==================================================
    def by_ingredient(self, ingredient: str) -> list:
        results = self.book.search_by_ingredient(ingredient.strip().lower())
        if not results:
            print(f"[AVISO] Nenhuma receita com ingrediente '{ingredient}'.")
        return results

    # ==================================================
    # BUSCA POR CATEGORIA
    # ==================================================
    def by_category(self, category: str) -> list:
        category = category.strip().lower()
        results = [
            r for r in self.book.all_recipes()
            if r.category.strip().lower() == category
        ]
        if not results:
            print(f"[AVISO] Nenhuma receita na categoria '{category}'.")
        return results

    # ==================================================
    # MENU DA CONSULTA RAPIDA
    # ==================================================
    def menu_quick_search(self):
        while True:
            print("\n Modo Consulta Rapida")
            print("1. Por ID.")
            print("2. Por Nome (prefixo).")
            print("3. Por ingrediente.")
            print("4. Por categoria.")
            print("0. Sair")

            op = input("Qual Consulta quer fazer? ")

            match op:
                case "1":
                    recipe_id = input("Digite o ID da receita: ")
                    print(self.by_id(recipe_id))

                case "2":
                    recipe_name = input("Digite o nome (prefixo) da receita: ")
                    print(self.by_name(recipe_name))

                case "3":
                    recipe_ingredient = input("Digite o nome do ingrediente: ")
                    print(self.by_ingredient(recipe_ingredient))

                case "4":
                    recipe_category = input("Digite o nome da categoria: ")
                    print(self.by_category(recipe_category))

                case "0":
                    print("Saindo da consulta rápida...\n")
                    break

                case _:
                    print("[AVISO] Opção inválida. Tente novamente.")
