# Imports necessários
import copy
import time

class Rota:
    """ Representa uma única rota de um veículo. """
    def __init__(self, deposito_id, capacidade_max):
        self.id_deposito = deposito_id
        self.capacidade_maxima = capacidade_max
        
        # Lista de tuplas (service_id, u, v, tipo_servico)
        self.servicos_realizados = []
        self.carga_total = 0
        self.custo_total = 0

    def recalcular_rota_completa(self, grafo, servicos_info, dist_matrix, node_to_index):
        """ Recalcula o custo total da rota do zero. Útil após modificações complexas. """
        self.custo_total = 0
        no_atual = self.id_deposito
        
        # Custo de deslocamento + Custo de serviço
        for (sid, u, v, tipo) in self.servicos_realizados:
            # Custo do deslocamento do nó anterior até o início do serviço atual
            self.custo_total += dist_matrix[node_to_index[no_atual]][node_to_index[u]]
            # Custo de execução do serviço
            self.custo_total += servicos_info[(u,v,tipo)]['cost']
            no_atual = v # O próximo deslocamento começa do final deste serviço
            
        # Custo de retorno ao depósito
        self.custo_total += dist_matrix[node_to_index[no_atual]][node_to_index[self.id_deposito]]
        
        # Recalcula a carga
        self.carga_total = sum(servicos_info[(u,v,tipo)]['demand'] for (sid, u, v, tipo) in self.servicos_realizados)

    def get_sequencia_nos_servico(self):
        """ Retorna a sequência de nós visitados, incluindo o depósito no início e fim. """
        sequencia = [self.id_deposito]
        for (sid, u, v, tipo) in self.servicos_realizados:
            # Em um serviço de nó (u==v), não adicionamos o nó duas vezes
            if u == v:
                sequencia.append(u)
            else:
                sequencia.append(u)
                sequencia.append(v)
        sequencia.append(self.id_deposito)
        return sequencia


class Solucao:
    """ Representa a solução completa, com um conjunto de rotas. """
    def __init__(self):
        self.rotas = []
        self.custo_total = 0
        self.servicos_nao_atendidos = set()

    def recalcular_custo_solucao(self):
        """ Soma o custo de todas as rotas para obter o custo total da solução. """
        self.custo_total = sum(r.custo_total for r in self.rotas)

    def adicionar_rota(self, rota):
        self.rotas.append(rota)
        self.recalcular_custo_solucao()

    def print_formatado(self, nome_instancia, tempo_total, tempo_melhor_sol):
        """ Imprime a solução no formato DAT exigido pelo professor. """
        print(f"{int(self.custo_total)}")
        print(f"{len(self.rotas)}")
        print(f"{int(tempo_total)}")
        print(f"{int(tempo_melhor_sol)}")

        for i, rota in enumerate(self.rotas, 1):
            # Formato da linha: 0 1 ID_ROTA DEMANDA CUSTO VISITAS (sequencia...)
            # Vamos usar a carga total e o número de serviços + 2 (depósito).
            num_visitas = len(rota.servicos_realizados) + 2
            
            linha = f"0 1 {i} {int(rota.carga_total)} {int(rota.custo_total)} {num_visitas}"
            
            # Formato da tupla (Tipo ID, Nó1, Nó2)
            # Depósito no início
            linha += f" (D 0,1,1)"

            # Serviços
            for (sid, u, v, tipo) in rota.servicos_realizados:
                linha += f" (S {sid},{u},{v})"

            # Depósito no fim
            linha += f" (D 0,1,1)"
            
            print(linha)


def preparar_servicos(parsed_data):
    """ Prepara um dicionário único com todos os serviços e atribui IDs. """
    servicos_info = {} # Chave (u,v,tipo) -> {'demand': D, 'cost': C, 'id': ID}
    id_counter = 1
    
    # Nós requeridos (u e v são iguais)
    for node_data in parsed_data["ReN"]:
        nid, demand, cost = node_data['id'], node_data['demand'], node_data['cost']
        servicos_info[(nid, nid, 'N')] = {'demand': demand, 'cost': cost, 'id': id_counter}
        id_counter += 1
        
    # Arestas requeridas
    for edge_data in parsed_data["ReE"]:
        u, v, cost, demand, scost = edge_data['u'], edge_data['v'], edge_data['cost'], edge_data['demand'], edge_data['scost']
        # O custo do serviço de uma aresta é o 'service_cost' (scost), não o custo de travessia ('cost')
        servicos_info[(u, v, 'E')] = {'demand': demand, 'cost': scost, 'id': id_counter}
        id_counter += 1
        
    # Arcos requeridos
    for arc_data in parsed_data["ReA"]:
        u, v, cost, demand, scost = arc_data['u'], arc_data['v'], arc_data['cost'], arc_data['demand'], arc_data['scost']
        servicos_info[(u, v, 'A')] = {'demand': demand, 'cost': scost, 'id': id_counter}
        id_counter += 1
        
    return servicos_info


def construtivo_guloso_vizinho_mais_proximo(grafo, servicos_info, dist_matrix, node_to_index):
    """
    Algoritmo construtivo simples (vizinho mais próximo).
    Cria rotas adicionando o serviço mais próximo que ainda não foi atendido.
    """
    solucao = Solucao()
    servicos_nao_atendidos = set(servicos_info.keys())
    
    while servicos_nao_atendidos:
        # Inicia uma nova rota a partir do depósito
        rota_atual = Rota(grafo.depot, grafo.capacity)
        no_atual = grafo.depot
        
        while True:
            melhor_servico = None
            menor_custo_insercao = float('inf')
            
            # Encontra o serviço mais próximo do nó atual que pode ser adicionado
            for (u, v, tipo) in servicos_nao_atendidos:
                demanda = servicos_info[(u,v,tipo)]['demand']
                
                # Custo para ir do nó atual ao início do serviço
                custo_deslocamento = dist_matrix[node_to_index[no_atual]][node_to_index[u]]
                
                if rota_atual.carga_total + demanda <= rota_atual.capacidade_maxima and custo_deslocamento < menor_custo_insercao:
                    menor_custo_insercao = custo_deslocamento
                    melhor_servico = (u, v, tipo)
            
            if melhor_servico:
                # Adiciona o melhor serviço encontrado à rota
                u, v, tipo = melhor_servico
                info = servicos_info[melhor_servico]
                rota_atual.servicos_realizados.append((info['id'], u, v, tipo))
                rota_atual.carga_total += info['demand']
                servicos_nao_atendidos.remove(melhor_servico)
                no_atual = v # Atualiza o nó atual para o final do serviço adicionado
            else:
                # Nenhum serviço pode ser adicionado (capacidade ou não há mais serviços)
                break
        
        # Se a rota não ficou vazia, recalcula seus custos e a adiciona à solução
        if rota_atual.servicos_realizados:
            rota_atual.recalcular_rota_completa(grafo, servicos_info, dist_matrix, node_to_index)
            solucao.adicionar_rota(rota_atual)
            
    solucao.recalcular_custo_solucao()
    return solucao