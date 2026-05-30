import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 9

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================

def parse_log_file(filename):
    """Analisa arquivo de log e retorna DataFrame com os dados."""
    data = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('43'):
                try:
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

def funcao_n_log_n(n, a):
    """Função O(n log n)."""
    return a * n * np.log(n)

def funcao_n_squared(n, a):
    """Função O(n²)."""
    return a * n ** 2

def funcao_n_linear(n, a):
    """Função O(n)."""
    return a * n

def ajustar_curva(n_values, y_values, func, p0):
    """Ajusta uma função aos dados."""
    try:
        params, _ = curve_fit(func, n_values, y_values, p0=p0, maxfev=10000)
        return params, func(n_values, *params)
    except:
        return None, None

def calcular_r_squared(y_real, y_pred):
    """Calcula R² (coeficiente de determinação)."""
    if len(y_real) < 2 or y_pred is None:
        return 0
    ss_res = np.sum((y_real - y_pred) ** 2)
    ss_tot = np.sum((y_real - np.mean(y_real)) ** 2)
    return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

# ============================================================================
# 1. LEITURA DOS DADOS
# ============================================================================
print("\n" + "="*80)
print("ANÁLISE AVANÇADA DE QUICKSORT - Casos Melhor, Médio e Pior")
print("="*80)

print("\nLendo arquivos de log...")
df_c = parse_log_file('log_c.txt')
df_python = parse_log_file('log_python.txt')

print(f"[OK] C: {len(df_c)} registros")
print(f"[OK] Python: {len(df_python)} registros")

# ============================================================================
# 2. ANÁLISE ESTATÍSTICA DETALHADA
# ============================================================================
print("\n" + "="*80)
print("ANÁLISE ESTATÍSTICA DETALHADA")
print("="*80)

for impl_name, df in [("C", df_c), ("Python", df_python)]:
    print(f"\n{impl_name.upper()}")
    print("-" * 80)
    
    for tipo in ['melhor', 'medio', 'pior']:
        dados = df[df['tipo'] == tipo]['tempo']
        if len(dados) > 0:
            print(f"\n  {tipo.upper()}:")
            print(f"    Contagem:    {len(dados)}")
            print(f"    Média:       {dados.mean():.9e} s")
            print(f"    Mediana:     {dados.median():.9e} s")
            print(f"    Desvio Pad.: {dados.std():.9e} s")
            print(f"    Min:         {dados.min():.9e} s")
            print(f"    Max:         {dados.max():.9e} s")
            print(f"    Amplitude:   {dados.max() - dados.min():.9e} s")
            print(f"    Quartil 25%: {dados.quantile(0.25):.9e} s")
            print(f"    Quartil 75%: {dados.quantile(0.75):.9e} s")

# ============================================================================
# 3. AJUSTE DE CURVAS E ANÁLISE DE COMPLEXIDADE
# ============================================================================
print("\n" + "="*80)
print("AJUSTE DE CURVAS E ANÁLISE DE COMPLEXIDADE")
print("="*80)

for impl_name, df in [("C", df_c), ("Python", df_python)]:
    print(f"\n{impl_name.upper()}")
    print("-" * 80)
    
    # Pior caso (O(n²))
    df_pior = df[df['tipo'] == 'pior'].sort_values('n')
    if len(df_pior) > 2:
        n_vals = df_pior['n'].values.astype(float)
        y_vals = df_pior['tempo'].values
        
        params, y_pred = ajustar_curva(n_vals, y_vals, funcao_n_squared, [1e-6])
        r2 = calcular_r_squared(y_vals, y_pred)
        print(f"\n  PIOR CASO (esperado O(n²)):")
        print(f"    Coeficiente a: {params[0]:.9e}" if params else "    Falha no ajuste")
        print(f"    R² (qualidade): {r2:.6f}" if params else "    N/A")
    
    # Caso médio (O(n log n))
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    if len(df_medio) > 2:
        n_vals = df_medio['n'].values.astype(float)
        y_vals = df_medio['tempo'].values
        
        params, y_pred = ajustar_curva(n_vals, y_vals, funcao_n_log_n, [1e-7])
        r2 = calcular_r_squared(y_vals, y_pred)
        print(f"\n  CASO MÉDIO (esperado O(n log n)):")
        print(f"    Coeficiente a: {params[0]:.9e}" if params else "    Falha no ajuste")
        print(f"    R² (qualidade): {r2:.6f}" if params else "    N/A")
    
    # Melhor caso (O(n) ou O(n log n))
    df_melhor = df[df['tipo'] == 'melhor'].sort_values('n')
    if len(df_melhor) > 2:
        n_vals = df_melhor['n'].values.astype(float)
        y_vals = df_melhor['tempo'].values
        
        # Tentar O(n log n)
        params, y_pred = ajustar_curva(n_vals, y_vals, funcao_n_log_n, [1e-8])
        r2 = calcular_r_squared(y_vals, y_pred)
        print(f"\n  MELHOR CASO:")
        print(f"    Ajuste O(n log n) - Coef: {params[0]:.9e}, R²: {r2:.6f}" if params else "    N/A")

# ============================================================================
# 4. RAZÕES E COMPARAÇÕES ENTRE CASOS
# ============================================================================
print("\n" + "="*80)
print("COMPARAÇÃO: RAZÕES ENTRE CASOS")
print("="*80)

for impl_name, df in [("C", df_c), ("Python", df_python)]:
    print(f"\n{impl_name.upper()}")
    print("-" * 80)
    print("\nRazão: Pior Caso / Caso Médio (esperado: crescer com n para O(n²) vs O(n log n))")
    
    df_pior = df[df['tipo'] == 'pior'].sort_values('n')
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    
    for n in df_pior['n'].values:
        t_pior = df_pior[df_pior['n'] == n]['tempo'].values
        t_medio = df_medio[df_medio['n'] == n]['tempo'].values
        
        if len(t_pior) > 0 and len(t_medio) > 0 and t_medio[0] > 0:
            razao = t_pior[0] / t_medio[0]
            print(f"  n={n:5d}: {razao:8.2f}x")

print("\nRazão: Pior Caso / Melhor Caso (mostra otimização do melhor cenário)")
for impl_name, df in [("C", df_c), ("Python", df_python)]:
    print(f"\n{impl_name.upper()}")
    print("-" * 80)
    
    df_pior = df[df['tipo'] == 'pior'].sort_values('n')
    df_melhor = df[df['tipo'] == 'melhor'].sort_values('n')
    
    for n in df_pior['n'].values:
        t_pior = df_pior[df_pior['n'] == n]['tempo'].values
        t_melhor = df_melhor[df_melhor['n'] == n]['tempo'].values
        
        if len(t_pior) > 0 and len(t_melhor) > 0 and t_melhor[0] > 1e-12:
            razao = t_pior[0] / t_melhor[0]
            print(f"  n={n:5d}: {razao:10.2f}x")

# ============================================================================
# 5. GRÁFICOS - Figura 1: Comparação Linear vs Log entre Casos
# ============================================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Análise Detalhada: Comparação Melhor vs Médio vs Pior', 
             fontsize=16, fontweight='bold')

for idx, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    # Gráfico Linear
    ax = axes[idx, 0]
    for tipo, cor, marcador in [('melhor', '#2ca02c', 'o'), 
                                 ('medio', '#1f77b4', 's'), 
                                 ('pior', '#d62728', '^')]:
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        ax.plot(df_tipo['n'], df_tipo['tempo'], marcador + '-', label=tipo, 
                color=cor, linewidth=2.5, markersize=7)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name} - Linear', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Gráfico Log-Log
    ax = axes[idx, 1]
    for tipo, cor, marcador in [('melhor', '#2ca02c', 'o'), 
                                 ('medio', '#1f77b4', 's'), 
                                 ('pior', '#d62728', '^')]:
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        ax.loglog(df_tipo['n'], df_tipo['tempo'], marcador + '-', label=tipo, 
                  color=cor, linewidth=2.5, markersize=7)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name} - Log-Log', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    # Gráfico Normalizado (relativo ao melhor caso)
    ax = axes[idx, 2]
    for tipo, cor, marcador in [('melhor', '#2ca02c', 'o'), 
                                 ('medio', '#1f77b4', 's'), 
                                 ('pior', '#d62728', '^')]:
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        df_melhor_norm = df[df['tipo'] == 'melhor'].sort_values('n')
        
        # Normalizar pelo melhor caso
        razoes = []
        for i, n in enumerate(df_tipo['n'].values):
            t_norm = df_melhor_norm[df_melhor_norm['n'] == n]['tempo'].values
            if len(t_norm) > 0 and t_norm[0] > 0:
                razoes.append(df_tipo.iloc[i]['tempo'] / t_norm[0])
            else:
                razoes.append(1)
        
        ax.plot(df_tipo['n'].values, razoes, marcador + '-', label=tipo, 
                color=cor, linewidth=2.5, markersize=7)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Razão (relativo ao melhor)', fontweight='bold')
    ax.set_title(f'{impl_name} - Normalizado', fontweight='bold')
    ax.set_yscale('log')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('01_comparacao_detalhada.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 01_comparacao_detalhada.png")
plt.close()

# ============================================================================
# 6. GRÁFICOS - Figura 2: Diferença Relativa Melhor vs Médio
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Diferença Entre Melhor e Caso Médio: Visualizando Otimizações',
             fontsize=16, fontweight='bold')

for idx, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    ax = axes[idx]
    
    df_melhor = df[df['tipo'] == 'melhor'].sort_values('n')
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    
    diferencas = []
    n_vals = []
    
    for n in df_melhor['n'].values:
        t_melhor = df_melhor[df_melhor['n'] == n]['tempo'].values
        t_medio = df_medio[df_medio['n'] == n]['tempo'].values
        
        if len(t_melhor) > 0 and len(t_medio) > 0 and t_melhor[0] > 0:
            # Percentual de diferença
            pct_diff = ((t_medio[0] - t_melhor[0]) / t_melhor[0]) * 100
            diferencas.append(pct_diff)
            n_vals.append(n)
    
    ax.bar(range(len(n_vals)), diferencas, color='#ff7f0e', alpha=0.7, edgecolor='black')
    ax.set_xticks(range(len(n_vals)))
    ax.set_xticklabels([f'{n}' for n in n_vals], rotation=45)
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Diferença Percentual (%)', fontweight='bold')
    ax.set_title(f'{impl_name} - (Médio - Melhor) / Melhor × 100', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('02_diferenca_melhor_medio.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 02_diferenca_melhor_medio.png")
plt.close()

# ============================================================================
# 7. GRÁFICOS - Figura 3: Ajuste de Curvas com Funções Teóricas
# ============================================================================
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Ajuste de Curvas: Dados vs Funções Teóricas',
             fontsize=16, fontweight='bold')

for idx, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    casos = [('melhor', 'O(n log n)', funcao_n_log_n, 1e-8),
             ('medio', 'O(n log n)', funcao_n_log_n, 1e-7),
             ('pior', 'O(n²)', funcao_n_squared, 1e-6)]
    
    for col, (tipo, complexidade, func, p0) in enumerate(casos):
        ax = axes[idx, col]
        
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        n_vals = df_tipo['n'].values.astype(float)
        y_vals = df_tipo['tempo'].values
        
        params, y_pred = ajustar_curva(n_vals, y_vals, func, [p0])
        r2 = calcular_r_squared(y_vals, y_pred)
        
        # Plotar dados reais
        ax.plot(n_vals, y_vals, 'o-', label='Dados Reais', 
                color='#1f77b4', linewidth=2.5, markersize=7)
        
        # Plotar curva ajustada
        if params is not None:
            ax.plot(n_vals, y_pred, 's--', label=f'Ajuste (R²={r2:.4f})', 
                    color='#d62728', linewidth=2.5, markersize=6)
        
        ax.set_xlabel('Tamanho (n)', fontweight='bold')
        ax.set_ylabel('Tempo (s)', fontweight='bold')
        ax.set_title(f'{impl_name} - {tipo} ({complexidade})', fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('03_ajuste_curvas.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 03_ajuste_curvas.png")
plt.close()

# ============================================================================
# 8. GRÁFICOS - Figura 4: Razões Entre Casos
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Razões Entre Casos de Execução',
             fontsize=16, fontweight='bold')

for idx, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    ax = axes[idx]
    
    df_pior = df[df['tipo'] == 'pior'].sort_values('n')
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    df_melhor = df[df['tipo'] == 'melhor'].sort_values('n')
    
    razoes_pior_medio = []
    razoes_pior_melhor = []
    n_vals = []
    
    for n in df_pior['n'].values:
        t_pior = df_pior[df_pior['n'] == n]['tempo'].values
        t_medio = df_medio[df_medio['n'] == n]['tempo'].values
        t_melhor = df_melhor[df_melhor['n'] == n]['tempo'].values
        
        if len(t_pior) > 0 and len(t_medio) > 0 and len(t_melhor) > 0:
            if t_medio[0] > 0 and t_melhor[0] > 0:
                razoes_pior_medio.append(t_pior[0] / t_medio[0])
                razoes_pior_melhor.append(t_pior[0] / t_melhor[0])
                n_vals.append(n)
    
    x = np.arange(len(n_vals))
    width = 0.35
    
    ax.bar(x - width/2, razoes_pior_medio, width, label='Pior / Médio', 
           color='#ff7f0e', alpha=0.8, edgecolor='black')
    ax.bar(x + width/2, razoes_pior_melhor, width, label='Pior / Melhor', 
           color='#d62728', alpha=0.8, edgecolor='black')
    
    ax.set_xticks(x)
    ax.set_xticklabels([f'{n}' for n in n_vals], rotation=45)
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Razão (Pior / Outro)', fontweight='bold')
    ax.set_title(f'{impl_name}', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')

plt.tight_layout()
plt.savefig('04_razoes_casos.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 04_razoes_casos.png")
plt.close()

# ============================================================================
# 9. GRÁFICOS - Figura 5: Desvios e Variabilidade
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Distribuição de Tempos por Tipo de Caso',
             fontsize=16, fontweight='bold')

for idx, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    ax = axes[idx]
    
    dados = [df[df['tipo'] == tipo]['tempo'].values for tipo in ['melhor', 'medio', 'pior']]
    
    bp = ax.boxplot(dados, labels=['Melhor', 'Médio', 'Pior'], patch_artist=True)
    
    cores = ['#2ca02c', '#1f77b4', '#d62728']
    for patch, cor in zip(bp['boxes'], cores):
        patch.set_facecolor(cor)
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name}', fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_yscale('log')

plt.tight_layout()
plt.savefig('05_distribuicao_boxplot.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 05_distribuicao_boxplot.png")
plt.close()

# ============================================================================
# 10. GRÁFICOS - Figura 6: Comparação C vs Python (Overlay)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Comparação Direta: C vs Python para Cada Caso',
             fontsize=16, fontweight='bold')

for col, tipo in enumerate(['melhor', 'medio', 'pior']):
    ax = axes[col]
    
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_py_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    ax.plot(df_c_tipo['n'], df_c_tipo['tempo'], 'o-', label='C', 
            color='#1f77b4', linewidth=2.5, markersize=8)
    ax.plot(df_py_tipo['n'], df_py_tipo['tempo'], 's-', label='Python', 
            color='#ff7f0e', linewidth=2.5, markersize=8)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{tipo.upper()}', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    ax.set_xscale('log')

plt.tight_layout()
plt.savefig('06_c_vs_python_casos.png', dpi=300, bbox_inches='tight')
print("✓ Gráfico salvo: 06_c_vs_python_casos.png")
plt.close()

# ============================================================================
# 11. RESUMO FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMO EXECUTIVO")
print("="*80)

print("\nVELOCIDADE RELATIVA (Python vs C) - Pior Caso, n=8192:")
c_pior_max = df_c[df_c['tipo'] == 'pior']['tempo'].max()
py_pior_max = df_python[df_python['tipo'] == 'pior']['tempo'].max()
print(f"  C:      {c_pior_max:.6e} s")
print(f"  Python: {py_pior_max:.6e} s")
print(f"  → Python é {py_pior_max/c_pior_max:.2f}x mais lento")

print("\nTEMPO MÉDIO POR TIPO (C):")
for tipo in ['melhor', 'medio', 'pior']:
    media = df_c[df_c['tipo'] == tipo]['tempo'].mean()
    print(f"  {tipo.upper():10s}: {media:.9e} s")

print("\nTEMPO MÉDIO POR TIPO (Python):")
for tipo in ['melhor', 'medio', 'pior']:
    media = df_python[df_python['tipo'] == tipo]['tempo'].mean()
    print(f"  {tipo.upper():10s}: {media:.9e} s")

print("\n" + "="*80)
print("ANÁLISE CONCLUÍDA - 6 GRÁFICOS GERADOS")
print("="*80)
print("""
Arquivos gerados:
  1. 01_comparacao_detalhada.png - Linear, Log-Log e Normalizado
  2. 02_diferenca_melhor_medio.png - % Diferença Melhor vs Médio
  3. 03_ajuste_curvas.png - Ajuste com funções teóricas
  4. 04_razoes_casos.png - Razões entre casos
  5. 05_distribuicao_boxplot.png - Box plots de distribuição
  6. 06_c_vs_python_casos.png - C vs Python por tipo
""")
