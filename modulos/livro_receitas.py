from modulos.investigacao import generate_signature
from estruturas.hash_table import HashTable
from estruturas.trie import TrieTree
from modelos import Recipe
from random import randint, choice
import json

CATEGORIES = [
    "Breakfast", "Lunch", "Dinner", "Dessert",
    "Appetizer", "Soup", "Salad", "Snack", "Drink"
]


class RecipeBook:
    def __init__(self):
        self.table_by_id = HashTable()
        self.trie_names = TrieTree()
        self.trie_ingredients = TrieTree()
        self.list_recipes = []

    def carregar_json(self, path, limit=100):
        loaded_recipes = 0

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {path}")
            return 0
        except json.JSONDecodeError as e:
            print(f"JSON inválido: {e}")
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
            rating = float(randint(40, 100))
            category = info.get("category") or choice(CATEGORIES)

            recipe = Recipe(key, name, category, ingredients, cost, rating)
            self._insert(recipe)
            loaded_recipes += 1

        print(f"{loaded_recipes} receitas carregadas.")
        return loaded_recipes

    def _insert(self, recipe):
        self.list_recipes.append(recipe)
        self.table_by_id.insert(recipe.id, recipe)

        # indexa cada palavra do nome separadamente e o nome completo
        for word in recipe.name.split():
            self.trie_names.insert(word, recipe.id)
        self.trie_names.insert(recipe.name, recipe.id)

        # indexa cada palavra de cada ingrediente e o ingrediente completo
        for ingredient in recipe.ingredients:
            for word in ingredient.split():
                self.trie_ingredients.insert(word.lower(), recipe.id)
            self.trie_ingredients.insert(ingredient.lower(), recipe.id)

    def search_by_id(self, recipe_id):
        return self.table_by_id.search(recipe_id)

    def search_by_prefix(self, prefix):
        found_ids = self.trie_names.prefix_search(prefix)
        unique_ids = list(set(found_ids))
        return [self.search_by_id(rid) for rid in unique_ids if self.search_by_id(rid)]

    def search_by_ingredient(self, ingredient):
        found_ids = self.trie_ingredients.prefix_search(ingredient.lower())
        unique_ids = list(set(found_ids))
        return [self.search_by_id(rid) for rid in unique_ids if self.search_by_id(rid)]

    def all_recipes(self):
        return self.list_recipes
