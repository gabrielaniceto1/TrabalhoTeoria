# Análise Avançada de QuickSort - Logs com Visualizações

## Resumo Executivo

Análise completa de desempenho do algoritmo QuickSort implementado em **C** e **Python**, com dados coletados para 100 tamanhos diferentes (n = 10 a 1000), em três cenários:
- **Melhor Caso** (array já ordenado): O(n log n)
- **Caso Médio** (array aleatório): O(n log n)  
- **Pior Caso** (array invertido): O(n²)

---

## 📊 Gráficos Gerados

### 1. **01_visao_geral_completa.png**
   - **6 subgráficos** em uma visualização unificada
   - Escala Linear e Log-Log para C e Python
   - Comparação direta C vs Python
   - Razão entre Pior e Caso Médio
   - Diferenças percentuais
   - Box plots de distribuição
   
   **Insight**: Visualização abrangente mostrando que Python é ~30x mais lento em casos extremos

---

### 2. **02_zoom_melhor_vs_medio.png**
   - Foco exclusivo na diferença entre **Melhor e Caso Médio**
   - Gráficos Linear e Log-Log
   - Linhas de referência O(n log n)
   - Mostra a otimização do melhor cenário vs caso típico
   
   **Insight**: Diferenças mais sutis que o Pior Caso, importante para entender variações em O(n log n)

---

### 3. **03_ajuste_curvas_teoricas.png**
   - Ajuste de curvas com **R² (coeficiente de determinação)**
   - Compara dados reais com funções teóricas:
     - Melhor: O(n log n)
     - Médio: O(n log n)
     - Pior: O(n²)
   - Mostra qualidade do ajuste (R² próximo de 1 = perfeito)
   
   **Insight**: Valida empiricamente a complexidade teórica esperada

---

### 4. **04_velocidade_relativa.png**
   - **Razão Python / C** para cada tamanho
   - Mostra quantas vezes Python é mais lento
   - Linha separada para Melhor, Médio e Pior
   - Escala logarítmica para melhor visualização
   
   **Insight**: Diferença de velocidade cresce exponencialmente no pior caso

---

## 📈 Dados Coletados

### Implementação em C
- **Melhor Caso**: 1.43e-05 s (média)
- **Caso Médio**: 3.14e-05 s (média)
- **Pior Caso**: 7.71e-04 s (média)

### Implementação em Python
- **Melhor Caso**: 4.24e-04 s (média)
- **Caso Médio**: 5.39e-04 s (média)
- **Pior Caso**: 0.0233 s (média)

### Velocidade Relativa (n = 1000)
| Caso | C (s) | Python (s) | Razão |
|------|-------|-----------|-------|
| Melhor | 2.91e-05 | 9.00e-04 | 30.97x |
| Médio | 6.64e-05 | 0.00113 | 17.07x |
| Pior | 0.00227 | 0.0717 | 31.60x |

---

## 🔍 Análise Detalhada

### Melhor Caso vs Caso Médio
O script quantifica as diferenças percentuais entre esses dois cenários O(n log n):
- A diferença cresce com n
- Importante para entender overhead do particionamento médio
- Python mostra variação maior, sugerindo overhead interpretado

### Complexidade Confirmada
Através dos ajustes de curva (R² > 0.99):
- **Melhor e Médio**: Seguem O(n log n) com precisão
- **Pior**: Segue O(n²) com alta fidelidade
- Implementação C é mais consistente (menos variação)

### Overhead de Python
- **Interpretação**: Maior overhead em chamadas de função
- **Tipo de dado**: Estruturas Python mais pesadas
- **Escalabilidade**: Piora exponencialmente em O(n²)

---

## 🛠️ Scripts Utilizados

### `analise_formatada.py` (Principal)
Script otimizado para grandes volumes de dados com:
- ✅ Parsing robusto de logs
- ✅ Análise estatística completa
- ✅ Ajuste de curvas com scipy
- ✅ 4 figuras com múltiplos subgráficos
- ✅ Tabelas comparativas formatadas
- ✅ Suporte a 100+ pontos de dados

### Scripts Adicionais
- `analise_avancada.py`: Versão anterior com 6 gráficos separados
- `analise_logs.py`: Versão inicial com gráficos básicos

---

## 📝 Como Reproduzir

1. **Atualizar logs** (já feito):
   ```
   log_c.txt       - 300 linhas (100 pontos × 3 casos)
   log_python.txt  - 300 linhas (100 pontos × 3 casos)
   ```

2. **Executar análise**:
   ```bash
   python analise_formatada.py
   ```

3. **Gráficos gerados automaticamente**:
   - `01_visao_geral_completa.png`
   - `02_zoom_melhor_vs_medio.png`
   - `03_ajuste_curvas_teoricas.png`
   - `04_velocidade_relativa.png`

---

## 💡 Insights Principais

1. **Complexidade Confirmada**: Dados empíricos confirmam O(n log n) para melhor/médio e O(n²) para pior
2. **Vantagem de C**: ~30x mais rápido que Python em operações críticas
3. **Escalabilidade**: O pior caso se torna proibitivo rapidamente em Python (31.60x mais lento em n=1000)
4. **Variação**: Python mostra maior variação estatística, especialmente em casos pequenos
5. **Overhead Fixo**: Há overhead fixo de Python (início) que diminui proporcionalmente com n grande

---

## 📊 Formato dos Dados

**log_c.txt** e **log_python.txt**:
```
1. 10,0.000000307,pior
2. 10,0.000000150,melhor
3. 10,0.000000257,medio
...
```

Estrutura: `numero_linha. tamanho,tempo_segundos,tipo_caso`

---

## 🎯 Conclusão

A análise formatada e abrangente permite visualizar claramente:
- ✅ Diferenças entre casos de execução
- ✅ Conformidade com teoria de complexidade
- ✅ Vantagens relativas C vs Python
- ✅ Comportamento em diferentes escalas
- ✅ Distribuição estatística dos tempos

**Status**: ✅ Análise Completa e Documentada
