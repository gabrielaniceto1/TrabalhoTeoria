import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Configurar estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)
plt.rcParams['font.size'] = 10

def parse_log_file(filename):
    """Analisa arquivo de log e retorna DataFrame com os dados."""
    data = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('43'):  # Ignora linhas vazias
                try:
                    # Remove número de linha (ex: "1. ", "2. ")
                    if '. ' in line:
                        line = line.split('. ', 1)[1]
                    
                    parts = line.split(',')
                    if len(parts) >= 3:
                        n = int(parts[0])
                        tempo = float(parts[1])
                        tipo = parts[2]
                        data.append({'n': n, 'tempo': tempo, 'tipo': tipo})
                except (ValueError, IndexError):
                    continue
    return pd.DataFrame(data)

def gerar_funcoes_complexidade(n_values):
    """Gera curvas teóricas de complexidade."""
    n_log_n = n_values * np.log(n_values)
    n_squared = n_values ** 2
    n_linear = n_values
    return n_log_n, n_squared, n_linear

def normalizar_curva(curva, dados_reais):
    """Normaliza a curva teórica para comparação com os dados reais."""
    if len(dados_reais) > 0 and max(curva) > 0:
        fator = max(dados_reais) / max(curva)
        return curva * fator
    return curva

# ============================================================================
# 1. LEITURA E PREPARAÇÃO DOS DADOS
# ============================================================================
print("Lendo arquivos de log...")
df_c = parse_log_file('log_c.txt')
df_python = parse_log_file('log_python.txt')

print(f"\nDados do C: {len(df_c)} registros")
print(f"Dados do Python: {len(df_python)} registros")

# ============================================================================
# 2. ANÁLISE ESTATÍSTICA
# ============================================================================
print("\n" + "="*70)
print("ANÁLISE ESTATÍSTICA - IMPLEMENTAÇÃO EM C")
print("="*70)

for tipo in ['pior', 'melhor', 'medio']:
    dados = df_c[df_c['tipo'] == tipo]['tempo']
    if len(dados) > 0:
        print(f"\n{tipo.upper()}:")
        print(f"  Média: {dados.mean():.9e} segundos")
        print(f"  Mediana: {dados.median():.9e} segundos")
        print(f"  Desvio padrão: {dados.std():.9e} segundos")
        print(f"  Mínimo: {dados.min():.9e} segundos")
        print(f"  Máximo: {dados.max():.9e} segundos")

print("\n" + "="*70)
print("ANÁLISE ESTATÍSTICA - IMPLEMENTAÇÃO EM PYTHON")
print("="*70)

for tipo in ['pior', 'melhor', 'medio']:
    dados = df_python[df_python['tipo'] == tipo]['tempo']
    if len(dados) > 0:
        print(f"\n{tipo.upper()}:")
        print(f"  Média: {dados.mean():.9e} segundos")
        print(f"  Mediana: {dados.median():.9e} segundos")
        print(f"  Desvio padrão: {dados.std():.9e} segundos")
        print(f"  Mínimo: {dados.min():.9e} segundos")
        print(f"  Máximo: {dados.max():.9e} segundos")

# ============================================================================
# 3. GRÁFICO 1: COMPARAÇÃO C vs PYTHON (Todas as Complexidades)
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Análise de Desempenho: C vs Python - QuickSort', fontsize=16, fontweight='bold')

tipos = ['pior', 'melhor', 'medio']
cores_c = {'pior': '#d62728', 'melhor': '#2ca02c', 'medio': '#1f77b4'}
cores_python = {'pior': '#ff7f0e', 'melhor': '#bcbd22', 'medio': '#17becf'}

# Primeiro gráfico: Escala Linear
ax = axes[0, 0]
for tipo in tipos:
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_python_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    ax.plot(df_c_tipo['n'], df_c_tipo['tempo'], 'o-', 
            label=f'C - {tipo}', color=cores_c[tipo], linewidth=2, markersize=6)
    ax.plot(df_python_tipo['n'], df_python_tipo['tempo'], 's--', 
            label=f'Python - {tipo}', color=cores_python[tipo], linewidth=2, markersize=6)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold')
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold')
ax.set_title('Escala Linear', fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

# Segundo gráfico: Escala Logarítmica
ax = axes[0, 1]
for tipo in tipos:
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_python_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    ax.loglog(df_c_tipo['n'], df_c_tipo['tempo'], 'o-', 
              label=f'C - {tipo}', color=cores_c[tipo], linewidth=2, markersize=6)
    ax.loglog(df_python_tipo['n'], df_python_tipo['tempo'], 's--', 
              label=f'Python - {tipo}', color=cores_python[tipo], linewidth=2, markersize=6)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold')
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold')
ax.set_title('Escala Logarítmica (Log-Log)', fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3, which='both')

# ============================================================================
# Gráficos: Comparação com Curvas Teóricas
# ============================================================================

# CASO PIOR (n²)
ax = axes[1, 0]
df_c_pior = df_c[df_c['tipo'] == 'pior'].sort_values('n')
df_python_pior = df_python[df_python['tipo'] == 'pior'].sort_values('n')

n_values = df_c_pior['n'].values.astype(float)
n_log_n, n_squared, n_linear = gerar_funcoes_complexidade(n_values)

# Normalizar curvas teóricas
n_squared_norm_c = normalizar_curva(n_squared, df_c_pior['tempo'].values)
n_squared_norm_py = normalizar_curva(n_squared, df_python_pior['tempo'].values)

ax.plot(n_values, df_c_pior['tempo'].values, 'o-', label='C - Pior Caso', 
        color='#d62728', linewidth=2, markersize=7)
ax.plot(n_values, df_python_pior['tempo'].values, 's--', label='Python - Pior Caso', 
        color='#ff7f0e', linewidth=2, markersize=7)
ax.plot(n_values, n_squared_norm_c, '^:', label='Curva O(n²) - C', 
        color='#d62728', linewidth=2, markersize=5, alpha=0.7)
ax.plot(n_values, n_squared_norm_py, 'v:', label='Curva O(n²) - Python', 
        color='#ff7f0e', linewidth=2, markersize=5, alpha=0.7)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold')
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold')
ax.set_title('Pior Caso - Comparação com O(n²)', fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

# CASO MÉDIO (n*log(n))
ax = axes[1, 1]
df_c_medio = df_c[df_c['tipo'] == 'medio'].sort_values('n')
df_python_medio = df_python[df_python['tipo'] == 'medio'].sort_values('n')

n_values = df_c_medio['n'].values.astype(float)
n_log_n, n_squared, n_linear = gerar_funcoes_complexidade(n_values)

n_log_n_norm_c = normalizar_curva(n_log_n, df_c_medio['tempo'].values)
n_log_n_norm_py = normalizar_curva(n_log_n, df_python_medio['tempo'].values)

ax.plot(n_values, df_c_medio['tempo'].values, 'o-', label='C - Caso Médio', 
        color='#1f77b4', linewidth=2, markersize=7)
ax.plot(n_values, df_python_medio['tempo'].values, 's--', label='Python - Caso Médio', 
        color='#17becf', linewidth=2, markersize=7)
ax.plot(n_values, n_log_n_norm_c, '^:', label='Curva O(n log n) - C', 
        color='#1f77b4', linewidth=2, markersize=5, alpha=0.7)
ax.plot(n_values, n_log_n_norm_py, 'v:', label='Curva O(n log n) - Python', 
        color='#17becf', linewidth=2, markersize=5, alpha=0.7)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold')
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold')
ax.set_title('Caso Médio - Comparação com O(n log n)', fontweight='bold')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analise_completa.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráfico salvo: analise_completa.png")

# ============================================================================
# 4. GRÁFICO 2: Crescimento da Complexidade (Detalhado)
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Análise de Complexidade - Crescimento de Tempo com n', fontsize=16, fontweight='bold')

# C - Todos os casos
ax = axes[0]
for tipo in tipos:
    df_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    ax.plot(df_tipo['n'], df_tipo['tempo'], 'o-', label=f'{tipo}', 
            color=cores_c[tipo], linewidth=2.5, markersize=8)

# Adicionar curvas teóricas normalizadas
n_values = df_c[df_c['tipo'] == 'pior'].sort_values('n')['n'].values.astype(float)
if len(n_values) > 0:
    n_log_n, n_squared, n_linear = gerar_funcoes_complexidade(n_values)
    
    # Normalizar para o pior caso
    pior_caso = df_c[df_c['tipo'] == 'pior'].sort_values('n')['tempo'].values
    n_squared_norm = normalizar_curva(n_squared, pior_caso)
    n_log_n_norm = normalizar_curva(n_log_n, df_c[df_c['tipo'] == 'medio'].sort_values('n')['tempo'].values)
    
    ax.plot(n_values, n_squared_norm, '^--', label='O(n²)', color='red', 
            linewidth=2, markersize=6, alpha=0.6)
    ax.plot(n_values, n_log_n_norm, 's--', label='O(n log n)', color='green', 
            linewidth=2, markersize=6, alpha=0.6)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold', fontsize=12)
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold', fontsize=12)
ax.set_title('Implementação em C', fontweight='bold', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

# Python - Todos os casos
ax = axes[1]
for tipo in tipos:
    df_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    ax.plot(df_tipo['n'], df_tipo['tempo'], 'o-', label=f'{tipo}', 
            color=cores_python[tipo], linewidth=2.5, markersize=8)

# Adicionar curvas teóricas normalizadas
n_values = df_python[df_python['tipo'] == 'pior'].sort_values('n')['n'].values.astype(float)
if len(n_values) > 0:
    n_log_n, n_squared, n_linear = gerar_funcoes_complexidade(n_values)
    
    # Normalizar para o pior caso
    pior_caso = df_python[df_python['tipo'] == 'pior'].sort_values('n')['tempo'].values
    n_squared_norm = normalizar_curva(n_squared, pior_caso)
    n_log_n_norm = normalizar_curva(n_log_n, df_python[df_python['tipo'] == 'medio'].sort_values('n')['tempo'].values)
    
    ax.plot(n_values, n_squared_norm, '^--', label='O(n²)', color='red', 
            linewidth=2, markersize=6, alpha=0.6)
    ax.plot(n_values, n_log_n_norm, 's--', label='O(n log n)', color='green', 
            linewidth=2, markersize=6, alpha=0.6)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold', fontsize=12)
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold', fontsize=12)
ax.set_title('Implementação em Python', fontweight='bold', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('crescimento_complexidade.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: crescimento_complexidade.png")

# ============================================================================
# 5. GRÁFICO 3: Escala Logarítmica (para visualizar melhor a linearidade)
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))
fig.suptitle('Análise em Escala Log-Log: Identificação de Complexidade', fontsize=14, fontweight='bold')

for tipo in tipos:
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_python_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    ax.loglog(df_c_tipo['n'], df_c_tipo['tempo'], 'o-', 
              label=f'C - {tipo}', color=cores_c[tipo], linewidth=2.5, markersize=8)
    ax.loglog(df_python_tipo['n'], df_python_tipo['tempo'], 's--', 
              label=f'Python - {tipo}', color=cores_python[tipo], linewidth=2.5, markersize=8)

# Adicionar linhas de referência
n_min, n_max = 1, 10000
n_ref = np.array([n_min, n_max])
norm_factor_quad = 1e-8
norm_factor_log = 1e-7

ax.loglog(n_ref, norm_factor_quad * (n_ref ** 2), 'r--', label='Referência O(n²)', 
          linewidth=1.5, alpha=0.6)
ax.loglog(n_ref, norm_factor_log * (n_ref * np.log(n_ref)), 'g--', label='Referência O(n log n)', 
          linewidth=1.5, alpha=0.6)

ax.set_xlabel('Tamanho do Array (n)', fontweight='bold', fontsize=12)
ax.set_ylabel('Tempo de Execução (segundos)', fontweight='bold', fontsize=12)
ax.legend(loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3, which='both', linestyle=':')
plt.tight_layout()
plt.savefig('escala_logaritmica.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: escala_logaritmica.png")

# ============================================================================
# 6. GRÁFICO 4: Taxa de Crescimento (Razão entre tempos)
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Taxa de Crescimento: Razão de Tempo entre Incrementos de n', fontsize=14, fontweight='bold')

# C
ax = axes[0]
for tipo in tipos:
    df_tipo = df_c[df_c['tipo'] == tipo].sort_values('n').reset_index(drop=True)
    if len(df_tipo) > 1:
        razoes = []
        n_values = []
        for i in range(1, len(df_tipo)):
            if df_tipo.loc[i-1, 'tempo'] > 1e-12:  # Evitar divisão por zero
                razao = df_tipo.loc[i, 'tempo'] / df_tipo.loc[i-1, 'tempo']
                razoes.append(razao)
                n_values.append(df_tipo.loc[i, 'n'])
        
        if razoes:
            ax.plot(n_values, razoes, 'o-', label=f'{tipo}', color=cores_c[tipo], 
                    linewidth=2, markersize=7)

ax.axhline(y=4, color='red', linestyle='--', linewidth=1.5, label='Razão esperada (≈4 para n²)', alpha=0.7)
ax.set_xlabel('Tamanho do Array (n)', fontweight='bold', fontsize=12)
ax.set_ylabel('Razão de Tempo (t_i / t_i-1)', fontweight='bold', fontsize=12)
ax.set_title('Taxa de Crescimento - C', fontweight='bold', fontsize=12)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# Python
ax = axes[1]
for tipo in tipos:
    df_tipo = df_python[df_python['tipo'] == tipo].sort_values('n').reset_index(drop=True)
    if len(df_tipo) > 1:
        razoes = []
        n_values = []
        for i in range(1, len(df_tipo)):
            if df_tipo.loc[i-1, 'tempo'] > 1e-12:  # Evitar divisão por zero
                razao = df_tipo.loc[i, 'tempo'] / df_tipo.loc[i-1, 'tempo']
                razoes.append(razao)
                n_values.append(df_tipo.loc[i, 'n'])
        
        if razoes:
            ax.plot(n_values, razoes, 'o-', label=f'{tipo}', color=cores_python[tipo], 
                    linewidth=2, markersize=7)

ax.axhline(y=4, color='red', linestyle='--', linewidth=1.5, label='Razão esperada (≈4 para n²)', alpha=0.7)
ax.set_xlabel('Tamanho do Array (n)', fontweight='bold', fontsize=12)
ax.set_ylabel('Razão de Tempo (t_i / t_i-1)', fontweight='bold', fontsize=12)
ax.set_title('Taxa de Crescimento - Python', fontweight='bold', fontsize=12)
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('taxa_crescimento.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: taxa_crescimento.png")

# ============================================================================
# 7. RESUMO COMPARATIVO
# ============================================================================
print("\n" + "="*70)
print("RESUMO COMPARATIVO")
print("="*70)

print("\nTempo de Execução para n = 8192:")
c_pior_8192 = df_c[(df_c['n'] == 8192) & (df_c['tipo'] == 'pior')]['tempo'].values
py_pior_8192 = df_python[(df_python['n'] == 8192) & (df_python['tipo'] == 'pior')]['tempo'].values

if len(c_pior_8192) > 0 and len(py_pior_8192) > 0:
    speedup = py_pior_8192[0] / c_pior_8192[0]
    print(f"  C (Pior Caso):      {c_pior_8192[0]:.9f} segundos")
    print(f"  Python (Pior Caso): {py_pior_8192[0]:.9f} segundos")
    print(f"  Python é {speedup:.2f}x mais lento que C")

print("\n" + "="*70)
print("Análise completa! Todos os gráficos foram salvos.")
print("="*70)
print("\nArquivos gerados:")
print("  1. analise_completa.png - Comparação C vs Python com curvas teóricas")
print("  2. crescimento_complexidade.png - Gráficos de crescimento")
print("  3. escala_logaritmica.png - Análise em escala log-log")
print("  4. taxa_crescimento.png - Taxa de crescimento entre incrementos")
