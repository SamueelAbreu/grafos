def swap_entre_rotas(solucoes, grafo, servico_ids, dist, node_to_index, servicos):
    """
    Tenta trocar pares de serviços entre rotas diferentes,
    aceitando a troca se houver redução de custo e as restrições forem respeitadas.
    Retorna uma nova lista de rotas.
    """
    import copy
    melhorou = True
    solucoes = copy.deepcopy(solucoes)  # para não modificar o original

    while melhorou:
        melhorou = False
        # Percorre todos os pares de rotas diferentes
        for i in range(len(solucoes)):
            for j in range(i+1, len(solucoes)):
                rota1 = solucoes[i]
                rota2 = solucoes[j]

                for idx1, serv1 in enumerate(rota1.servicos_realizados):
                    for idx2, serv2 in enumerate(rota2.servicos_realizados):
                        nova_rota1 = copy.deepcopy(rota1)
                        nova_rota2 = copy.deepcopy(rota2)
                        # Troca os serviços
                        nova_rota1.servicos_realizados[idx1], nova_rota2.servicos_realizados[idx2] = \
                            nova_rota2.servicos_realizados[idx2], nova_rota1.servicos_realizados[idx1]

                        # Recalcula carga e custo das rotas após a troca
                        def atualiza_rota(rota):
                            # Agora, pega a demanda correta do dicionário servicos
                            rota.carga = sum(servicos[(u, v, tipo)][0] for (sid, u, v, tipo) in rota.servicos_realizados)
                            rota.custo = 0
                            rota.rota = [grafo.depot]
                            for sid, u, v, tipo in rota.servicos_realizados:
                                rota.rota.append(v)
                                i = node_to_index[rota.rota[-2]]
                                j = node_to_index[v]
                                rota.custo += dist[i][j]
                            rota.rota.append(grafo.depot)  # volta ao depósito
                            return rota

                        nova_rota1 = atualiza_rota(nova_rota1)
                        nova_rota2 = atualiza_rota(nova_rota2)

                        # Checa restrição de capacidade
                        if (nova_rota1.carga > nova_rota1.capacidade) or (nova_rota2.carga > nova_rota2.capacidade):
                            continue

                        # Checa se melhorou
                        custo_antigo = rota1.custo + rota2.custo
                        custo_novo = nova_rota1.custo + nova_rota2.custo
                        if custo_novo < custo_antigo:
                            solucoes[i] = nova_rota1
                            solucoes[j] = nova_rota2
                            melhorou = True
                            break
                    if melhorou:
                        break
                if melhorou:
                    break
            if melhorou:
                break
    return solucoes