# 3. Classe do grafo com métricas
from collections import defaultdict
import math
import matplotlib.pyplot as plt

class CustomGraphFinal:
    def __init__(self, parsed_data):
        self.V = set()
        self.edges = []
        self.arcs = []
        self.required_nodes = set()
        self.required_edges = []
        self.required_arcs = []
        self.depot = parsed_data["meta"]["depot"]
        self.capacity = parsed_data["meta"]["capacity"]
        self.graph = defaultdict(list)

        self.V.add(self.depot)  # Garante que o depósito está sempre no grafo!

        for node_id, demand, scost in parsed_data["ReN"]:
            self.required_nodes.add(node_id)
            self.V.add(node_id)

        for u, v, cost, demand, scost in parsed_data["ReE"]:
            self.edges.append((u, v, cost))
            self.required_edges.append((u, v, cost, demand, scost))
            self.graph[u].append((v, cost))
            self.graph[v].append((u, cost))
            self.V.add(u)
            self.V.add(v)

        for u, v, cost, demand, scost in parsed_data["ReA"]:
            self.arcs.append((u, v, cost))
            self.required_arcs.append((u, v, cost, demand, scost))
            self.graph[u].append((v, cost))
            self.V.add(u)
            self.V.add(v)

        for u, v, cost in parsed_data["NonRequiredArcs"]:
            self.arcs.append((u, v, cost))
            self.graph[u].append((v, cost))
            self.V.add(u)
            self.V.add(v)
    
    def num_vertices(self): return len(self.V)
    def num_edges(self): return len(self.edges)
    def num_arcs(self): return len(self.arcs)
    def num_required_nodes(self): return len(self.required_nodes)
    def num_required_edges(self): return len(self.required_edges)
    def num_required_arcs(self): return len(self.required_arcs)

    def density(self):
        n = len(self.V)
        m = len(self.edges) + len(self.arcs)
        return m / (n * (n - 1)) if n > 1 else 0

    def degrees(self):
        degree = defaultdict(int)
        for u in self.graph:
            for v, _ in self.graph[u]:
                degree[u] += 1
        return min(degree.values()), max(degree.values())

    def floyd_warshall(self):
        # Mapeia cada nó para um índice sequencial
        nodes = sorted(list(self.V))
        node_to_index = {node: idx for idx, node in enumerate(nodes)}
        index_to_node = {idx: node for idx, node in enumerate(nodes)}

        n = len(nodes)
        INF = float('inf')
        dist = [[INF]*n for _ in range(n)]
        pred = [[-1]*n for _ in range(n)]

        # Inicializa
        for idx in range(n):
            dist[idx][idx] = 0
            pred[idx][idx] = idx

        for u in self.graph:
            for v, cost in self.graph[u]:
                i = node_to_index[u]
                j = node_to_index[v]
                dist[i][j] = min(dist[i][j], cost)
                pred[i][j] = i

        # Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]

        return dist, pred, node_to_index, index_to_node

    def average_path_length_and_diameter(self, dist):
        n = len(dist)
        values = [dist[i][j] for i in range(n) for j in range(n) if i != j and dist[i][j] < float('inf')]
        return (sum(values) / len(values), max(values)) if values else (float('inf'), float('inf'))

    def connected_components(self):
        visited = set()
        components = []
        def dfs(v, comp):
            visited.add(v)
            comp.append(v)
            for u, _ in self.graph[v]:
                if u not in visited:
                    dfs(u, comp)
        for v in self.V:
            if v not in visited:
                comp = []
                dfs(v, comp)
                components.append(comp)
        return components

    def betweenness_centrality(self, dist, pred):
        n = len(dist)
        bt = {i: 0 for i in range(n)}
        for s in range(n):
            for t in range(n):
                if s != t and pred[s][t] != -1:
                    v = pred[s][t]
                    while v != s and v != -1:
                        bt[v] += 1
                        v = pred[s][v]
        return bt
    
def desenhar_grafo(grafo):
    nodes = list(grafo.V)
    num_nodes = len(nodes)
    node_pos = {}

    # Distribuir os nós em um círculo
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / num_nodes
        x = math.cos(angle)
        y = math.sin(angle)
        node_pos[node] = (x, y)

    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_aspect('equal')

    # Desenhar arestas (não direcionadas)
    for u, v, cost in grafo.edges:
        x1, y1 = node_pos[u]
        x2, y2 = node_pos[v]
        plt.plot([x1, x2], [y1, y2], color='gray', linewidth=1, alpha=0.7)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        plt.text(mx, my, f'{cost}', fontsize=8, color='gray')

    # Desenhar arcos (direcionados)
    for u, v, cost in grafo.arcs:
        x1, y1 = node_pos[u]
        x2, y2 = node_pos[v]
        dx, dy = x2 - x1, y2 - y1
        plt.arrow(x1, y1, dx * 0.8, dy * 0.8, head_width=0.05, length_includes_head=True, color='blue', alpha=0.6)
        mx, my = x1 + dx * 0.5, y1 + dy * 0.5
        plt.text(mx, my, f'{cost}', fontsize=8, color='blue')

    # Desenhar nós
    for node, (x, y) in node_pos.items():
        if node == grafo.depot:
            color = 'red'
        elif node in grafo.required_nodes:
            color = 'yellow'
        else:
            color = 'lightblue'
        circle = plt.Circle((x, y), 0.07, color=color, ec='black', zorder=10)
        ax.add_patch(circle)
        plt.text(x, y, str(node), ha='center', va='center', fontsize=10, zorder=11)

    plt.axis('off')
    plt.title('Visualização do Grafo')
    plt.show()