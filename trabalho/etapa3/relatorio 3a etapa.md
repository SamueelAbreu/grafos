# Trabalho Prático Final - Algoritmos em Grafos (GCC218 / GCC262)

**Autores:**
* Samuel Moreira Abreu
* Tiago de Paula Martins

---

## 1. Descrição do Projeto

Este projeto consiste na implementação e otimização de algoritmos para resolver um problema de logística complexo, modelado como uma variação do Problema de Roteamento de Veículos (VRP). O objetivo é encontrar um conjunto de rotas de custo mínimo para uma frota de veículos, partindo de um depósito, para atender a uma série de serviços requeridos (em nós, arestas e arcos de um grafo), respeitando a capacidade de cada veículo.

O desenvolvimento foi dividido em etapas, começando com a modelagem e análise estatística do grafo, passando pela implementação de uma solução construtiva (Etapa 2) e, finalmente, pela aplicação de métodos de melhoria para refinar a qualidade da solução (Etapa 3).

## 2. Estrutura de Arquivos

O projeto está organizado nos seguintes arquivos principais:

* **`etapa_03.ipynb`**: O notebook principal que orquestra todo o processo: carrega os dados, executa os algoritmos e guarda as soluções.
* **`instancia.py`**: Módulo responsável por ler e interpretar os ficheiros de dados (`.dat`) das instâncias.
* **`grafo.py`**: Contém a implementação da classe `CustomGraphFinal`, que representa a estrutura do grafo e inclui métodos para cálculo de estatísticas e de caminhos mínimos.
* **`solucao.py`**: Define as classes `Solucao` e `Rota`, além de conter o algoritmo construtivo (Etapa 2).
* **`otimizacao.py`**: Contém o algoritmo de busca local (Etapa 3) para melhoria da solução.
* **`requirements.txt`**: Lista as dependências Python necessárias para executar o projeto.
* **`dados/`**: Pasta contendo todas as instâncias do problema.
* **`solucoes/`**: Pasta onde as soluções geradas pelo notebook são guardadas.
* **`comparar_solucoes.py`**: Script utilizado para comparar os resultados gerados com as soluções de referência.

## 3. Como Executar

**Configuração Inicial (apenas na primeira vez):**
1.  Garanta que o Python 3.8+ está instalado.
2.  Crie o ficheiro `requirements.txt` na raiz do projeto com o conteúdo abaixo:
    ```text
    pandas
    matplotlib
    jupyterlab
    ```
3.  Abra um terminal na pasta do projeto e instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

**Execução Normal:**
Abra o notebook **`etapa_03.ipynb`** e execute todas as células. O script irá processar todas as instâncias da pasta `dados/` e guardar os resultados na pasta `solucoes/`.

## 4. Evolução Técnica e Otimizações Realizadas

O desenvolvimento partiu de uma base funcional que apresentava sérios problemas de correção e performance. As seguintes alterações foram cruciais para o sucesso do projeto:

### 4.1. Correção do Parser de Instâncias
* **Problema Inicial:** O algoritmo gerava "soluções vazias" (custo e rotas zero) para cerca de 15 instâncias.
* **Diagnóstico:** O diagnóstico revelou uma falha no parser (`instancia.py`), que não processava corretamente as secções de arestas e arcos **não requeridos** (`NrE` e `NrA`). Isso resultava na criação de um grafo desconectado, onde os serviços eram inalcançáveis a partir do depósito.
* **Solução:** O parser foi totalmente reescrito para ser mais robusto, identificando explicitamente cada seção do ficheiro de dados e garantindo que o grafo fosse construído com todas as suas conexões.

### 4.2. Otimização do Cálculo de Caminhos Mínimos (Etapa 1)
* **Problema Inicial:** O algoritmo era extremamente lento em ficheiros grandes, chegando a travar ou demorar horas.
* **Diagnóstico:** O "gargalo" era o uso do algoritmo de **Floyd-Warshall**, com complexidade de tempo **O(V³)**, que se mostrou inviável para grafos com centenas de vértices.
* **Solução:** Substituímos o Floyd-Warshall pela execução do **algoritmo de Dijkstra a partir de cada nó**. Para os grafos esparsos do problema, a complexidade **O(V * E * log V)** é ordens de magnitude mais eficiente, resultando numa redução drástica do tempo de processamento de horas para poucos minutos.

### 4.3. Refatoração dos Algoritmos de Solução (Etapas 2 e 3)

#### Solução Construtiva (Etapa 2)
* **Problema:** O algoritmo construtivo original (baseado em Savings) era complexo e continha bugs de implementação que dificultavam a depuração.
* **Solução:** Para garantir uma base de comparação funcional e robusta, implementámos um algoritmo construtivo mais simples do tipo **"Vizinho Mais Próximo Guloso"**. Ele rapidamente gera uma solução inicial válida, que serve como um ponto de partida para a fase de melhoria.

#### Algoritmo de Melhoria (Etapa 3)
* **Problema:** A busca local inicialmente idealizada, com movimento de `swap`, era muito lenta devido ao uso excessivo de `copy.deepcopy()` e ao recálculo completo do custo da rota a cada tentativa de troca.
* **Solução (Otimização Chave):** A função foi otimizada de duas formas:
    1.  **Eliminação de Cópias:** Removemos o `deepcopy()` de dentro do loop principal, evitando a criação de cópias desnecessárias e de alto custo computacional.
    2.  **Implementação da "Avaliação Delta":** Em vez de recalcular o custo total da rota, passámos a calcular apenas a *diferença* de custo (`delta`) que uma troca causaria. Isto reduziu a complexidade da avaliação de cada movimento de `O(N)` para `O(1)`, resultando num ganho de velocidade massivo.

## 5. Análise dos Resultados Finais

Após todas as otimizações, o algoritmo final apresenta um *trade-off* (relação de troca) claro e interessante:

* **Desempenho de Execução (-99.91%):** O nosso algoritmo final é **extraordinariamente rápido**(calculos realizados no algoritmo g.py, na pasta 'Comparativo'), resolvendo todas as instâncias numa pequena fração do tempo da solução de referência. O objetivo de lidar com ficheiros grandes foi um sucesso.
* **Qualidade da Solução (+123.28%):** Em contrapartida, o **custo médio** das nossas soluções é mais que o dobro do custo das soluções de referência. Isto indica que as nossas heurísticas (Vizinho Mais Próximo + Swap) são muito "gulosas" e simples, ficando presas em ótimos locais de baixa qualidade.

## 6. Metodologia de Desenvolvimento e Depuração

No início da Etapa 3, o projeto enfrentava desafios críticos: a falha em processar todas as instâncias e um tempo de execução que chegava a quase **4 horas**, o que impossibilitava a conclusão do trabalho a tempo, considerando as nossas outras responsabilidades como trabalho e estágio.

Isto levou-nos a realizar uma reavaliação completa do trabalho desenvolvido, partindo do zero para uma análise forense dos erros. Ficámos desapontados com a falta de atenção que tivemos nas etapas iniciais, principalmente ao não corrigir o problema da leitura dos dados logo na Etapa 2.

Para a depuração, adotamos uma metodologia mista. Inicialmente, utilizámos ferramentas de IA (Gemini, ChatGPT) para auxiliar na identificação de "gargalos" de performance e bugs lógicos. Elas foram úteis para apontar possíveis áreas problemáticas, mas percebemos que as suas sugestões de código, em muitos casos, adicionavam uma complexidade desnecessária ou não se integravam bem à nossa base de código.

Por essa razão, o nosso método principal de depuração focou-se em técnicas tradicionais e controladas: múltiplos **testes de mesa** e a análise cuidadosa da lógica passo a passo. Foi através desta análise manual que identificámos a causa raiz da lentidão: o uso indiscriminado de `deepcopy()` dentro da nossa busca local.

Diante do prazo, tomámos uma decisão estratégica: **priorizar a otimização do tempo de execução em detrimento da qualidade do custo**. Esta abordagem forçou-nos a corrigir a falha fundamental do nosso parser e a otimizar os algoritmos.

No final, após fazer todos esses passos, tivemos um algoritmo completo e mais legivel, estruturado, funcional e rápido, que foi o nosso principal objetivo para essa etapa.

