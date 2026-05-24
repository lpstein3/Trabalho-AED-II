from pathlib import Path
from modulos.livro_receitas import RecipeBook
from modulos.consulta_rapida import QuickSearch
from modulos.investigacao import Investigation
from modulos.chef import Chef

ROOT_DIR = Path(__file__).resolve().parent

DATASET_PATH = ROOT_DIR / "dataset" / "recipes_raw_nosource_epi.json"


def menu_principal():
    print("Menu Principal")
    print("1. Modo Consulta Rapida")
    print("2. Modo Investigação")
    print("3. Modo Chef ")
    print("0. Sair")
    return input("Escolha uma opção: ")


def main():
    book = RecipeBook()

    book.carregar_json(DATASET_PATH)
    quick_search = QuickSearch(book)
    investigation = Investigation(book)
    chef = Chef(book)

    # 3. Loop do Menu
    while True:
        opcao = menu_principal()

        match opcao:
            case "1":
                quick_search.menu_quick_search()
            case "2":
                investigation.menu_investigation()
            case "3":
                chef.menu_chef()
            case "0":
                print("Saindo...")
                break


if __name__ == "__main__":
    main()
