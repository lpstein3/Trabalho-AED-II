class Recipe():
    def __init__(self, id, name, category, ingredients, cost, rating):
        self.id = id
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.cost = cost  # Sera o peso da mochila
        self.rating = rating  # sera o valor da mochila

        self.ratio_rating_cost = rating / cost if cost > 0 else 0

    def __repr__(self):
        return f"{self.Name} | Custo: R${self.custo:.2f} | Avaliação: {self.rating} | Razão: {self.ratio_rating_cost:.2f}"
