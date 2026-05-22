# Desafio na Cozinha - Sistema Jacquin

**Disciplina:** Algoritmos e Estruturas de Dados II
**Equipa:** Gabriel Schuch e Lucas Stein

## Sobre o Projeto

O "Desafio na Cozinha" é um sistema de gestão inteligente de receitas desenvolvido para ajudar o Chef Erick Jacquin a organizar o seu restaurante. O sistema permite pesquisar receitas rapidamente, verificar adulterações culinárias e sugerir cardápios otimizados com base num orçamento estrito.

## Estrutura do Projeto

## Fonte de Dados e Adaptações

Utilizámos a base de dados RecipeBox (especificamente o ficheiro proveniente do site Epicurious, focado em receitas mais sofisticadas). Como os dados originais não possuíam campos numéricos nativos para o orçamento e avaliação, realizámos a seguinte adaptação matemática durante o carregamento:

- Custo (Peso): Calculado com base na quantidade de ingredientes (R$ 5,00 por ingrediente listado).
- Avaliação (Valor): Gerada aleatoriamente (entre 40 e 100 pontos) para simular a popularidade do prato.

## Estruturas de Dados Utilizadas

Árvore Trie (Busca Rápida): Utilizada para pesquisar receitas de forma quase instantânea através do prefixo do nome (Módulo 2).

Tabela Hash (Modo Investigação): Implementada para detetar adulterações ("sabotagem culinária"), garantindo a integridade dos dados através de identificadores únicos e verificação rápida.

Algoritmo Guloso (Modo Chef): Seleciona a melhor combinação de receitas/ingredientes maximizando a avaliação dentro de um limite financeiro.

## Como Executar

Certifique-se de que tem o Python 3 instalado. No terminal, navegue até à diretoria raiz do projeto e execute:

```bash
python main.py
```
