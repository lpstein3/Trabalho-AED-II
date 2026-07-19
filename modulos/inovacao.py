import random
from estruturas.algoritmos.dijkstra import dijkstra, shortest_path


class InnovationLab:
    def __init__(self, logistics_network):
        self.network = logistics_network
        self.time_graph = logistics_network.time_graph

    def gerar_rota_entregas_tsp(self, origem, destinos):
        rota_completa = [origem]
        nao_visitados = set(destinos)
        tempo_total = 0
        atual = origem

        while nao_visitados:
            distancias, _ = dijkstra(self.time_graph, atual)

            proximo_destino = None
            menor_tempo = float('inf')

            for destino in nao_visitados:
                tempo = distancias.get(destino, float('inf'))
                if tempo < menor_tempo:
                    menor_tempo = tempo
                    proximo_destino = destino

            if proximo_destino is None or menor_tempo == float('inf'):
                return None, float('inf')

            caminho_passo_a_passo, _ = shortest_path(
                self.time_graph, atual, proximo_destino)
            if caminho_passo_a_passo:
                rota_completa.extend(caminho_passo_a_passo[1:])

            tempo_total += menor_tempo
            nao_visitados.remove(proximo_destino)
            atual = proximo_destino

        distancias_finais, _ = dijkstra(self.time_graph, atual)
        tempo_retorno = distancias_finais.get(origem, float('inf'))

        if tempo_retorno == float('inf'):
            return None, float('inf')

        caminho_retorno, _ = shortest_path(self.time_graph, atual, origem)
        if caminho_retorno:
            rota_completa.extend(caminho_retorno[1:])

        tempo_total += tempo_retorno
        return rota_completa, tempo_total

    def menu_inovacao(self):
        while True:
            print("")
            print("Laboratorio de Inovacao do Chef")
            print("")
            print("1. Gerar Rota Otimizada de Entregas Múltiplas")
            print("0. Voltar")

            op = input("\nEscolha a operação: ")
            match op:
                case "1":
                    origem = input(
                        f"Informe a Cozinha de origem (ex: {self.network.kitchens[0]}): ").strip()
                    if origem not in self.network.time_graph.vertices():
                        print("Cozinha não encontrada. Verifique o nome digitado.")
                        continue

                    regioes_entrega = random.sample(self.network.regions, 5)
                    print(
                        f"\n[Pedidos Recebidos] O entregador deve passar por: {', '.join(regioes_entrega)}")
                    print("Calculando a rota logística mais rápida...")

                    rota, tempo = self.gerar_rota_entregas_tsp(
                        origem, regioes_entrega)

                    if rota is None or tempo == float('inf'):
                        print(
                            "\n[!] Não foi possível estabelecer um circuito fechado viável.")
                    else:
                        print("\nRota de entregas multiplas feito:")
                        caminho_str = " -> ".join(rota)
                        print(f"Caminho: {caminho_str}")
                        print(f"Tempo Total Estimado: {tempo} minutos")
                case "0":
                    break
                case _:
                    print("Opção inválida.")
