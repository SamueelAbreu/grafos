import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# 1. Criação do grafo
# -------------------------------

# Criar um multigrafo direcionado
G = nx.MultiDiGraph()

# Conjunto de nós
V = [0, 1, 2, 3, 4]
G.add_nodes_from(V)

# Arestas/arcos (origem, destino, atributos)
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
VR = {0, 2}  # Nós requeridos
ER = [(0, 1), (2, 3)]  # Arestas requeridas
AR = [(4, 0)]          # Arcos requeridos

# -------------------------------
# 2. Cálculo das estatísticas
# -------------------------------

num_vertices = G.number_of_nodes()

# Contar arestas/arcos
num_arcs = sum(1 for u, v, k, d in G.edges(keys=True, data=True) if not G.has_edge(v, u, k))
num_edges = G.number_of_edges() - num_arcs

num_required_vertices = len(VR)
num_required_edges = len(ER)
num_required_arcs = len(AR)

density = nx.density(G.to_undirected())
components = nx.number_connected_components(G.to_undirected())

degrees = dict(G.degree())
min_degree = min(degrees.values())
max_degree = max(degrees.values())

# Intermediação
betweenness = nx.betweenness_centrality(G.to_undirected())

# Caminhos mais curtos e predecessores
lengths = dict(nx.all_pairs_dijkstra_path_length(G.to_undirected()))
predecessors = dict(nx.all_pairs_dijkstra_path(G.to_undirected()))

# Caminho médio e diâmetro
all_lengths = [l for target_dict in lengths.values() for l in target_dict.values() if l > 0]
average_path_length = np.mean(all_lengths)
diameter = max(all_lengths)

# Estatísticas finais
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

# Mostrar estatísticas
stats_df = pd.DataFrame(list(stats.items()), columns=["Métrica", "Valor"])
print("\n==== ESTATÍSTICAS DO GRAFO ====\n")
print(stats_df.to_string(index=False))

# -------------------------------
# 3. Visualização do Grafo
# -------------------------------

# Layout automático
pos = nx.spring_layout(G, seed=42)

# Separar arestas requeridas e não requeridas
required_edges = [(u, v) for u, v, d in G.edges(data=True) if d['requerida']]
non_required_edges = [(u, v) for u, v, d in G.edges(data=True) if not d['requerida']]

# Desenhar nós
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=700)

# Arestas requeridas em vermelho
nx.draw_networkx_edges(G, pos, edgelist=required_edges, edge_color='red', width=2, arrows=True)

# Arestas não requeridas em cinza tracejado
nx.draw_networkx_edges(G, pos, edgelist=non_required_edges, edge_color='gray', style='dashed', arrows=True)

# Rótulos dos nós
nx.draw_networkx_labels(G, pos, font_size=12)

# Rótulos de custo nas arestas
edge_labels = {(u, v): d['custo'] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Mostrar o grafo
plt.title("Grafo com Arestas/Arcos Requeridos (vermelhos)")
plt.axis('off')
plt.tight_layout()
plt.show()
