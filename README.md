# Desafio na Cozinha - Sistema Jacquin

**Disciplina:** Algoritmos e Estruturas de Dados II

**Equipe:** Gabriel Schuch e Lucas Stein

---

## Sobre o Projeto

O "Desafio na Cozinha" é um sistema de gestão inteligente de receitas desenvolvido para ajudar o Chef Erick Jacquin a organizar o seu restaurante. O sistema permite pesquisar receitas rapidamente, verificar adulterações culinárias e sugerir cardápios otimizados com base num orçamento estrito.

---

## Estrutura do Projeto

```
Trabalho-AED-II/
│
├── main.py                         # Controlador e ponto de entrada do sistema
├── modelos.py                      # Classe Recipe e formatação de atributos
│
├── modulos/
│   ├── livro_receitas.py           # Módulo 1 — Carregamento e indexação
│   ├── consulta_rapida.py          # Módulo 2/3 — Busca rápida
│   ├── investigacao.py             # Modo Investigação — Integridade
│   ├── chef.py                     # Modo Chef — Recomendação gulosa
│   ├── logistica.py                # Módulo 7 — Operação de Delivery
│   ├── inovacao.py                 # Módulo 8 — Laboratorio de Inovacao
│   ├── namorados.py                # Desafio Extra
│   ├── otimizacao.py               # Módulo 6 — Menu Degustação VIP (PD)
│   └── producao.py                 # Módulo 5 — Dependências e Ciclos
│
├── estruturas/
│   ├── algoritmos/
│   │   ├── buscas.py               # BFS, DFS e Ancestrais
│   │   ├── dijkstra.py
│   │   ├── fluxo.py                # Edmonds-Karp e Corte Mínimo
│   │   ├── kosaraju.py             # Componentes Fortemente Conexos
│   │   ├── kruskal.py
│   │   └── topologico.py           # Ordenação Topológica de Kahn
│   ├── hash_table.py
│   ├── graph.py
│   └── trie.py
│
└── dataset/
    └── recipes_raw_nosource_epi.json  # Base de dados original
```

---

## Fonte de Dados e Adaptações

Utilizámos a base de dados RecipeBox. Como os dados originais não possuíam campos numéricos nativos para o orçamento e avaliação, realizámos a seguinte adaptação matemática durante o carregamento:

- Custo (Peso): Calculado com base na quantidade de ingredientes (R$ 5,00 por ingrediente listado).
- Avaliação (Valor): Gerada aleatoriamente (entre 40 e 100 pontos) para simular a popularidade do prato.
- Categoria: Gerado aleatoriamente( "Breakfast", "Lunch", "Dinner", "Dessert",
  "Appetizer", "Soup", "Salad", "Snack", "Drink")

---

## Estruturas de Dados e Algoritmos Utilizados

**Árvore Trie (Busca Rápida)**: Utilizada para pesquisar receitas de forma quase instantânea através do prefixo do nome (Módulo 2).

**Tabela Hash (Modo Investigação)**: Implementada para detetar adulterações ("sabotagem culinária"), garantindo a integridade dos dados através de identificadores únicos e verificação rápida.

**Algoritmo Guloso (Modo Chef)**: Seleciona a melhor combinação de receitas/ingredientes maximizando a avaliação dentro de um limite financeiro.

**Grafo**: Empregado para modelar tanto a rede de dependências dos preparos na cozinha quanto a malha física de delivery, permitindo calcular sequências de execução ótimas, rotas mais rápidas e gargalos operacionais

**Programacao Dinamica**: Resolve de forma exata o Problema da Mochila 0/1 através de uma abordagem tabular (Bottom-Up), montando o cardápio ótimo que maximiza lucros ou avaliações sob rígidas restrições de tempo ou orçamento.

**Algoritmo de Dijkstra**: Aplicado na malha logística para calcular rapidamente a rota de menor tempo de deslocamento entre as cozinhas e as regiões de destino.

**Edmonds-Karp**: Utilizado para calcular a capacidade máxima de atendimento simultâneo da rede de delivery e identificar arestas saturadas (gargalos operacionais) na operação.

**Algoritmo de kosaraju**: Implementado para detetar Componentes Fortemente Conexos (CFCs) na rede, mapeando eventuais "bolhas logísticas" ou circuitos fechados e isolados de tráfego.

**Algoritmo de Kruskal**: Constrói a Árvore Geradora Mínima (AGM) da rede de transportes, planeando a infraestrutura de rotas mais económica capaz de manter todas as unidades operacionais interligadas.

**Algoritmo de Kahn**: Executa a ordenação topológica no grafo de dependências da cozinha, determinando a sequência correta de produção de cada prato e bloqueando erros (ciclos) no cadastro de preparos intermediários.

---

## Como Executar

Certifique-se de que tem o Python 3.10 ou superior instalado. No terminal, navegue até à diretoria raiz do projeto e execute:

```bash
python main.py
```

---

## [RECUPERAÇÃO P1]

- **Questão da prova escolhida**: Questão 5 sobre algoritmo guloso
- **Explicação da Adicao**: Implementamos as duas mochilas(O/1 e Fracionaria) e fazemos a comparação entre as duas para mostrar o porque o algoritmo guloso não funciona para a mochila 0/1

### Como Testar

1. Execute o sistema:

```bash
python main.py
```

2. No menu principal, escolha a opção `3. Modo Chef`

3. Escolha `1. Menu do Chef (máximo rating)` ou `2. Menu Econômico`

4. Informe um orçamento, por exemplo:

```
Orçamento (R$): 200
```

5. O terminal exibirá a comparação entre os dois algoritmos:

```
 COMPARAÇÃO: 0/1 vs Fracionária

Receitas selecionadas               10           11
Custo total (R$)                185.00       200.00
Rating total                    806.00       858.50
```
