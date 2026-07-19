from modulos.chef import Chef
from modulos.investigacao import Investigation
from modulos.consulta_rapida import QuickSearch
from modulos.otimizacao import MenuOptimizer
from modulos.logistica import LogisticsNetwork
from modulos.producao import ProductionWorkshop
from modulos.inovacao import InnovationLab
from modulos.livro_receitas import RecipeBook
from pathlib import Path
from modulos.namorados import ValentineMenuGenerator

ROOT_DIR = Path(__file__).resolve().parent
DATASET_PATH = ROOT_DIR / "dataset" / "recipes_raw_nosource_epi.json"
LOAD_LIMIT = 3000


def exibir_menu_principal():
    print("")
    print("        SISTEMA DE GESTÃO - DESAFIO NA COZINHA         ")
    print("   [FUNCIONALIDADES DO TRABALHO 1 ]")
    print("1. Modo Consulta Rápida (Tabela Hash e Árvore Trie)")
    print("2. Modo Auditoria de Dados (Análise de Hashes/Colisões)")
    print("3. Modo Recomendação Básica (Algoritmos Gulosos)")
    print('')
    print("   [FUNCIONALIDADES DO TRABALHO 2]")
    print("4. Modo Oficina de Produção (Módulo 5)")
    print("5. Modo Logística e Delivery (Módulo 7)")
    print("6. Modo Otimização de Menu VIP (Módulo 6)")
    print("7. Módulo de Inovação: Caixeiro Viajante (Módulo 8)")
    print("8. Desafio Extra: Menu Dia dos Namorados")
    print('')
    print("0. Encerrar Sistema")
    print('')


def modo_consulta_rapida(quick_search: QuickSearch):
    quick_search.menu_quick_search()


def modo_auditoria(investigation: Investigation):
    while True:
        print("\n Investigacao de Dados (T1) ")
        print("1. Verificar alterações não autorizadas (Hashes)")
        print("2. Procurar duplicidades no sistema")
        print("3. Procurar conflitos de ID")
        print("4. Verificar integridade dos campos numéricos")
        print("5. Gerar Relatório Completo")
        print("0. Voltar")
        op = input("Escolha uma opção: ")
        match op:
            case "1":
                results = investigation.check_alterations()
                print(f"\n{len(results)} receita(s) alterada(s).")
                for r in results:
                    print(f"    {r['id']} | {r['name']} -> {r['problem']}")
            case "2":
                results = investigation.check_duplicates()
                print(f"\n{len(results)} duplicata(s) encontrada(s).")
                for r in results:
                    print(
                        f"    {r['id_a']} <-> {r['id_b']} | {r['name']} -> {r['problem']}")
            case "3":
                results = investigation.check_conflicts()
                print(f"\n{len(results)} conflito(s) encontrado(s).")
                for r in results:
                    print(
                        f"    {r['id_a']} <-> {r['id_b']} | {r['name']} -> {r['problem']}")
            case "4":
                results = investigation.check_integrity()
                print(f"\n{len(results)} receita(s) com campo(s) inválido(s).")
                for r in results:
                    print(f"    {r['id']} | {r['name']} -> {r['problem']}")
            case "5":
                investigation.full_report()
            case "0":
                break
            case _:
                print("Opção inválida.")


def modo_recomendacao_basica(chef_module: Chef):
    chef_module.menu_chef()


def modo_producao(workshop: ProductionWorkshop):
    workshop.menu_producao()


def modo_logistica(logistics: LogisticsNetwork):
    logistics.menu_logistica()


def modo_otimizacao_vip(optimizer: MenuOptimizer):
    optimizer.menu_otimizacao()


def modo_inovacao(logistics: LogisticsNetwork):
    lab = InnovationLab(logistics)
    lab.menu_inovacao()


def modo_namorados(book: RecipeBook):
    generator = ValentineMenuGenerator(book)
    generator.menu_namorados()


def main():
    book = RecipeBook()
    try:
        book.carregar_json(DATASET_PATH, LOAD_LIMIT)
    except FileNotFoundError:
        print(f"ERRO: Arquivo JSON não encontrado em '{DATASET_PATH}'.")
        print("Verifique se a pasta 'dataset' está no mesmo diretório do main.py.")
        return

    quick_search = QuickSearch(book)
    investigation = Investigation(book)
    chef_module = Chef(book)
    workshop = ProductionWorkshop(book)
    logistics = LogisticsNetwork(book)
    optimizer = MenuOptimizer(book)

    while True:
        exibir_menu_principal()
        opcao = input("Selecione o modo de operação: ").strip()
        match opcao:
            case "1":
                modo_consulta_rapida(quick_search)
            case "2":
                modo_auditoria(investigation)
            case "3":
                modo_recomendacao_basica(chef_module)
            case "4":
                modo_producao(workshop)
            case "5":
                modo_logistica(logistics)
            case "6":
                modo_otimizacao_vip(optimizer)
            case "7":
                modo_inovacao(logistics)
            case "8":
                modo_namorados(book)
            case "0":
                print("\nEncerrando o sistema de gestão. Operação concluída.")
                break
            case _:
                print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
