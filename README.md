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
├── main.py                         # Ponto de entrada do sistema
├── modelos.py                      # Classe Recipe
│
├── modulos/
│   ├── livro_receitas.py           # Módulo 1 — Carregamento e indexação
│   ├── consulta_rapida.py          # Módulo 2/3 — Busca rápida
│   ├── investigacao.py             # Modo Investigação — Integridade
│   └── chef.py                     # Modo Chef — Recomendação gulosa
│
├── estruturas/
│   ├── hash_table.py               
│   └── trie.py                     
│
└── dataset/
    └── recipes_raw_nosource_epi.json  # Dataset de receitas 
```

---

## Fonte de Dados e Adaptações

Utilizámos a base de dados RecipeBox (especificamente o ficheiro proveniente do site Epicurious, focado em receitas mais sofisticadas). Como os dados originais não possuíam campos numéricos nativos para o orçamento e avaliação, realizámos a seguinte adaptação matemática durante o carregamento:

- Custo (Peso): Calculado com base na quantidade de ingredientes (R$ 5,00 por ingrediente listado).
- Avaliação (Valor): Gerada aleatoriamente (entre 40 e 100 pontos) para simular a popularidade do prato.
- Categoria: Gerado aleatoriamente( "Breakfast", "Lunch", "Dinner", "Dessert",
  "Appetizer", "Soup", "Salad", "Snack", "Drink")

---

## Estruturas de Dados Utilizadas

Árvore Trie (Busca Rápida): Utilizada para pesquisar receitas de forma quase instantânea através do prefixo do nome (Módulo 2).

Tabela Hash (Modo Investigação): Implementada para detetar adulterações ("sabotagem culinária"), garantindo a integridade dos dados através de identificadores únicos e verificação rápida.

Algoritmo Guloso (Modo Chef): Seleciona a melhor combinação de receitas/ingredientes maximizando a avaliação dentro de um limite financeiro.

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
