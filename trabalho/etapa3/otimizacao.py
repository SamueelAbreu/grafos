# ARQUIVO: otimizacao.py

import copy

def swap_entre_rotas(solucao_obj, grafo, servicos_info, dist_matrix, node_to_index):
    """
    Aplica um algoritmo de busca local (Etapa 3) para otimizar uma solução inicial.

    A heurística explora a vizinhança de troca de serviços (inter-route swap),
    onde um serviço de uma rota é trocado por um serviço de outra.

    Estratégia de Busca:
        - Best Improvement: A cada iteração, avalia todas as trocas possíveis e aplica
          apenas a que gera a maior redução de custo.
        - Iterativa: O processo repete-se até que nenhuma troca vantajosa seja encontrada.

    Otimização de Performance:
        - Avaliação Delta: O custo de cada troca é calculado de forma incremental (O(1)),
          evitando o recálculo completo da rota, o que torna a busca eficiente.
    
    Args:
        solucao_obj (Solucao): O objeto de solução inicial a ser otimizado.
        grafo (CustomGraph): O objeto do grafo.
        servicos_info (dict): Dicionário com informações detalhadas de cada serviço.
        dist_matrix (list[list]): Matriz de caminhos mínimos pré-calculada.
        node_to_index (dict): Mapeamento de ID de nó para índice de matriz.

    Returns:
        Solucao: Um novo objeto de solução, otimizado pela busca local.
    """
    # Cria uma cópia profunda inicial para não modificar a solução original.
    solucao_atual = copy.deepcopy(solucao_obj)

    while True:
        melhor_delta_custo = 0
        melhor_troca_info = None

        # Itera sobre todos os pares de rotas (r1, r2) para testar trocas.
        for i in range(len(solucao_atual.rotas)):
            for j in range(i + 1, len(solucao_atual.rotas)):
                rota1 = solucao_atual.rotas[i]
                rota2 = solucao_atual.rotas[j]

                # Itera sobre todos os pares de serviços (s1 de r1, s2 de r2).
                for idx1, (s1_id, u1, v1, t1) in enumerate(rota1.servicos_realizados):
                    for idx2, (s2_id, u2, v2, t2) in enumerate(rota2.servicos_realizados):
                        
                        servico1_info = servicos_info[(u1, v1, t1)]
                        servico2_info = servicos_info[(u2, v2, t2)]
                        
                        # --- 1. Checagem de Viabilidade (Capacidade) ---
                        # Verifica se a troca respeita a capacidade máxima de ambos os veículos.
                        if (rota1.carga_total - servico1_info['demand'] + servico2_info['demand'] > rota1.capacidade_maxima) or \
                           (rota2.carga_total - servico2_info['demand'] + servico1_info['demand'] > rota2.capacidade_maxima):
                            continue

                        # --- 2. Cálculo do Delta Custo (Otimização O(1)) ---
                        # Identifica os nós vizinhos de cada serviço na sua rota original.
                        no_ant1 = rota1.id_deposito if idx1 == 0 else rota1.servicos_realizados[idx1 - 1][2]
                        no_prox1 = rota1.id_deposito if idx1 == len(rota1.servicos_realizados) - 1 else rota1.servicos_realizados[idx1 + 1][1]
                        
                        no_ant2 = rota2.id_deposito if idx2 == 0 else rota2.servicos_realizados[idx2 - 1][2]
                        no_prox2 = rota2.id_deposito if idx2 == len(rota2.servicos_realizados) - 1 else rota2.servicos_realizados[idx2 + 1][1]
                        
                        # Custo da vizinhança do serviço 1 na rota 1 (a ser removido)
                        custo_antigo1 = (dist_matrix[node_to_index[no_ant1]][node_to_index[u1]] + servico1_info['cost'] + dist_matrix[node_to_index[v1]][node_to_index[no_prox1]])
                        # Custo da vizinhança do serviço 2 na rota 2 (a ser removido)
                        custo_antigo2 = (dist_matrix[node_to_index[no_ant2]][node_to_index[u2]] + servico2_info['cost'] + dist_matrix[node_to_index[v2]][node_to_index[no_prox2]])

                        # Custo de inserir o serviço 2 na rota 1
                        custo_novo1 = (dist_matrix[node_to_index[no_ant1]][node_to_index[u2]] + servico2_info['cost'] + dist_matrix[node_to_index[v2]][node_to_index[no_prox1]])
                        # Custo de inserir o serviço 1 na rota 2
                        custo_novo2 = (dist_matrix[node_to_index[no_ant2]][node_to_index[u1]] + servico1_info['cost'] + dist_matrix[node_to_index[v1]][node_to_index[no_prox2]])
                        
                        # A variação total de custo é a diferença entre o custo novo e o antigo.
                        delta_local = (custo_novo1 + custo_novo2) - (custo_antigo1 + custo_antigo2)

                        # Se a troca atual for a melhor encontrada até agora, guarda a sua informação.
                        if delta_local < melhor_delta_custo:
                            melhor_delta_custo = delta_local
                            melhor_troca_info = (i, j, idx1, idx2)

        # Após testar todas as trocas, verifica se uma melhoria foi encontrada.
        if melhor_troca_info:
            # --- 3. Aplicação da Melhor Troca Encontrada ---
            i, j, idx1, idx2 = melhor_troca_info
            
            # Realiza a troca dos serviços entre as listas das rotas.
            servico_trocado1 = solucao_atual.rotas[i].servicos_realizados[idx1]
            servico_trocado2 = solucao_atual.rotas[j].servicos_realizados[idx2]
            solucao_atual.rotas[i].servicos_realizados[idx1] = servico_trocado2
            solucao_atual.rotas[j].servicos_realizados[idx2] = servico_trocado1
            
            # Recalcula o custo e a carga das duas rotas alteradas para manter a consistência.
            solucao_atual.rotas[i].recalcular_rota_completa(grafo, servicos_info, dist_matrix, node_to_index)
            solucao_atual.rotas[j].recalcular_rota_completa(grafo, servicos_info, dist_matrix, node_to_index)
        else:
            # Se nenhuma troca vantajosa foi encontrada numa iteração completa, a busca termina.
            break
            
    # Recalcula o custo total da solução antes de a retornar.
    solucao_atual.recalcular_custo_solucao()
    return solucao_atual