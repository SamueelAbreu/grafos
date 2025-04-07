import re
from collections import defaultdict
import pandas as pd

# Função para ler e interpretar os dados da instância
def parse_instance_fully_correct(file_path: str):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    data = {
        "meta": {},
        "ReN": [],
        "ReE": [],
        "ReA": [],
        "NonRequiredArcs": []
    }

    section = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("the data is"):
            continue
        if line.startswith("Name:"):
            data["meta"]["name"] = line.split(":")[1].strip()
        elif line.startswith("Capacity:"):
            data["meta"]["capacity"] = int(line.split(":")[1].strip())
        elif line.startswith("Depot Node:"):
            data["meta"]["depot"] = int(line.split(":")[1].strip())
        elif re.match(r"#\w+:", line):
            key, value = line.split(":")
            data["meta"][key.strip()] = int(value.strip())
        elif line.startswith("ReN."):
            section = "ReN"
        elif line.startswith("ReE."):
            section = "ReE"
        elif line.startswith("ReA."):
            section = "ReA"
        else:
            parts = re.split(r'\s+', line)
            if section == "ReN" and len(parts) == 3 and parts[0].startswith("N"):
                nid = int(parts[0][1:])
                demand = int(parts[1])
                scost = int(parts[2])
                data["ReN"].append((nid, demand, scost))
            elif section == "ReE" and len(parts) == 6 and parts[0].startswith("E"):
                _, u, v, cost, demand, scost = parts
                data["ReE"].append((int(u), int(v), int(cost), int(demand), int(scost)))
            elif section == "ReA" and len(parts) == 6 and parts[0].startswith("A"):
                _, u, v, cost, demand, scost = parts
                data["ReA"].append((int(u), int(v), int(cost), int(demand), int(scost)))
            elif (line.startswith("NrA") or line.startswith("ARC")) and len(parts) == 4:
                _, u, v, cost = parts
                data["NonRequiredArcs"].append((int(u), int(v), int(cost)))
    return data

# Classe que representa o grafo e calcula as estatísticas
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

    def num_vertices(self): 
        return len(self.V)
    
    def num_edges(self): 
        return len(self.edges)
    
    def num_arcs(self): 
        return len(self.arcs)
    
    def num_required_nodes(self): 
        return len(self.required_nodes)
    
    def num_required_edges(self): 
        return len(self.required_edges)
    
    def num_required_arcs(self): 
        return len(self.required_arcs)

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
        n = max(self.V) + 1
        INF = float('inf')
        dist = [[INF]*n for _ in range(n)]
        pred = [[-1]*n for _ in range(n)]
        for u in self.V:
            dist[u][u] = 0
            pred[u][u] = u
        for u in self.graph:
            for v, cost in self.graph[u]:
                dist[u][v] = min(dist[u][v], cost)
                pred[u][v] = u
        for k in self.V:
            for i in self.V:
                for j in self.V:
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]
        return dist, pred

    def average_path_length_and_diameter(self, dist):
        values = [dist[i][j] for i in self.V for j in self.V if i != j and dist[i][j] < float('inf')]
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
        bt = {v: 0 for v in self.V}
        for s in self.V:
            for t in self.V:
                if s != t and pred[s][t] != -1:
                    v = pred[s][t]
                    while v != s and v != -1:
                        bt[v] += 1
                        v = pred[s][v]
        return bt