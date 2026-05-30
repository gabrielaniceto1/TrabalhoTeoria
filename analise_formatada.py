# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy import stats
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACAO DE ESTILO
# ============================================================================
sns.set_style("whitegrid")
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# Paleta de cores consistente
CORES = {
    'melhor': '#2ecc71',    # Verde
    'medio': '#3498db',     # Azul
    'pior': '#e74c3c',      # Vermelho
    'c': '#34495e',         # Cinza escuro
    'python': '#f39c12'     # Laranja
}

MARCADORES = {
    'melhor': 'o',
    'medio': 's',
    'pior': '^'
}

# ============================================================================
# FUNCOES AUXILIARES
# ============================================================================

def parse_log_file(filename):
    """Parse log file and return DataFrame."""
    data = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('301'):
                try:
                    if '. ' in line:
                        line = line.split('. ', 1)[1]
                    
                    parts = line.split(',')
                    if len(parts) >= 3:
                        n = int(parts[0])
                        tempo = float(parts[1])
                        tipo = parts[2].strip()
                        data.append({'n': n, 'tempo': tempo, 'tipo': tipo})
                except (ValueError, IndexError):
                    continue
    return pd.DataFrame(data)

def funcao_n_log_n(n, a):
    return a * n * np.log(n)

def funcao_n_squared(n, a):
    return a * n ** 2

def funcao_n_linear(n, a):
    return a * n

def ajustar_curva(n_values, y_values, func, p0):
    try:
        params, _ = curve_fit(func, n_values, y_values, p0=p0, maxfev=10000)
        return params, func(n_values, *params)
    except:
        return None, None

def calcular_r_squared(y_real, y_pred):
    if len(y_real) < 2 or y_pred is None:
        return 0
    ss_res = np.sum((y_real - y_pred) ** 2)
    ss_tot = np.sum((y_real - np.mean(y_real)) ** 2)
    return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

def formatar_numero(num, precisao=2):
    """Formata numero em notacao cientifica ou decimal."""
    if num < 1e-3:
        return f"{num:.2e}"
    elif num < 1:
        return f"{num:.6f}"
    else:
        return f"{num:.4f}"

# ============================================================================
# 1. LEITURA DOS DADOS
# ============================================================================
print("\n" + "="*80)
print("ANALISE AVANCADA DE QUICKSORT - Dados Atualizados")
print("="*80)

print("\nCarregando arquivos de log...")
df_c = parse_log_file('log_c.txt')
df_python = parse_log_file('log_python.txt')

print(f"[OK] Implementacao C: {len(df_c)} registros")
print(f"[OK] Implementacao Python: {len(df_python)} registros")

# Mostrar estatisticas basicas
print(f"\nIntervalo de n:")
print(f"  C:      {df_c['n'].min()} a {df_c['n'].max()}")
print(f"  Python: {df_python['n'].min()} a {df_python['n'].max()}")

# ============================================================================
# 2. ANALISE ESTATISTICA
# ============================================================================
print("\n" + "="*80)
print("ANALISE ESTATISTICA")
print("="*80)

def print_stats(name, df):
    print(f"\n{name}")
    print("-"*80)
    
    for tipo in ['melhor', 'medio', 'pior']:
        dados = df[df['tipo'] == tipo]['tempo']
        if len(dados) > 0:
            print(f"\n  {tipo.upper():10s} ({len(dados)} medidas):")
            print(f"    Media:       {formatar_numero(dados.mean()):>15s} s")
            print(f"    Mediana:     {formatar_numero(dados.median()):>15s} s")
            print(f"    Desvio Pad.: {formatar_numero(dados.std()):>15s} s")
            print(f"    Min:         {formatar_numero(dados.min()):>15s} s")
            print(f"    Max:         {formatar_numero(dados.max()):>15s} s")
            print(f"    Q1:          {formatar_numero(dados.quantile(0.25)):>15s} s")
            print(f"    Q3:          {formatar_numero(dados.quantile(0.75)):>15s} s")

print_stats("IMPLEMENTACAO EM C", df_c)
print_stats("IMPLEMENTACAO EM PYTHON", df_python)

# ============================================================================
# 3. COMPARACAO C vs PYTHON
# ============================================================================
print("\n" + "="*80)
print("COMPARACAO: C vs PYTHON")
print("="*80)

for tipo in ['melhor', 'medio', 'pior']:
    print(f"\n{tipo.upper()}:")
    print("-"*80)
    print(f"{'n':>6s} | {'C (s)':>12s} | {'Python (s)':>14s} | {'Razao':>8s}")
    print("-"*80)
    
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_py_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    for n in df_c_tipo['n'].unique()[:20]:  # Mostrar primeiros 20
        tc = df_c_tipo[df_c_tipo['n'] == n]['tempo'].values
        tp = df_py_tipo[df_py_tipo['n'] == n]['tempo'].values
        
        if len(tc) > 0 and len(tp) > 0:
            razao = tp[0] / tc[0] if tc[0] > 0 else np.inf
            print(f"{n:6d} | {formatar_numero(tc[0]):>12s} | {formatar_numero(tp[0]):>14s} | {razao:8.2f}x")

# ============================================================================
# 4. GRAFICOS PRINCIPAIS
# ============================================================================

# FIGURA 1: Visao Geral Completa
fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)

fig.suptitle('Analise Completa: QuickSort em C vs Python\nComparacao Melhor, Medio e Pior Caso',
             fontsize=16, fontweight='bold', y=0.995)

# Linha 1: Graficos Lineares por Implementacao
for col, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    ax = fig.add_subplot(gs[0, col])
    
    for tipo in ['melhor', 'medio', 'pior']:
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        ax.plot(df_tipo['n'], df_tipo['tempo'], 
               marker=MARCADORES[tipo], markersize=4, linewidth=2,
               label=tipo, color=CORES[tipo], alpha=0.8)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name} - Escala Linear', fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)

# Comparacao direta C vs Python
ax = fig.add_subplot(gs[0, 2])
for tipo in ['melhor', 'medio', 'pior']:
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_py_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    ax.plot(df_c_tipo['n'], df_c_tipo['tempo'],
           marker=MARCADORES[tipo], markersize=4, linewidth=2,
           label=f'C - {tipo}', color=CORES[tipo], alpha=0.7)
    ax.plot(df_py_tipo['n'], df_py_tipo['tempo'],
           marker=MARCADORES[tipo], markersize=4, linewidth=2, linestyle='--',
           label=f'Python - {tipo}', color=CORES[tipo], alpha=0.5)

ax.set_xlabel('Tamanho (n)', fontweight='bold')
ax.set_ylabel('Tempo (s)', fontweight='bold')
ax.set_title('C vs Python - Overlay', fontweight='bold')
ax.legend(loc='upper left', fontsize=8)
ax.grid(True, alpha=0.3)

# Linha 2: Log-Log
for col, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    ax = fig.add_subplot(gs[1, col])
    
    for tipo in ['melhor', 'medio', 'pior']:
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        ax.loglog(df_tipo['n'], df_tipo['tempo'],
                 marker=MARCADORES[tipo], markersize=4, linewidth=2,
                 label=tipo, color=CORES[tipo], alpha=0.8)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name} - Log-Log', fontweight='bold')
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, which='both')

# Razao Pior/Medio para mostrar diferenca
ax = fig.add_subplot(gs[1, 2])
for impl_name, df, cor in [("C", df_c, CORES['c']), ("Python", df_python, CORES['python'])]:
    df_pior = df[df['tipo'] == 'pior'].sort_values('n')
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    
    razoes = []
    n_vals = []
    for n in df_pior['n'].values:
        tp = df_pior[df_pior['n'] == n]['tempo'].values
        tm = df_medio[df_medio['n'] == n]['tempo'].values
        
        if len(tp) > 0 and len(tm) > 0 and tm[0] > 0:
            razoes.append(tp[0] / tm[0])
            n_vals.append(n)
    
    ax.semilogy(n_vals, razoes, marker='o', linewidth=2, markersize=5,
               label=impl_name, color=cor, alpha=0.8)

ax.set_xlabel('Tamanho (n)', fontweight='bold')
ax.set_ylabel('Razao (Pior/Medio)', fontweight='bold')
ax.set_title('Diferenca entre Casos', fontweight='bold')
ax.legend(fontsize=9)
ax.grid(True, alpha=0.3, which='both')

# Linha 3: Diferencas percentuais e distribuicoes
for col, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    ax = fig.add_subplot(gs[2, col])
    
    df_melhor = df[df['tipo'] == 'melhor'].sort_values('n')
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    
    pct_diffs = []
    n_vals = []
    
    for n in df_melhor['n'].unique():
        tm = df_melhor[df_melhor['n'] == n]['tempo'].values
        tmed = df_medio[df_medio['n'] == n]['tempo'].values
        
        if len(tm) > 0 and len(tmed) > 0 and tm[0] > 0:
            pct = ((tmed[0] - tm[0]) / tm[0]) * 100
            pct_diffs.append(pct)
            n_vals.append(n)
    
    # Plotar a cada 5 pontos para nao ficar muito denso
    step = max(1, len(n_vals) // 15)
    n_plot = n_vals[::step]
    pct_plot = pct_diffs[::step]
    
    ax.scatter(n_plot, pct_plot, s=50, alpha=0.6, color=CORES['medio'])
    ax.plot(n_plot, pct_plot, linewidth=2, color=CORES['medio'], alpha=0.6)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Diferenca (%)', fontweight='bold')
    ax.set_title(f'{impl_name} - Medio vs Melhor (%)', fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=8))

# Terceira coluna: Box plots
ax = fig.add_subplot(gs[2, 2])
dados_box = []
labels_box = []

for impl_name, df in [("C", df_c), ("Python", df_python)]:
    for tipo in ['melhor', 'medio', 'pior']:
        dados = df[df['tipo'] == tipo]['tempo'].values
        dados_box.append(dados)
        labels_box.append(f'{impl_name}\n{tipo}')

bp = ax.boxplot(dados_box, labels=labels_box, patch_artist=True)

for i, patch in enumerate(bp['boxes']):
    tipo_idx = i % 3
    tipos_order = ['melhor', 'medio', 'pior']
    patch.set_facecolor(CORES[tipos_order[tipo_idx]])
    patch.set_alpha(0.6)

ax.set_ylabel('Tempo (s)', fontweight='bold')
ax.set_title('Distribuicao de Tempos', fontweight='bold')
ax.set_yscale('log')
ax.grid(True, alpha=0.3, axis='y')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)

plt.savefig('01_visao_geral_completa.png', dpi=300, bbox_inches='tight')
print("\n[OK] Grafico: 01_visao_geral_completa.png")
plt.close()

# FIGURA 2: Zoom em Melhor vs Medio
fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Analise Detalhada: Melhor vs Caso Medio',
             fontsize=14, fontweight='bold')

for row, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    # Grafico Linear
    ax = axes[row, 0]
    df_melhor = df[df['tipo'] == 'melhor'].sort_values('n')
    df_medio = df[df['tipo'] == 'medio'].sort_values('n')
    
    ax.plot(df_melhor['n'], df_melhor['tempo'], 'o-', label='Melhor', 
           color=CORES['melhor'], linewidth=2.5, markersize=5)
    ax.plot(df_medio['n'], df_medio['tempo'], 's-', label='Medio',
           color=CORES['medio'], linewidth=2.5, markersize=5)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name} - Linear', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Grafico Log-Log
    ax = axes[row, 1]
    ax.loglog(df_melhor['n'], df_melhor['tempo'], 'o-', label='Melhor',
             color=CORES['melhor'], linewidth=2.5, markersize=5)
    ax.loglog(df_medio['n'], df_medio['tempo'], 's-', label='Medio',
             color=CORES['medio'], linewidth=2.5, markersize=5)
    
    # Adicionar referencia O(n log n)
    n_ref = df_melhor['n'].values.astype(float)
    if len(n_ref) > 1:
        y_ref = 1e-8 * n_ref * np.log(n_ref)
        ax.loglog(n_ref, y_ref, '--', label='Ref O(n log n)', 
                 color='gray', linewidth=1.5, alpha=0.5)
    
    ax.set_xlabel('Tamanho (n)', fontweight='bold')
    ax.set_ylabel('Tempo (s)', fontweight='bold')
    ax.set_title(f'{impl_name} - Log-Log', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

plt.tight_layout()
plt.savefig('02_zoom_melhor_vs_medio.png', dpi=300, bbox_inches='tight')
print("[OK] Grafico: 02_zoom_melhor_vs_medio.png")
plt.close()

# FIGURA 3: Comparacao com Curvas Teoricas
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Ajuste de Curvas: Dados Reais vs Funcoes Teoricas',
             fontsize=14, fontweight='bold')

for row, (impl_name, df) in enumerate([("C", df_c), ("Python", df_python)]):
    casos = [('melhor', funcao_n_log_n, 1e-9),
             ('medio', funcao_n_log_n, 1e-8),
             ('pior', funcao_n_squared, 1e-7)]
    
    for col, (tipo, func, p0) in enumerate(casos):
        ax = axes[row, col]
        
        df_tipo = df[df['tipo'] == tipo].sort_values('n')
        n_vals = df_tipo['n'].values.astype(float)
        y_vals = df_tipo['tempo'].values
        
        params, y_pred = ajustar_curva(n_vals, y_vals, func, [p0])
        r2 = calcular_r_squared(y_vals, y_pred)
        
        # Dados
        ax.scatter(n_vals, y_vals, s=30, alpha=0.6, color=CORES[tipo], label='Dados')
        
        # Curva ajustada
        if params is not None and y_pred is not None:
            n_smooth = np.linspace(n_vals.min(), n_vals.max(), 200)
            y_smooth = func(n_smooth, params[0])
            ax.plot(n_smooth, y_smooth, '--', linewidth=2.5,
                   color=CORES[tipo], label=f'Ajuste (R²={r2:.4f})', alpha=0.8)
        
        ax.set_xlabel('Tamanho (n)', fontweight='bold')
        ax.set_ylabel('Tempo (s)', fontweight='bold')
        ax.set_title(f'{impl_name} - {tipo.upper()}', fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('03_ajuste_curvas_teoricas.png', dpi=300, bbox_inches='tight')
print("[OK] Grafico: 03_ajuste_curvas_teoricas.png")
plt.close()

# FIGURA 4: Velocidade Relativa (C vs Python)
fig, ax = plt.subplots(figsize=(14, 8))

velocidades = {}
for tipo in ['melhor', 'medio', 'pior']:
    df_c_tipo = df_c[df_c['tipo'] == tipo].sort_values('n')
    df_py_tipo = df_python[df_python['tipo'] == tipo].sort_values('n')
    
    n_vals = []
    razoes = []
    
    for n in df_c_tipo['n'].unique()[:50]:  # Limitar para nao ficar muito denso
        tc = df_c_tipo[df_c_tipo['n'] == n]['tempo'].values
        tp = df_py_tipo[df_py_tipo['n'] == n]['tempo'].values
        
        if len(tc) > 0 and len(tp) > 0 and tc[0] > 0:
            razoes.append(tp[0] / tc[0])
            n_vals.append(n)
    
    if n_vals:
        ax.plot(n_vals, razoes, marker=MARCADORES[tipo], linewidth=2.5,
               markersize=6, label=tipo, color=CORES[tipo], alpha=0.8)

ax.set_xlabel('Tamanho (n)', fontweight='bold', fontsize=12)
ax.set_ylabel('Razao: Python / C', fontweight='bold', fontsize=12)
ax.set_title('Velocidade Relativa: Quantas Vezes Python eh Mais Lento?',
            fontweight='bold', fontsize=13)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3)
ax.set_yscale('log')

plt.tight_layout()
plt.savefig('04_velocidade_relativa.png', dpi=300, bbox_inches='tight')
print("[OK] Grafico: 04_velocidade_relativa.png")
plt.close()

# ============================================================================
# RESUMO FINAL
# ============================================================================
print("\n" + "="*80)
print("RESUMO EXECUTIVO FINAL")
print("="*80)

# Encontrar maximos para casos maiores
n_maior = df_c['n'].max()
print(f"\nPara n = {n_maior} (maior tamanho testado):")
print("-"*80)

for tipo in ['melhor', 'medio', 'pior']:
    tc = df_c[(df_c['n'] == n_maior) & (df_c['tipo'] == tipo)]['tempo'].values
    tp = df_python[(df_python['n'] == n_maior) & (df_python['tipo'] == tipo)]['tempo'].values
    
    if len(tc) > 0 and len(tp) > 0:
        razao = tp[0] / tc[0]
        print(f"\n{tipo.upper()}:")
        print(f"  C:      {formatar_numero(tc[0])} s")
        print(f"  Python: {formatar_numero(tp[0])} s")
        print(f"  Razao:  {razao:.2f}x mais lento em Python")

print("\n" + "="*80)
print("ANALISE CONCLUIDA!")
print("="*80)
print("""
Graficos gerados:
  1. 01_visao_geral_completa.png
  2. 02_zoom_melhor_vs_medio.png
  3. 03_ajuste_curvas_teoricas.png
  4. 04_velocidade_relativa.png
""")
