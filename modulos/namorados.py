class ValentineMenuGenerator:
    def __init__(self, recipe_book):
        self.book = recipe_book

    def gerar_combinacao_otima(self, orcamento_maximo, tempo_maximo, criterio_otimizacao="lucro"):
        todas_receitas = self.book.all_recipes()

        entradas = [r for r in todas_receitas if r.dish_class == "entrada"]
        principais = [r for r in todas_receitas if r.dish_class == "principal"]
        sobremesas = [r for r in todas_receitas if r.dish_class == "sobremesa"]

        if criterio_otimizacao == "lucro":
            entradas.sort(key=lambda r: r.profit, reverse=True)
            principais.sort(key=lambda r: r.profit, reverse=True)
            sobremesas.sort(key=lambda r: r.profit, reverse=True)
        else:
            entradas.sort(key=lambda r: r.rating, reverse=True)
            principais.sort(key=lambda r: r.rating, reverse=True)
            sobremesas.sort(key=lambda r: r.rating, reverse=True)

        melhor_menu = None
        melhor_pontuacao = -1.0

        for p in principais:
            if p.cost > orcamento_maximo or p.prep_time > tempo_maximo:
                continue
            for e in entradas:
                if p.cost + e.cost > orcamento_maximo or p.prep_time + e.prep_time > tempo_maximo:
                    continue
                for s in sobremesas:
                    custo_total = e.cost + p.cost + s.cost
                    tempo_total = e.prep_time + p.prep_time + s.prep_time

                    if custo_total > orcamento_maximo or tempo_total > tempo_maximo:
                        continue

                    if criterio_otimizacao == "lucro":
                        pontuacao_atual = e.profit + p.profit + s.profit
                    else:
                        pontuacao_atual = (
                            e.rating + p.rating + s.rating) / 3.0

                    if pontuacao_atual > melhor_pontuacao:
                        melhor_pontuacao = pontuacao_atual
                        melhor_menu = (e, p, s, custo_total, tempo_total)

        return melhor_menu

    def menu_namorados(self):
        while True:
            print("")
            print("Menu dos Dias dos Namorados")
            print("")
            print("1. Gerar Menu (Maximizar Margem de Lucro)")
            print("2. Gerar Menu (Maximizar Experiência / Avaliação)")
            print("0. Voltar")

            op = input("\nEscolha a estratégia comercial: ")

            if op == "0":
                break
            if op not in ["1", "2"]:
                print("Opção inválida.")
                continue

            try:
                orcamento = float(input("Orçamento Máximo Total (Custo R$): "))
                tempo = int(
                    input("Tempo Máximo Tolerável na Cozinha (minutos): "))
            except ValueError:
                print("Erro: Por favor, introduza valores numéricos válidos.")
                continue

            criterio = "lucro" if op == "1" else "avaliacao"
            print("\nProcessando otimização vetorial. Aguarde...")

            resultado = self.gerar_combinacao_otima(orcamento, tempo, criterio)

            if resultado is None:
                print("\n[!] IMPOSSÍVEL MONTAR MENU COM ESTAS RESTRIÇÕES.")
            else:
                ent, prin, sob, custo, tmp = resultado
                venda_total = ent.sale_price + prin.sale_price + sob.sale_price
                lucro_total = ent.profit + prin.profit + sob.profit
                aval_media = (ent.rating + prin.rating + sob.rating) / 3.0

                print("\nMenu Especial Dia dos Namorados:")
                print(f"Entrada: {ent.name} (Custo: R$ {ent.cost:.2f})")
                print(f"Principal: {prin.name} (Custo: R$ {prin.cost:.2f})")
                print(f"Sobremesa: {sob.name} (Custo: R$ {sob.cost:.2f})")
                print("-" * 30)
                print(f"Valor total de venda: R$ {venda_total:.2f}")
                print(f"Custo estimado: R$ {custo:.2f}")
                print(f"Lucro estimado: R$ {lucro_total:.2f}")
                print(f"Tempo total de preparo: {tmp} minutos")
                print(f"Avaliação média: {aval_media:.1f}")

                if tmp > 120 or len(prin.ingredients) > 10:
                    dif = "alta"
                elif tmp > 60:
                    dif = "média"
                else:
                    dif = "baixa"
                print(f"Dificuldade logística: {dif}")
