# README – Etapa 1: Pré-processamento dos Dados 🚦🔍

## Trabalho Prático Final – GCC218 / GCC262

**Universidade Federal de Lavras**
Prof. Mayron Cézar O. Moreira

---

## 1. Objetivo da Etapa 1 🎯

A Etapa 1 tem como objetivo realizar o **pré-processamento dos dados** de instâncias de um problema logístico modelado em grafos, preparando a base para as próximas etapas do trabalho. Essa fase compreende:

* 🗺️ Representação do problema com estruturas de dados em grafos;
* 📥 Implementação da leitura de dados das instâncias;
* 📊 Cálculo e apresentação de diversas estatísticas sobre os grafos analisados.

---

## 2. Descrição Formal do Problema 📚

O problema é modelado sobre um **multigrafo** G = (V, E, A), onde:

* **V**: conjunto de nós (interseções, esquinas) 🔵
* **E**: conjunto de arestas (vias bidirecionais) 🟢
* **A**: conjunto de arcos (vias de mão única) 🔴

Serviços (demandas) são requeridos para subconjuntos:

* **VR ⊆ V** (nós requeridos) 🔵
* **ER ⊆ E** (arestas requeridas) 🟢
* **AR ⊆ A** (arcos requeridos) 🔴

O objetivo é, futuramente, resolver o problema de roteamento considerando restrições de capacidade e atendimento de todos os serviços, mas nesta etapa o foco é a modelagem e análise dos dados.

---

## 3. O que foi implementado nesta etapa 🛠️

### 3.1. **Leitura e Modelagem de Instâncias** 📥🗂️

* Leitura dos dados de entrada das instâncias fornecidas pelo professor.
* Estruturas de dados implementadas para representar:

  * Nós, arestas e arcos (com propriedades relevantes: demanda, custo, etc.)
  * Identificação de elementos requeridos (serviços obrigatórios).

### 3.2. **Cálculo de Estatísticas dos Grafos** 📈

Foram implementadas funções para calcular e exibir as seguintes métricas para cada instância:

1. 🔢 Quantidade de vértices (|V|)
2. ➿ Quantidade de arestas (|E|)
3. ➡️ Quantidade de arcos (|A|)
4. 🔵 Quantidade de vértices requeridos (|VR|)
5. 🟢 Quantidade de arestas requeridas (|ER|)
6. 🔴 Quantidade de arcos requeridos (|AR|)
7. 🏗️ Densidade do grafo (order strength)
8. 🔗 Componentes conectados
9. 📉 Grau mínimo dos vértices
10. 📈 Grau máximo dos vértices
11. 🧭 Intermediação (betweenness) de cada nó
12. 🛤️ Caminho médio
13. 📏 Diâmetro do grafo

**Observação:** Muitas dessas estatísticas dependem do cálculo da matriz de caminhos mínimos (matriz de distâncias) e matriz de predecessores, que também foram implementadas.

---

## 4. Como executar 🖥️

1. **Leitura dos arquivos:**

   * Os scripts permitem carregar arquivos de instâncias já presentes em uma pasta padrão (`dados/`).
   * O usuário pode executar o script principal para processar todas as instâncias automaticamente.

2. **Geração das Estatísticas:**

   * Após o processamento, as estatísticas de cada instância são exibidas na tela e/ou gravadas em arquivos de saída conforme o padrão estabelecido.

---

## 5. Estrutura do Repositório 🗃️

* `main.py` ou `notebook.ipynb`: Script principal que executa as etapas de leitura, processamento e geração das estatísticas.
* `grafos.py` (ou similar): Módulos/funções de modelagem de grafos e cálculos de métricas.
* `dados/`: Pasta com as instâncias de entrada.
* `resultados/`: Pasta (opcional) para saída dos relatórios gerados.
* `README.md`: Este arquivo de explicação da etapa.

---

## 6. Regras e Observações 📜

* 🚫 **Proibido** o uso de bibliotecas externas específicas de grafos (`networkx`, `igraph`, etc). Apenas estruturas da biblioteca padrão são permitidas.
* 🧑‍💻 Todo o código é autoral e comentado para facilitar o entendimento.
* 📅 O repositório contém apenas a Etapa 1 neste momento, em conformidade com o cronograma do trabalho.

---

## 7. Créditos 🙋‍♂️🙋‍♀️

Desenvolvido por \[NOME(S) DO(S) AUTOR(ES)] para as disciplinas GCC218 – Algoritmos em Grafos e GCC262 – Grafos e Suas Aplicações, UFLA.

---

### **Resumo das etapas cumpridas:** ✅

* Modelagem do problema via estruturas próprias de grafos;
* Implementação da leitura das instâncias;
* Implementação de algoritmos para cálculo de todas as estatísticas exigidas;
* Teste das funções nas instâncias disponibilizadas.

---