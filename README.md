# Trabalho Prático Final - Algoritmos em Grafos

Este repositório contém a implementação do Trabalho Prático Final para a disciplina **GCC262 - Grafos e suas Aplicações** da Universidade Federal de Lavras, ministrada pelo Prof. Mayron César O. Moreira.

## Autores

- **Tiago de Paula Martins**
- **Samuel Moreira Abreu**

## Introdução

O objetivo deste trabalho é utilizar grafos para modelar problemas logísticos, otimizando o fluxo de bens e serviços.  
**Conceitos principais:**

- **Nós:** Representam intersecções ou esquinas.
- **Arestas:** Representam vias bidirecionais.
- **Arcos:** Representam vias de mão única.

Além de construir o grafo a partir dos dados de entrada, o trabalho exige o cálculo de diversas estatísticas, como:
- Número de vértices, arestas e arcos;
- Densidade do grafo;
- Componentes conectados;
- Grau mínimo e máximo dos vértices;
- Caminho médio, diâmetro e betweenness centrality (intermediação).

## Objetivos do Projeto

- **Modelagem:** Representar o problema utilizando estruturas de dados em grafos.
- **Processamento:** Ler os dados e construir o grafo.
- **Cálculo:** Gerar estatísticas e métricas importantes (Floyd-Warshall para caminhos mínimos, entre outras).
- **Visualização:** Apresentar os resultados de forma interativa via notebook.

## Organização dos Arquivos

- **`graph.py`**  
  Contém toda a lógica para leitura dos dados, construção do grafo e cálculo das estatísticas.

- **`etapa1_grafos.ipynb`**  
  Notebook interativo para:
  - Fazer upload dos dados (instâncias de teste).
  - Importar e utilizar o módulo `graph.py`.
  - Exibir as métricas calculadas e visualizar o grafo (plots e gráficos).

- **`README.md`**  
  Este arquivo, explicando a organização e como executar o projeto.

## Como Executar

### 1. Clonando o Repositório

Abra seu terminal e execute:
```bash
git clone https://github.com/depaulatiago/grafos.git
cd grafos
```

### 2. No Google Colab

- Abra o notebook `etapa1_grafos.ipynb`.
- Faça upload do arquivo `graph.py` e dos dados (.dat) para o ambiente.
- Siga as instruções do notebook para executar o processamento e visualizar os resultados.

### 3. Execução Local

- Certifique-se de ter o Python e as bibliotecas necessárias instaladas.
- Execute o script principal ou abra o notebook para interação.

## Instâncias de Teste

Você pode utilizar as instâncias de teste fornecidas pelo professor ou encontrá-las neste repositório. Também estão disponíveis através deste [link](https://drive.google.com/file/d/1hlBu7L8OBqrwkVRRlFrVOTvBWKnqITxz/view?usp=drive_link).
