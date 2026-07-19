DISH_CLASS_BY_CATEGORY = {
    "Appetizer": "entrada",
    "Soup": "entrada",
    "Salad": "entrada",
    "Snack": "entrada",
    "Breakfast": "principal",
    "Lunch": "principal",
    "Dinner": "principal",
    "Dessert": "sobremesa",
    "Drink": "bebida"
}

BASE_PREP_KEYWORDS = [
    "sauce", "dough", "stock", "broth", "base", "glaze",
    "batter", "marinade", "dressing", "filling", "crust",
    "syrup", "compote", "custard"
]


class Recipe():
    def __init__(self, id, name, category, ingredients, cost, rating):
        self.id = id
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.cost = cost
        self.rating = rating
        self.ratio_rating_cost = rating / cost if cost > 0 else 0

        seed = sum(ord(c) for c in str(id))
        self.prep_time = 10 + (len(ingredients) * 3 + seed) % 80
        self.popularity = round((rating * 0.6 + (seed % 40) * 1.0) % 100, 1)

        RARE_HINTS = ["truffle", "caviar", "saffron", "foie gras", "wagyu",
                      "lobster", "morel", "wild mushroom", "vanilla bean"]
        self.rare_ingredients = [
            ing for ing in ingredients
            if any(hint in ing.lower() for hint in RARE_HINTS)
        ]
        self.rare_ingredient_count = len(self.rare_ingredients)

        complexity_score = len(ingredients) + self.prep_time / 10
        if complexity_score < 12:
            self.logistics_difficulty = "baixa"
        elif complexity_score < 20:
            self.logistics_difficulty = "média"
        else:
            self.logistics_difficulty = "alta"

        self.team_required = 1 + (len(ingredients) // 8)
        self.dish_class = DISH_CLASS_BY_CATEGORY.get(category, "principal")
        name_lower = name.lower()
        self.is_base_prep = any(k in name_lower for k in BASE_PREP_KEYWORDS)

        self.sale_price = round(cost * 1.8 + rating * 0.5, 2)
        self.profit = round(self.sale_price - cost, 2)

    def __repr__(self):
        return (
            f"\n Receita: {self.name}\n"
            f" ID: {self.id}\n"
            f" Categoria: {self.category} ({self.dish_class})\n"
            f" Custo: R${self.cost:.2f} | Venda: R${self.sale_price:.2f} | Lucro: R${self.profit:.2f}\n"
            f" Avaliação: {self.rating} | Popularidade: {self.popularity}\n"
            f" Tempo de preparo: {self.prep_time} min | Dificuldade logística: {self.logistics_difficulty}\n"
            f" Ingredientes raros: {self.rare_ingredient_count} | Equipe necessária: {self.team_required}\n"
            f" Razão Avaliação/Custo: {self.ratio_rating_cost:.2f}\n"
        )
