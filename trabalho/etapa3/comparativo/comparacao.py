import os
import glob

def parse_solution_file(path):
    """
    Lê um ficheiro de solução e extrai as 4 primeiras linhas de metadados.
    Retorna um dicionário com os dados ou None se o ficheiro for inválido.
    """
    try:
        with open(path, 'r') as f:
            # Lê apenas as linhas não vazias do ficheiro
            lines = [l.strip() for l in f if l.strip()]
            if len(lines) < 4:
                return None  # Retorna None se o ficheiro não tiver o cabeçalho mínimo

            # Converte os dados para os tipos numéricos corretos
            return {
                'custo':       float(lines[0]),
                'rotas':       int(lines[1]),
                'clocks_exec': int(lines[2]),
                'clocks_ref':  int(lines[3]),
            }
    except (ValueError, IndexError):
        # Captura erros de conversão ou se uma linha esperada não existir
        return None

def formatar_comparativo_percentual(valor_seu, valor_prof, tipo='custo'):
    """
    Formata uma string de comparação em percentual, adicionando uma interpretação
    textual para facilitar a análise dos resultados.
    """
    # Evita divisão por zero se o valor de referência for 0
    if valor_prof == 0:
        return "inf%" if valor_seu > 0 else "0.00% (equivalente)"

    percent_diff = ((valor_seu - valor_prof) / valor_prof) * 100
    
    # Adiciona uma interpretação textual baseada no tipo de métrica
    if tipo in ['custo', 'tempo']:
        if percent_diff < -0.01:
            interpretacao = "(melhor)" if tipo == 'custo' else "(mais rápido)"
        elif percent_diff > 0.01:
            interpretacao = "(pior)" if tipo == 'custo' else "(mais lento)"
        else:
            interpretacao = "(equivalente)"
    else: 
        interpretacao = "(diferença)"

    # Retorna o valor formatado com sinal de positivo/negativo e duas casas decimais
    return f"{percent_diff:+.2f}% {interpretacao}"


def compare_solutions(dir_swap, dir_prof, output_path):
    """
    Função principal que compara os ficheiros de solução do diretório do grupo ('dir_swap')
    com os do diretório de referência ('dir_prof') e gera um relatório.
    """
    # Procura todos os ficheiros de solução gerados pelo algoritmo do grupo
    swap_files = glob.glob(os.path.join(dir_swap, 'sol-*.dat'))
    
    # Listas para agregar os resultados e calcular as médias no final
    gaps, diffs_rotas, ratios_exec, ratios_ref = [], [], [], []
    report_lines = []

    # Itera sobre cada ficheiro de solução encontrado, em ordem alfabética
    for swap_file in sorted(swap_files):
        filename = os.path.basename(swap_file)
        
        # Assume que o ficheiro de referência tem o mesmo nome
        prof_file = os.path.join(dir_prof, filename)

        report_lines.append(f"=== Comparação: {filename} ===")

        # Verifica se o ficheiro de referência correspondente existe
        if not os.path.exists(prof_file):
            report_lines.append(f"⚠️  Arquivo de referência não encontrado em: {prof_file}\n")
            continue
            
        # Lê os dados de ambos os ficheiros de solução
        s_swap = parse_solution_file(swap_file)
        s_prof = parse_solution_file(prof_file)

        # Valida se os ficheiros foram lidos corretamente
        if s_swap is None:
            report_lines.append("❌ Erro: O seu ficheiro de solução está mal-formado ou vazio.\n")
            continue
        if s_prof is None:
            report_lines.append(f"❌ Erro: O ficheiro de referência ({filename}) está mal-formado ou vazio.\n")
            continue

        # Realiza os cálculos comparativos para esta instância
        gap_str = formatar_comparativo_percentual(s_swap['custo'], s_prof['custo'], tipo='custo')
        diff_rotas = s_swap['rotas'] - s_prof['rotas']
        perf_exec_str = formatar_comparativo_percentual(s_swap['clocks_exec'], s_prof['clocks_exec'], tipo='tempo')
        perf_ref_str = formatar_comparativo_percentual(s_swap['clocks_ref'], s_prof['clocks_ref'], tipo='tempo')

        # Adiciona os valores numéricos às listas para o cálculo das médias
        if s_prof['custo'] > 0:
            gaps.append((s_swap['custo'] - s_prof['custo']) / s_prof['custo'] * 100)
        diffs_rotas.append(diff_rotas)
        if s_prof['clocks_exec'] > 0:
            ratios_exec.append((s_swap['clocks_exec'] - s_prof['clocks_exec']) / s_prof['clocks_exec'] * 100)
        if s_prof['clocks_ref'] > 0:
            ratios_ref.append((s_swap['clocks_ref'] - s_prof['clocks_ref']) / s_prof['clocks_ref'] * 100)

        # Formata as linhas do relatório para esta instância
        report_lines.append(f"Custo:            {s_swap['custo']:<12.0f} | Prof: {s_prof['custo']:<12.0f} | Gap: {gap_str}")
        report_lines.append(f"Rotas:            {s_swap['rotas']:<12} | Prof: {s_prof['rotas']:<12} | Diferença: {diff_rotas:+.0f}")
        report_lines.append(f"Tempo Execução:   {s_swap['clocks_exec']:<12} | Prof: {s_prof['clocks_exec']:<12} | Desempenho: {perf_exec_str}")
        report_lines.append(f"Tempo Melhor Sol: {s_swap['clocks_ref']:<12} | Prof: {s_prof['clocks_ref']:<12} | Desempenho: {perf_ref_str}")
        report_lines.append("")

    # Calcula e adiciona as estatísticas gerais ao final do relatório
    if gaps:
        report_lines.append("================================")
        report_lines.append("===    Estatísticas Gerais   ===")
        report_lines.append("================================")
        report_lines.append(f"Média Gap de Custo:              {sum(gaps)/len(gaps):+.2f}%")
        report_lines.append(f"Média Diferença de Rotas:        {sum(diffs_rotas)/len(diffs_rotas):+.2f}")
        if ratios_exec:
            report_lines.append(f"Média Desempenho (Execução):     {sum(ratios_exec)/len(ratios_exec):+.2f}%")
        if ratios_ref:
            report_lines.append(f"Média Desempenho (Melhor Sol):   {sum(ratios_ref)/len(ratios_ref):+.2f}%")
    else:
        report_lines.append("⚠️  Nenhuma comparação foi possível. Verifique os caminhos e os nomes dos ficheiros.")

    # Escreve o conteúdo do relatório no ficheiro de saída
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print(f"\n✅ Relatório de comparação salvo em: {output_path}")

# Ponto de entrada do script
if __name__ == "__main__":
    # Definição dos caminhos para os diretórios de soluções
    dir_swap = r"E:\Etapa_03\solucoes"
    dir_prof = r"E:\Etapa_03\comparativo\G0"
    output_path = r"E:\Etapa_03\comparativo\comparativo_relatorio.txt"

    # Chama a função principal para iniciar o processo de comparação
    compare_solutions(dir_swap, dir_prof, output_path)
