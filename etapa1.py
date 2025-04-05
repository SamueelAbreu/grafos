import networkx as nx
import numpy as np
import pandas as pd

# Criar um multigrafo direcionado (para representar arcos e arestas)
G = nx.MultiDiGraph()

# -------------------------------
# Exemplo de dados (simulados)
# -------------------------------

# Conjunto de vértices
V = [0, 1, 2, 3, 4]
G.add_nodes_from(V)

# Arestas/arcos: (origem, destino, atributos)
edges = [
    (0, 1, {'custo': 2, 'demanda': 3, 'requerida': True}),
    (1, 0, {'custo': 2, 'demanda': 3, 'requerida': True}),
    (1, 2, {'custo': 4, 'demanda': 1, 'requerida': False}),
    (2, 3, {'custo': 1, 'demanda': 2, 'requerida': True}),
    (3, 4, {'custo': 3, 'demanda': 2, 'requerida': False}),
    (4, 0, {'custo': 5, 'demanda': 2, 'requerida': True}),
]
G.add_edges_from(edges)

# Subconjuntos requeridos
VR = {0, 2}  # nós requeridos
ER = [(0, 1), (2, 3)]  # arestas requeridas (considerando bidirecionais)
AR = [(4, 0)]          # arcos requeridos (vias de mão única)

# -------------------------------
# Cálculo de Estatísticas
# -------------------------------

# Quantidade de vértices
num_vertices = G.number_of_nodes()

# Quantidade de arestas e arcos
num_arcs = sum(1 for u, v, k, d in G.edges(keys=True, data=True) if not G.has_edge(v, u, k))
num_edges = G.number_of_edges() - num_arcs

# Subconjuntos requeridos
num_required_vertices = len(VR)
num_required_edges = len(ER)
num_required_arcs = len(AR)

# Densidade (grafo não-direcionado para esta métrica)
density = nx.density(G.to_undirected())

# Componentes conectados (grafo não-direcionado)
components = nx.number_connected_components(G.to_undirected())

# Graus
min_degree = min(dict(G.degree()).values())
max_degree = max(dict(G.degree()).values())

# Intermediação (grafo não-direcionado)
betweenness = nx.betweenness_centrality(G.to_undirected())

# Matrizes de caminhos mais curtos e predecessores
lengths = dict(nx.all_pairs_dijkstra_path_length(G.to_undirected()))
predecessors = dict(nx.all_pairs_dijkstra_path(G.to_undirected()))

# Caminho médio e diâmetro
all_lengths = [l for target_dict in lengths.values() for l in target_dict.values() if l > 0]
average_path_length = np.mean(all_lengths)
diameter = max(all_lengths)

# -------------------------------
# Compilar estatísticas em DataFrame
# -------------------------------

stats = {
    "Quantidade de vértices": num_vertices,
    "Quantidade de arestas": num_edges,
    "Quantidade de arcos": num_arcs,
    "Quantidade de vértices requeridos": num_required_vertices,
    "Quantidade de arestas requeridas": num_required_edges,
    "Quantidade de arcos requeridos": num_required_arcs,
    "Densidade do grafo": density,
    "Componentes conectados": components,
    "Grau mínimo": min_degree,
    "Grau máximo": max_degree,
    "Intermediação": betweenness,
    "Caminho médio": average_path_length,
    "Diâmetro": diameter,
}

# Converte para DataFrame para visualização
stats_df = pd.DataFrame(list(stats.items()), columns=["Métrica", "Valor"])
print(stats_df)
