from modulos.livro_receitas import RecipeBook


class QuickSearch:
    def __init__(self, recipe_book: RecipeBook):
        self.book = recipe_book

    def by_id(self, recipe_id):
        result = self.book.search_by_id(recipe_id)
        if result is None:
            print(f"Nenhuma receita encontrada com ID '{recipe_id}'.")
            return None
        return result

    def by_name(self, query: str) -> list:
        results = self.book.search_by_prefix(query.strip())
        if not results:
            print(f"Nenhuma receita encontrada com o nome '{query}'.")
        return results

    def by_ingredient(self, ingredient: str) -> list:
        results = self.book.search_by_ingredient(ingredient.strip().lower())
        if not results:
            print(
                f"Nenhuma receita encontrada com o ingrediente '{ingredient}'.")
        return results

    def by_category(self, category: str) -> list:
        category = category.strip().lower()
        results = [
            r for r in self.book.all_recipes()
            if r.category.strip().lower() == category
        ]
        if not results:
            print(f"Nenhuma receita encontrada na categoria '{category}'.")
        return results

    def menu_quick_search(self):
        while True:
            print("\n Consulta Rápida")
            print("1. Por ID")
            print("2. Por nome (prefixo)")
            print("3. Por ingrediente")
            print("4. Por categoria")
            print("0. Voltar")

            op = input("O que quer buscar? ")

            match op:
                case "1":
                    recipe_id = input("ID da receita: ")
                    print(self.by_id(recipe_id))

                case "2":
                    recipe_name = input("Nome (ou prefixo): ")
                    print(self.by_name(recipe_name))

                case "3":
                    recipe_ingredient = input("Nome do ingrediente: ")
                    print(self.by_ingredient(recipe_ingredient))

                case "4":
                    recipe_category = input("Nome da categoria: ")
                    print(self.by_category(recipe_category))

                case "0":
                    break

                case _:
                    print("Opção inválida.")
