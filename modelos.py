class Recipe():
    def __init__(self, id, name, category, ingredients, cost, rating):
        self.id = id
        self.name = name
        self.category = category
        self.ingredients = ingredients
        self.cost = cost
        self.rating = rating
        self.ratio_rating_cost = rating / cost if cost > 0 else 0

    def __repr__(self):
        return (
            f"\n Receita: {self.name}\n"
            f" ID: {self.id}\n"
            f" Categoria: {self.category}\n"
            f" Custo: R${self.cost:.2f}\n"
            f" Avaliação: {self.rating}\n"
            f" Razão Avaliação/Custo: {self.ratio_rating_cost:.2f}\n"
        )
