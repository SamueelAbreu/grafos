
# README – Etapa 2: Solução Inicial 🚚🛣️

## Trabalho Prático Final – GCC218 / GCC262

**Universidade Federal de Lavras**
Prof. Mayron Cézar O. Moreira

---

## 1. Objetivo da Etapa 2 🎯

A Etapa 2 tem como objetivo desenvolver um **algoritmo construtivo** para gerar uma solução inicial para o problema de roteamento em grafos com restrições de capacidade. Nesta etapa, é necessário criar rotas que atendam a todos os serviços (nós, arestas e arcos requeridos), respeitando as demandas e limitações do veículo, além de seguir o padrão de formatação das soluções estabelecido pelo professor.

---

## 2. O que foi implementado nesta etapa 🛠️

### 2.1. **Desenvolvimento do Algoritmo Construtivo** 🏗️

* Implementação de um algoritmo que constrói rotas a partir do zero, alocando serviços (nós, arestas e arcos requeridos) de forma que:

  * 🚫 **Nenhuma rota ultrapasse a capacidade máxima do veículo**;
  * ✅ **Cada serviço seja atendido por exatamente uma rota**;
  * 🧮 Se um vértice, aresta ou arco requerido for percorrido mais de uma vez, o custo e demanda desse serviço são contados apenas uma vez por rota.

* O algoritmo foi projetado para **garantir viabilidade** (todas as restrições são respeitadas) e para **buscar soluções de custo mínimo**, ainda que seja uma abordagem inicial (não necessariamente ótima).

---

### 2.2. **Formatação e Salvamento das Soluções** 🗃️

* As soluções geradas são salvas em arquivos seguindo o padrão solicitado:

  * Nome dos arquivos: `sol-nomeinstancia.dat`
  * Estrutura dos arquivos conforme modelo fornecido pelo docente

* Todos os testes foram realizados com as instâncias disponibilizadas pelo professor.

---

### 2.3. **Testes e Validação** 🧪

* Todas as soluções foram validadas para garantir:

  * Respeito à capacidade dos veículos;
  * Cobertura de todos os serviços obrigatórios;
  * Formatação correta dos arquivos de saída.

---

## 3. Como executar 🚦

1. **Execução do algoritmo:**

   * Utilize o script principal (`main.py`, `etapa_02.ipynb` ou equivalente) para processar cada instância presente na pasta de dados.

2. **Geração das soluções:**

   * As soluções serão salvas automaticamente na pasta especificada, seguindo o padrão exigido.

3. **Comando de execução (exemplo):**

   ```bash
   jupyter notebook etapa_02.ipynb
   ```

---

## 4. Estrutura do Repositório 🗂️

* `etapa_02.ipynb`: Script principal que executa o algoritmo construtivo.
* `dados/`: Pasta com as instâncias de entrada.
* `solucoes/`: Pasta com as soluções geradas.
* `README.md`: Este arquivo de explicação da etapa.

---

## 5. Regras e Observações 📜

* ⚠️ **Código autoral:** Todo o desenvolvimento é original, respeitando as normas da disciplina.
* 🚫 **Proibido** o uso de frameworks de grafos como `networkx` ou `igraph`. Apenas a biblioteca padrão e estruturas próprias foram utilizadas.
* 📏 **Padronização:** A formatação dos arquivos de solução segue exatamente o padrão solicitado para evitar penalidades na correção.

---

## 6. Créditos 🙋‍♂️🙋‍♀️

Desenvolvido por Tiago de Paula Martins e Samuel Moreira Abreu para as disciplinas GCC218 – Algoritmos em Grafos e GCC262 – Grafos e Suas Aplicações, UFLA.

---

### **Resumo das etapas cumpridas nesta fase:** ✅

* Projeto e implementação do algoritmo construtivo para roteamento;
* Testes e geração de soluções para todas as instâncias;
* Garantia de respeito a todas as restrições do problema e do formato de entrega;
* Organização das soluções em arquivos padronizados para submissão.

---
