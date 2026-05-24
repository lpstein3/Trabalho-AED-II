from pathlib import Path
from modulos.livro_receitas import RecipeBook

ROOT_DIR = Path(__file__).resolve().parent

DATASET_PATH = ROOT_DIR / "dataset" / "recipes_raw_nosource_epi.json"


def menu_principal():
    print("\n--- 👨‍🍳 DESAFIO NA COZINHA: SISTEMA JACQUIN ---")
    print("1. Consultar Receitas (Busca Rápida)")
    print("2. Investigar Sabotagem (Auditoria)")
    print("3. Modo Chef (Otimização de Menu - Guloso)")
    print("0. Sair")
    return input("Escolha uma opção: ")


def main():
    book = RecipeBook()

    book.carregar_json(DATASET_PATH)

    # 3. Loop do Menu
    while True:
        opcao = menu_principal()

        if opcao == "1":
            prefix = input("Digite o prefixo do nome da receita: ")
            results = book.search_by_prefix(prefix)
            print(f"Receitas encontradas: {[r.name for r in results]}")

        elif opcao == "2":
            # Aqui chamará o seu módulo de investigação
            print("Funcionalidade de investigação em construção...")

        elif opcao == "3":
            # Aqui chamará o seu módulo de recuperação da P1
            orcamento = float(input("Defina o orçamento para o menu: "))
            # executar_desafio_guloso(livro, orcamento)
            print(f"Executando otimização com orçamento R${orcamento}...")

        elif opcao == "0":
            print("Au revoir! O Chef agradece a dedicação.")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()
