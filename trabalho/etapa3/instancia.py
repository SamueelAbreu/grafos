# ARQUIVO: instancia.py

# Imports necessários
import re

def parse_instance(file_path: str):
    """
    Lê e interpreta um ficheiro de instância do problema (.dat), extraindo os seus
    metadados e os dados de nós, arestas e arcos (requeridos ou não).

    A função utiliza uma abordagem de máquina de estados para identificar a secção
    atual do ficheiro e processar as linhas de acordo com o seu formato específico.

    Args:
        file_path (str): O caminho para o ficheiro .dat da instância.

    Returns:
        dict: Um dicionário estruturado contendo os metadados e os dados do grafo.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Estrutura de dados principal para armazenar as informações da instância.
    data = {
        "meta": {},
        "ReN": [], "ReE": [], "ReA": [], # Elementos requeridos
        "NrE": [], "NrA": []             # Elementos não requeridos
    }
    
    # Mapeia os cabeçalhos do ficheiro para as chaves do dicionário de dados.
    # Esta abordagem torna o parser flexível a diferentes nomes de cabeçalho.
    section_map = {
        "ReN.": "ReN",
        "ReE.": "ReE",
        "ReA.": "ReA",
        "EDGE": "NrE", 
        "ARC": "NrA"
    }

    current_section = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Verifica se a linha atual corresponde a um cabeçalho de secção.
        section_header_found = False
        for header, key in section_map.items():
            if line.startswith(header):
                current_section = key
                section_header_found = True
                break
        
        if section_header_found:
            continue

        # Divide a linha em partes com base em espaços em branco.
        parts = re.split(r'\s+', line)

        # Processa os metadados do cabeçalho do ficheiro (antes de qualquer secção de dados).
        if current_section is None:
            if ":" in line:
                key, value = [p.strip() for p in line.split(":", 1)]
                if key == 'Name':
                    data["meta"]["name"] = value
                elif key == 'Capacity':
                    data["meta"]["capacity"] = int(value)
                elif key == 'Depot Node':
                    data["meta"]["depot"] = int(value)
                elif key.startswith("#"):
                    data["meta"][key] = int(value)
            continue

        # Processa a linha de dados com base na secção atual identificada.
        try:
            if current_section == "ReN" and parts[0].startswith("N"):
                nid = int(parts[0][1:])
                demand = int(parts[1])
                scost = int(parts[2])
                data["ReN"].append({'id': nid, 'demand': demand, 'cost': scost})
            
            elif current_section == "ReE" and parts[0].startswith("E"):
                _, u, v, cost, demand, scost = parts
                data["ReE"].append({'u': int(u), 'v': int(v), 'cost': int(cost), 'demand': int(demand), 'scost': int(scost)})

            elif current_section == "NrE" and parts[0].startswith("NrE"):
                _, u, v, cost = parts
                data["NrE"].append({'u': int(u), 'v': int(v), 'cost': int(cost)})

            elif current_section == "ReA" and parts[0].startswith("A"):
                _, u, v, cost, demand, scost = parts
                data["ReA"].append({'u': int(u), 'v': int(v), 'cost': int(cost), 'demand': int(demand), 'scost': int(scost)})

            elif current_section == "NrA" and parts[0].startswith("NrA"):
                _, u, v, cost = parts
                data["NrA"].append({'u': int(u), 'v': int(v), 'cost': int(cost)})
        
        except (ValueError, IndexError):
            # Ignora linhas que não correspondem ao formato de dados esperado,
            # como os cabeçalhos das colunas (ex: "From N. To N. ...").
            continue
            
    return data
