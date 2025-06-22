import copy
from collections import deque, defaultdict

class Rota:
    def __init__(self, deposito, capacidade):
        self.rota = [deposito]  # Sequência de nós visitados
        self.carga = 0
        self.capacidade = capacidade
        self.custo = 0
        self.servicos_realizados = []    # Lista de serviços realizados
        self.servicos_atendidos = set()  # Conjunto para checar duplicidades

    def pode_adicionar(self, demanda):
        """Verifica se é possível adicionar um serviço sem exceder a capacidade."""
        return self.carga + demanda <= self.capacidade

    def adicionar_servico(self, origem, destino, id_serv, custo_real, demanda, tipo_servico, pred=None):
        """Adiciona um serviço à rota."""
        self.rota.append(destino)
        self.custo += custo_real
        self.carga += demanda
        self.servicos_realizados.append((id_serv, origem, destino, tipo_servico))
        self.servicos_atendidos.add((origem, destino, tipo_servico))

def preparar_servicos(parsed_data, deposito):
    """Prepara dicionários de serviços e IDs."""
    servicos = {}
    servico_ids = {}
    id_counter = 1

    for node_id, demand, scost in parsed_data["ReN"]:
        servicos[(deposito, node_id, 'N')] = (demand, scost)
        servico_ids[(deposito, node_id, 'N')] = id_counter
        id_counter += 1
    for u, v, cost, demand, scost in parsed_data["ReE"]:
        servicos[(u, v, 'E')] = (demand, scost)
        servico_ids[(u, v, 'E')] = id_counter
        id_counter += 1
    for u, v, cost, demand, scost in parsed_data["ReA"]:
        servicos[(u, v, 'A')] = (demand, scost)
        servico_ids[(u, v, 'A')] = id_counter
        id_counter += 1

    return servicos, servico_ids

def inicializa_rotas_savings(servicos, deposito, servico_ids):
    """Cria uma rota inicial para cada serviço, isoladamente."""
    rotas = {}
    for (u, v, tipo), (demanda, scost) in servicos.items():
        id_serv = servico_ids[(u, v, tipo)]
        rota = {
            "servicos": [(id_serv, u, v, tipo)],
            "nos": [deposito, u, v, deposito] if u != deposito else [deposito, v, deposito],
            "carga": demanda,
            "custo": scost,
            "caminho": [(u, v, tipo)]
        }
        rotas[(u, v, tipo)] = rota
    return rotas

def calcula_savings(rotas, deposito, matriz_custos, node_to_index):
    """Calcula a matriz de savings para pares de rotas."""
    savings = []
    chaves = list(rotas.keys())
    for i in range(len(chaves)):
        for j in range(i+1, len(chaves)):
            s1 = rotas[chaves[i]]
            s2 = rotas[chaves[j]]
            end1 = s1["nos"][-2]
            start2 = s2["nos"][1]
            i_depot = node_to_index[deposito]
            i_end1 = node_to_index[end1]
            i_start2 = node_to_index[start2]
            saving = matriz_custos[i_depot][i_end1] + matriz_custos[i_depot][i_start2] - matriz_custos[i_end1][i_start2]
            savings.append(((chaves[i], chaves[j]), saving))
    savings.sort(key=lambda x: -x[1])
    return savings

def pode_fundir(rot1, rot2, capacidade):
    """Verifica se é possível unir duas rotas sem exceder a capacidade."""
    return rot1["carga"] + rot2["carga"] <= capacidade

def fundir_rotas(rot1, rot2, matriz_custos, deposito, servicos, node_to_index):
    """Funde duas rotas em uma nova rota."""
    nova_nos = rot1["nos"][:-1] + rot2["nos"][1:]
    nova_servicos = rot1["servicos"] + rot2["servicos"]
    nova_caminho = rot1["caminho"] + rot2["caminho"]
    nova_carga = rot1["carga"] + rot2["carga"]
    custo = 0
    for i in range(len(nova_nos)-1):
        custo += matriz_custos[node_to_index[nova_nos[i]]][node_to_index[nova_nos[i+1]]]
    custo += sum(servicos[(u, v, tipo)][1] for (id_serv, u, v, tipo) in nova_servicos)
    return {
        "servicos": nova_servicos,
        "nos": nova_nos,
        "carga": nova_carga,
        "custo": custo,
        "caminho": nova_caminho
    }

def caminho_totalmente_viavel(nos, matriz_custos, node_to_index):
    """Verifica se todas as arestas do caminho existem (não há custos infinitos)."""
    for i in range(len(nos) - 1):
        if matriz_custos[node_to_index[nos[i]]][node_to_index[nos[i+1]]] == float('inf'):
            return False
    return True

def acessiveis_do_deposito(grafo, deposito):
    """Retorna todos os nós acessíveis a partir do depósito (BFS)."""
    visited = set()
    fila = deque([deposito])
    while fila:
        v = fila.popleft()
        if v in visited:
            continue
        visited.add(v)
        for u, _ in grafo.graph[v]:
            if u not in visited:
                fila.append(u)
    return visited

def construtivo_savings(g, servicos, servico_ids, deposito, capacidade, matriz_custos, node_to_index):
    """Algoritmo construtivo baseado no Savings de Clarke & Wright."""
    rotas = inicializa_rotas_savings(servicos, deposito, servico_ids)
    savings = calcula_savings(rotas, deposito, matriz_custos, node_to_index)
    rotas_chave = copy.deepcopy(rotas)
    service_to_route = {k: k for k in rotas_chave}

    for (par, saving) in savings:
        k1, k2 = par
        r1_chave = service_to_route[k1]
        r2_chave = service_to_route[k2]
        if r1_chave == r2_chave:
            continue
        rot1 = rotas_chave[r1_chave]
        rot2 = rotas_chave[r2_chave]
        if rot1["nos"][-2] == rot2["nos"][1]:
            continue

        nova_rota_temp = fundir_rotas(rot1, rot2, matriz_custos, deposito, servicos, node_to_index)
        nos = nova_rota_temp["nos"]
        if pode_fundir(rot1, rot2, capacidade) and caminho_totalmente_viavel(nos, matriz_custos, node_to_index):
            nova_rota = nova_rota_temp
            del rotas_chave[r1_chave]
            del rotas_chave[r2_chave]
            nova_key = tuple(sorted(rot1["servicos"] + rot2["servicos"]))
            rotas_chave[nova_key] = nova_rota
            for s in rot1["caminho"] + rot2["caminho"]:
                service_to_route[s] = nova_key

    rotas_finais = []
    for rota_dict in rotas_chave.values():
        nos = rota_dict["nos"]
        if not caminho_totalmente_viavel(nos, matriz_custos, node_to_index):
            continue
        rota_obj = Rota(deposito, capacidade)
        rota_obj.rota = rota_dict["nos"]
        rota_obj.carga = rota_dict["carga"]
        rota_obj.custo = rota_dict["custo"]
        for (id_serv, u, v, tipo) in rota_dict["servicos"]:
            rota_obj.servicos_realizados.append((id_serv, u, v, tipo))
            rota_obj.servicos_atendidos.add((u, v, tipo))
        rotas_finais.append(rota_obj)
    return rotas_finais

def print_solucao_padroes(solucoes, nome_instancia, servico_ids, clocks_ref=0, clocks_sol=0):
    """Imprime a solução no padrão solicitado pelo professor."""
    custo_total = int(sum(r.custo for r in solucoes))
    print(f"{custo_total}")
    print(f"{len(solucoes)}")
    print(f"{clocks_ref}")  # clocks do algoritmo referência (coloque o valor correto se medir, senão deixe 0)
    print(f"{clocks_sol}")  # clocks para encontrar a solução referência (idem)

    for idx, rota in enumerate(solucoes, start=1):
        num_servicos = len(rota.servicos_realizados)
        carga = int(rota.carga)
        tam_rota = len(rota.rota)

        # Trate custo infinito explicitamente
        if rota.custo == float('inf') or rota.custo != rota.custo:  # float('inf') e NaN
            print(f"# ⚠ Atenção: rota {idx} possui custo infinito ou inválido e será ignorada.")
            continue

        custo = int(rota.custo)
        # Cabeçalho da linha
        linha = f"0 1 {idx} {num_servicos} {custo} {carga} {tam_rota}"
        # Primeira visita ao depósito
        linha += f" (D {rota.rota[0]},{rota.rota[1]},{rota.rota[1]})"
        # Serviços realizados
        for i in range(1, tam_rota - 1):
            u = rota.rota[i-1]
            v = rota.rota[i]
            id_serv = None
            for tipo in ['N', 'E', 'A']:
                if (u, v, tipo) in servico_ids:
                    id_serv = servico_ids[(u, v, tipo)]
                    break
            if id_serv is not None:
                linha += f" (S {id_serv},{u},{v})"
        # Última visita ao depósito
        linha += f" (D {rota.rota[-2]},{rota.rota[-1]},{rota.rota[-1]})"
        # Agora sim, imprime e quebra linha
        print(linha)