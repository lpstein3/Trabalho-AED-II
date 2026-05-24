import json
from random import randint
from modelos import Recipe
from estruturas.trie import TrieTree
from estruturas.hash_table import HashTable


class RecipeBook:
    def __init__(self):
        self.table_by_id = HashTable()
        self.table_by_hash = HashTable()
        self.trie_names = TrieTree()
        self.trie_ingredients = TrieTree()
        self.list_recipes = []
        self._total_loaded = 0
        print("init recipe book")

    def carregar_json(self, path, limit=100) -> int:

        loaded_recipes = 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"[ERRO] Arquivo não encontrado: {path}")
            return 0
        except json.JSONDecodeError as e:
            print(f"[ERRO] JSON inválido: {e}")
            return 0
        for key, info in data.items():
            if loaded_recipes >= limit:
                break

            if not isinstance(info, dict):
                continue

            if "title" not in info or "ingredients" not in info:
                continue

            name = info["title"].strip()
            ingredients = [i.strip() for i in info["ingredients"] if i.strip()]

            if not name or not ingredients:
                continue

            cost = round(len(ingredients) * 5.0, 2)
            if cost <= 0:
                continue

            rating = float(randint(40, 100))
            recipe = Recipe(
                key, name, info.get(
                    "category", "Geral"), ingredients, cost, rating
            )

            self._insert(recipe)
            loaded_recipes += 1

        self._total_loaded = loaded_recipes
        print(
            f"[OK] {loaded_recipes} recipes indexadas em todas as estruturas com sucesso.")
        return loaded_recipes

    def _insert(self, recipe) -> None:
        self.list_recipes.append(recipe)

        self.table_by_id.insert(recipe.id, recipe)
        signature = "|".join(recipe.ingredients)
        existing_ids = self.table_by_hash.search(signature)

        if existing_ids is None:
            self.table_by_hash.insert(signature, [recipe.id])
        else:
            existing_ids.append(recipe.id)

        for name in recipe.name.split():
            self.trie_names.insert(name, recipe.id)
        self.trie_names.insert(recipe.name, recipe.id)

        for ingredient in recipe.ingredients:
            first_word = ingredient.split(
            )[0] if ingredient.split() else ingredient
            self.trie_ingredients.insert(first_word, recipe.id)

    def search_by_id(self, recipe_id: str):
        return self.table_by_id.search(recipe_id)

    def search_by_prefix(self, prefixo: str):
        found_ids = self.trie_names.prefix_search(prefixo)
        single_ids = list(set(found_ids))
        return [self.search_by_id(rid) for rid in single_ids if self.search_by_id(rid)]

    def all_recipes(self):
        return self.list_recipes
