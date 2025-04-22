'''Um supermercado, localizado na cidade de Drummondville (Québec, Canadá), iniciou suas atividades recentemente e tem se destacado pela preocupação com o bem-estar de seus empregados. A empresa pretende comprar um ônibus para o transporte dos funcionários. Por ser uma cidade de pequeno porte, todas as ruas de Drummondville são de mão-dupla.  O supermercado, desejando reduzir os custos, quer saber qual é o número mínimo de viagens que um motorista deve fazer para sair de um ponto A, levar os funcionários para um ponto B, considerando um total de C funcionários a serem transportados. Existe uma capacidade máxima permitida para o transporte de passageiros em cada rua de Drummonville. Essa última restrição é uma exigência recente da prefeitura, para preservar a arquitetura histórica da cidade e conservar mais as vias de circulação.
Como exemplo, suponha que as ruas, com as suas devidas intersecções e limite máximo de passageiros, sejam apresentadas abaixo:
(1,2): máximo de 30 pessoas;
(1,3): máximo de 20 pessoas;
(1,4): máximo de 10 pessoas;
(2,4): máximo de 40 pessoas;
(2,5): máximo de 80 pessoas;
(3,4): máximo de 13 pessoas;
(3,6): máximo de 13 pessoas;
(4,7): máximo de 25 pessoas;
(5,7): máximo de 12 pessoas;
(6,7): máximo de 35 pessoas.
Considerando A = 1, B = 7 e C = 97, então o supermercado gastaria pelo menos 5 viagens para levar todos os seus funcionários ao destino, levando em conta uma aquisição de um ônibus que carregue até 25 pessoas.
Entrada
A entrada do problema pode conter um ou mais casos de teste. Para cada caso de teste, a primeira linha contém dois inteiros: o número de intersecções da cidade, X, e o número de ruas da cidade, denotada por Y. As próximas Y linhas contém, cada uma, três inteiros: u, v e p, correspondendo à intersecção u que liga à intersecção v, com limite máximo de pessoas dentro de um veículo de transporte dado por p. Na linha subsequente, considera-se os valores de A, B e C, respectivamente. O fim de todos os casos de teste é dado pela sequência de dois zeros.
Saída
Para cada caso de teste, imprima o número mínimo de viagens necessárias para transportar os funcionários do supermercaso.

Input
7 10
1 2 30
1 3 20
1 4 10
2 4 40
2 5 80
3 4 13
3 6 13
4 7 25
5 7 12
6 7 35
1 7 97
0 0


Output 
5
'''
from collections import deque
import math

# Função pra verificar se dá pra ir do ponto A até B usando só ruas com capacidade mínima 'capacity'
def bfs(graph, n, A, B, capacity):
    visited = [False] * (n + 1)
    queue = deque()
    queue.append(A)
    visited[A] = True

    while queue:
        u = queue.popleft()
        for v, w in graph[u]:
            # Se ainda não visitou o vizinho e a rua aguenta pelo menos 'capacity' pessoas
            if not visited[v] and w >= capacity:
                visited[v] = True
                queue.append(v)

    # Retorna se a gente conseguiu chegar no ponto B
    return visited[B]

def resolver_casos():
    while True:
        X, Y = map(int, input().split())
        if X == 0 and Y == 0:
            break  

        graph = [[] for _ in range(X + 1)]
        max_weight = 0  # Guardar a maior capacidade de todas, pra ajudar no binary search

        for _ in range(Y):
            u, v, p = map(int, input().split())
            # Como as ruas são de mão dupla, a gente adiciona nos dois sentidos
            graph[u].append((v, p))
            graph[v].append((u, p))
            max_weight = max(max_weight, p)  # Sempre atualizando a maior capacidade vista até agora

        A, B, C = map(int, input().split())  # Pontos de origem, destino e quantidade de gente

        # Agora faz um binary search pra achar o maior valor de capacidade possível
        low, high = 1, max_weight
        best = 1

        while low <= high:
            mid = (low + high) // 2
            if bfs(graph, X, A, B, mid):  # Se dá pra fazer o caminho com essa capacidade
                best = mid  # Atualiza o melhor valor
                low = mid + 1  # Tenta achar um maior ainda
            else:
                high = mid - 1  # Se não deu, tenta um menor

        # O motorista também tá dentro do ônibus, tira 1 da capacidade
        efetiva = best - 1
        # Quantas viagens são necessárias? Divide o total pela capacidade útil do ônibus
        viagens = math.ceil(C / efetiva)

        print(viagens)  

resolver_casos()
