# ARQUIVO: grafo.py

# Imports necessários
import heapq
from collections import defaultdict
import math
import matplotlib.pyplot as plt

# Definição da classe principal do grafo
class CustomGraph:
    """
    Representa a estrutura de dados do grafo, armazenando os seus componentes
    (vértices, arestas, arcos) e oferecendo métodos para o cálculo de métricas
    e de caminhos mínimos, conforme solicitado no trabalho.
    """
    def __init__(self, parsed_data):
        """
        Inicializa o grafo a partir dos dados extraídos do ficheiro de instância.
        Popula as listas de adjacência e os conjuntos de vértices, arestas e serviços.
        """
        # Inicialização dos atributos do grafo
        self.V = set()
        self.edges = []
        self.arcs = []
        self.required_nodes_info = {}
        self.required_edges_info = {}
        self.required_arcs_info = {}
        
        # Leitura dos metadados da instância
        self.depot = parsed_data["meta"]["depot"]
        self.capacity = parsed_data["meta"]["capacity"]
        self.graph = defaultdict(list)
        self.V.add(self.depot)

        # Processa os nós requeridos
        for node_data in parsed_data.get("ReN", []):
            node_id = node_data['id']
            self.required_nodes_info[node_id] = node_data
            self.V.add(node_id)

        # Processa as arestas (requeridas e não requeridas), que são não-direcionadas
        for edge_data in parsed_data.get("ReE", []):
            u, v, cost = edge_data['u'], edge_data['v'], edge_data['cost']
            self.edges.append((u, v, cost))
            self.required_edges_info[(u, v)] = edge_data
            self.required_edges_info[(v, u)] = edge_data # Armazena nos dois sentidos para facilitar a busca
            self.graph[u].append((v, cost))
            self.graph[v].append((u, cost))
            self.V.add(u)
            self.V.add(v)

        for edge_data in parsed_data.get("NrE", []):
            u, v, cost = edge_data['u'], edge_data['v'], edge_data['cost']
            self.edges.append((u, v, cost))
            self.graph[u].append((v, cost))
            self.graph[v].append((u, cost))
            self.V.add(u)
            self.V.add(v)

        # Processa os arcos (requeridos e não requeridos), que são direcionados
        for arc_data in parsed_data.get("ReA", []):
            u, v, cost = arc_data['u'], arc_data['v'], arc_data['cost']
            self.arcs.append((u, v, cost))
            self.required_arcs_info[(u, v)] = arc_data
            self.graph[u].append((v, cost))
            self.V.add(u)
            self.V.add(v)

        for arc_data in parsed_data.get("NrA", []):
            u, v, cost = arc_data['u'], arc_data['v'], arc_data['cost']
            self.arcs.append((u, v, cost))
            self.graph[u].append((v, cost))
            self.V.add(u)
            self.V.add(v)
        
        # Cria listas e conjuntos de serviços para acesso rápido
        self.required_nodes = set(self.required_nodes_info.keys())
        self.required_edges = list(self.required_edges_info.keys())
        self.required_arcs = list(self.required_arcs_info.keys())

    # --- Métodos para Estatísticas (Etapa 1) ---

    def num_vertices(self):
        """Retorna a quantidade total de vértices no grafo."""
        return len(self.V)

    def num_edges(self):
        """Retorna a quantidade total de arestas (não direcionadas) no grafo."""
        return len(self.edges)

    def num_arcs(self):
        """Retorna a quantidade total de arcos (direcionados) no grafo."""
        return len(self.arcs)

    def num_required_nodes(self):
        """Retorna a quantidade de nós que requerem serviço."""
        return len(self.required_nodes)

    def num_required_edges(self):
        """Retorna a quantidade de arestas que requerem serviço."""
        # A lista 'required_edges' armazena (u,v) e (v,u) para cada aresta.
        # Portanto, a contagem real de arestas únicas é o tamanho da lista a dividir por 2.
        return int(len(self.required_edges) / 2)

    def num_required_arcs(self):
        """Retorna a quantidade de arcos que requerem serviço."""
        return len(self.required_arcs)

    def density(self):
        """Calcula a densidade do grafo misto."""
        n = self.num_vertices()
        m = self.num_edges() + self.num_arcs()
        return m / (n * (n - 1)) if n > 1 else 0

    def degrees(self):
        """Calcula o grau mínimo e máximo entre todos os vértices do grafo."""
        degree = defaultdict(int)
        for u in self.graph:
            degree[u] += len(self.graph[u])
        
        for v_node in self.V:
            if v_node not in degree:
                degree[v_node] = 0
                
        return min(degree.values()), max(degree.values())
    
    def connected_components(self):
        """Encontra os componentes (fracamente) conectados do grafo usando BFS."""
        visited = set()
        components = []
        for v_node in self.V:
            if v_node not in visited:
                component = []
                q = [v_node]
                visited.add(v_node)
                while q:
                    u_node = q.pop(0)
                    component.append(u_node)
                    for neighbor, _ in self.graph.get(u_node, []):
                        if neighbor not in visited:
                            visited.add(neighbor)
                            q.append(neighbor)
                components.append(component)
        return components
    
    def average_path_length_and_diameter(self, dist):
        """Calcula o caminho médio e o diâmetro do grafo a partir da matriz de distâncias."""
        n = len(dist)
        values = [dist[i][j] for i in range(n) for j in range(n) if i != j and dist[i][j] < float('inf')]
        return (sum(values) / len(values), max(values)) if values else (float('inf'), float('inf'))

    def betweenness_centrality(self, dist, pred, node_to_index, index_to_node):
        """Calcula a centralidade de intermediação de cada nó (versão simplificada)."""
        n = len(self.V)
        centrality = {node: 0.0 for node in self.V}
        
        for i_idx in range(n):
            for j_idx in range(n):
                if i_idx == j_idx or pred[i_idx][j_idx] == -1:
                    continue
                
                curr_idx = j_idx
                while curr_idx != i_idx and pred[i_idx][curr_idx] != -1:
                    parent_idx = pred[i_idx][curr_idx]
                    if parent_idx != i_idx:
                        centrality[index_to_node[parent_idx]] += 1
                    curr_idx = parent_idx
        return centrality

    # --- Algoritmo Otimizado para Caminhos Mínimos ---

    def all_pairs_dijkstra(self):
        """
        Calcula a matriz de caminhos mínimos para todos os pares. Utiliza o algoritmo de
        Dijkstra a partir de cada nó, uma abordagem eficiente para os grafos esparsos do trabalho.
        """
        nodes = sorted(list(self.V))
        node_to_index = {node: i for i, node in enumerate(nodes)}
        index_to_node = {i: node for i, node in enumerate(nodes)}
        n = len(nodes)
        
        INF = float('inf')
        dist_matrix = [[INF] * n for _ in range(n)]
        pred_matrix = [[-1] * n for _ in range(n)]

        # Executa o Dijkstra para cada nó do grafo como origem.
        for start_node_val in nodes:
            start_node_idx = node_to_index[start_node_val]
            
            # Algoritmo de Dijkstra padrão com fila de prioridade (heapq).
            dist = {node: INF for node in self.V}
            pred = {node: -1 for node in self.V}
            dist[start_node_val] = 0
            pq = [(0, start_node_val)]

            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue

                for v, weight in self.graph.get(u, []):
                    if dist[u] + weight < dist[v]:
                        dist[v] = dist[u] + weight
                        pred[v] = u
                        heapq.heappush(pq, (dist[v], v))
            
            # Preenche as matrizes de resultado para o nó de início atual
            for end_node_val in nodes:
                end_node_idx = node_to_index[end_node_val]
                dist_matrix[start_node_idx][end_node_idx] = dist[end_node_val]
                if pred[end_node_val] != -1:
                    pred_matrix[start_node_idx][end_node_idx] = node_to_index[pred[end_node_val]]
                elif dist[end_node_val] == 0:
                    pred_matrix[start_node_idx][end_node_idx] = start_node_idx
        
        return dist_matrix, pred_matrix, node_to_index, index_to_node

# --- Função Auxiliar para Visualização ---

def desenhar_grafo(grafo):
    """
    Cria uma visualização gráfica do objeto CustomGraph usando a biblioteca Matplotlib.
    É uma ferramenta de depuração útil para instâncias pequenas.
    """
    nodes = list(grafo.V)
    num_nodes = len(nodes)
    node_pos = {}

    # Posiciona os nós em um círculo para melhor visualização.
    for i, node in enumerate(nodes):
        angle = 2 * math.pi * i / num_nodes
        x = 10 * math.cos(angle)
        y = 10 * math.sin(angle)
        node_pos[node] = (x, y)

    plt.figure(figsize=(12, 12))
    ax = plt.gca()
    ax.set_aspect('equal')

    # Desenha as arestas (não direcionadas) em cinza.
    for u, v, cost in grafo.edges:
        if u in node_pos and v in node_pos:
            x1, y1 = node_pos[u]
            x2, y2 = node_pos[v]
            plt.plot([x1, x2], [y1, y2], color='gray', linewidth=1, alpha=0.7, zorder=1)
    
    # Desenha os arcos (direcionados) com setas em azul.
    for u, v, cost in grafo.arcs:
        if u in node_pos and v in node_pos:
            x1, y1 = node_pos[u]
            x2, y2 = node_pos[v]
            dx, dy = x2 - x1, y2 - y1
            plt.arrow(x1, y1, dx * 0.9, dy * 0.9, head_width=0.4, head_length=0.5, fc='blue', ec='blue', alpha=0.6, zorder=2)

    # Desenha os nós, colorindo-os de acordo com a sua função.
    for node, (x, y) in node_pos.items():
        color = 'lightblue'  # Nó padrão
        if node == grafo.depot:
            color = 'red'  # Depósito
        elif node in grafo.required_nodes:
            color = 'yellow'  # Nó com serviço
        
        circle = plt.Circle((x, y), 0.5, color=color, ec='black', zorder=3)
        ax.add_patch(circle)
        plt.text(x, y, str(node), ha='center', va='center', fontsize=8, zorder=4)

    plt.axis('off')
    plt.title('Visualização do Grafo')
    plt.show()
