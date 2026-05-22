import json
from random import randint
from pathlib import Path
from modelos import Receita

ROOT_DIR = Path(__file__).resolve().parent

DATASET_PATH = ROOT_DIR / "dataset" / "recipes_raw_nosource_epi.json"


def carregar_dados(limite=100):
    receitas = []
    try:
        with open(DATASET_PATH, 'r', encoding='utf-8')as file:
            dados = json.load(file)

            for key, info in dados.items():
                if not isinstance(info, dict) or 'title' not in info or 'ingredients' not in info:
                    continue

                nome = info.get('title', 'Sem nome').strip()
                ingredientes = info.get('ingredients', [])

                custo = len(ingredientes) * 5.0

                avaliacao = randint(40, 100)

                if custo <= 0:
                    continue

                receita = Receita(id=key, nome=nome, categoria="Geral",
                                  ingredientes=ingredientes, custo=custo, avaliacao=avaliacao)

                receitas.append(receita)

                if len(receitas) >= limite:
                    break
        print(
            f"[Sucesso] {len(receitas)} receitas carregadas e adaptadas do RecipeBox.")

    except FileNotFoundError:
        print(f"[Erro] O arquivo {DATASET_PATH} não foi encontrado.")

    return receitas


def main():
    print("=== DESAFIO NA COZINHA - SISTEMA JACQUIN ===")
    receitas = carregar_dados()

    while True:
        print("\nMenu Principal:")
        print("1. Buscar Receitas (Árvore Trie - A fazer)")
        print("2. Investigar Sabotagem (Tabela Hash - A fazer)")
        print("3. Modo Chef / Desafio do Orçamento (Algoritmo Guloso)")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            print("Módulo de busca ainda não implementado.")
            for i in receitas:
                print(i)
        elif opcao == '2':
            print("Módulo de investigação ainda não implementado.")
        elif opcao == '3':
            print("\n--- Iniciando o Desafio do Orçamento (Mochila) ---")
            # Aqui chamaremos a função da sua recuperação!
            print("Em breve...")
        elif opcao == '0':
            print("Au revoir!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
