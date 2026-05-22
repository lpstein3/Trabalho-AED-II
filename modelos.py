class Receita():
    def __init__(self, id, nome, categoria, ingredientes, custo, avaliacao):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.ingredientes = ingredientes
        self.custo = custo  # Sera o peso da mochila
        self.avaliacao = avaliacao  # sera o valor da mochila

        self.razao_valor_custo = avaliacao / custo if custo > 0 else 0

    def __repr__(self):
        return f"{self.nome} | Custo: R${self.custo:.2f} | Avaliação: {self.avaliacao} | Razão: {self.razao_valor_custo:.2f}"
