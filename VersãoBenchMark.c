#ifndef _WIN32
#define _POSIX_C_SOURCE 199309L
#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#ifdef _WIN32
#include <windows.h>
#else
#include <time.h>
#endif

#define RODADAS 30

long long comparacoes = 0;
long long trocas = 0;

typedef void (*Gerador)(int *, int, int);

// ---------- TEMPO DE ALTA PRECISÃO ----------
double tempo_atual_ms(void) {
#ifdef _WIN32
    static LARGE_INTEGER frequencia;
    static int inicializado = 0;
    LARGE_INTEGER contador;

    if (!inicializado) {
        QueryPerformanceFrequency(&frequencia);
        inicializado = 1;
    }

    QueryPerformanceCounter(&contador);
    return (double)contador.QuadPart * 1000.0 / (double)frequencia.QuadPart;
#else
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec * 1000.0 + (double)ts.tv_nsec / 1000000.0;
#endif
}

// ---------- FUNÇÃO TROCA ----------
void troca(int v[], int i, int j) {
    int aux = v[i];
    v[i] = v[j];
    v[j] = aux;
    trocas++;
}

// ---------- PARTICIONAMENTO ----------
int particao(int v[], int inicio, int fim) {
    int pivot = inicio;
    int indice = fim;

    for (int i = fim; i > inicio; i--) {
        comparacoes++;

        if (v[i] >= v[pivot]) {
            troca(v, i, indice);
            indice--;
        }
    }

    troca(v, pivot, indice);
    return indice;
}

// ---------- QUICKSORT ----------
void quicksort(int v[], int inicio, int fim) {
    if (inicio < fim) {
        int indice = particao(v, inicio, fim);
        quicksort(v, inicio, indice - 1);
        quicksort(v, indice + 1, fim);
    }
}

// ---------- VERIFICA SE ORDENOU CORRETAMENTE ----------
int esta_ordenado(int v[], int n) {
    for (int i = 1; i < n; i++) {
        if (v[i - 1] > v[i]) {
            return 0;
        }
    }
    return 1;
}

// ---------- GERADOR PSEUDOALEATÓRIO REPRODUTÍVEL ----------
uint32_t xorshift32(uint32_t *estado) {
    uint32_t x = *estado;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    *estado = x;
    return x;
}

// ---------- CASO MÉDIO: VETOR ALEATÓRIO ----------
void preencher_caso_medio(int *v, int n, int rodada) {
    uint32_t estado = 2463534242u + (uint32_t)rodada * 747796405u;

    for (int i = 0; i < n; i++) {
        v[i] = (int)(xorshift32(&estado) & 0x7fffffff);
    }
}

// ---------- MELHOR CASO ----------
// Para este Quick Sort, o melhor caso ocorre quando o pivô divide
// o vetor aproximadamente ao meio em todas as chamadas recursivas.
void gerar_melhor_rec(int *saida, int pos, int valor_inicio, int quantidade) {
    if (quantidade <= 0) {
        return;
    }

    if (quantidade == 1) {
        saida[pos] = valor_inicio;
        return;
    }

    int tam_esq = quantidade / 2;
    int pivot = valor_inicio + tam_esq;
    int tam_dir = quantidade - tam_esq - 1;

    saida[pos] = pivot;

    if (tam_esq > 0) {
        int *perm_esq = (int *)malloc((size_t)tam_esq * sizeof(int));

        if (!perm_esq) {
            printf("Erro ao alocar memoria no gerador de melhor caso.\n");
            exit(EXIT_FAILURE);
        }

        gerar_melhor_rec(perm_esq, 0, valor_inicio, tam_esq);

        for (int i = 1; i < tam_esq; i++) {
            saida[pos + i] = perm_esq[i];
        }

        saida[pos + tam_esq] = perm_esq[0];

        free(perm_esq);
    }

    gerar_melhor_rec(saida, pos + 1 + tam_esq, pivot + 1, tam_dir);
}

void preencher_melhor_caso(int *v, int n, int rodada) {
    (void)rodada;
    gerar_melhor_rec(v, 0, 0, n);
}

// ---------- PIOR CASO ----------
// Como o pivô é sempre o primeiro elemento, vetor já ordenado causa
// partições extremamente desbalanceadas.
void preencher_pior_caso(int *v, int n, int rodada) {
    (void)rodada;

    for (int i = 0; i < n; i++) {
        v[i] = i;
    }
}

// ---------- MÉDIA ----------
double media(double valores[], int qtd) {
    double soma = 0.0;

    for (int i = 0; i < qtd; i++) {
        soma += valores[i];
    }

    return soma / qtd;
}

// ---------- DESVIO-PADRÃO AMOSTRAL ----------
double desvio_padrao(double valores[], int qtd) {
    if (qtd < 2) {
        return 0.0;
    }

    double m = media(valores, qtd);
    double soma = 0.0;

    for (int i = 0; i < qtd; i++) {
        double diferenca = valores[i] - m;
        soma += diferenca * diferenca;
    }

    return sqrt(soma / (qtd - 1));
}

// ---------- TESTE DE UM CENÁRIO ----------
void testar_cenario(FILE *csv, const char *nome_cenario, Gerador preencher, int n) {
    double tempos[RODADAS];
    double comparacoes_por_rodada[RODADAS];
    double trocas_por_rodada[RODADAS];

    for (int rodada = 0; rodada < RODADAS; rodada++) {
        int *v = (int *)malloc((size_t)n * sizeof(int));

        if (!v) {
            printf("Erro ao alocar memoria para n = %d\n", n);
            return;
        }

        preencher(v, n, rodada);

        comparacoes = 0;
        trocas = 0;

        double inicio = tempo_atual_ms();

        quicksort(v, 0, n - 1);

        double fim = tempo_atual_ms();

        if (!esta_ordenado(v, n)) {
            printf(
                "ERRO: vetor nao foi ordenado corretamente no cenario %s, n = %d, rodada = %d\n",
                nome_cenario,
                n,
                rodada + 1
            );
        }

        tempos[rodada] = fim - inicio;
        comparacoes_por_rodada[rodada] = (double)comparacoes;
        trocas_por_rodada[rodada] = (double)trocas;

        free(v);
    }

    double media_tempo = media(tempos, RODADAS);
    double desvio_tempo = desvio_padrao(tempos, RODADAS);

    double media_comparacoes = media(comparacoes_por_rodada, RODADAS);
    double desvio_comparacoes = desvio_padrao(comparacoes_por_rodada, RODADAS);

    double media_trocas = media(trocas_por_rodada, RODADAS);
    double desvio_trocas = desvio_padrao(trocas_por_rodada, RODADAS);

    printf(
        "%-10d | %-12s | %7d | %14.6f | %14.6f | %18.2f | %18.2f | %14.2f | %14.2f\n",
        n,
        nome_cenario,
        RODADAS,
        media_tempo,
        desvio_tempo,
        media_comparacoes,
        desvio_comparacoes,
        media_trocas,
        desvio_trocas
    );

    if (csv) {
        fprintf(
            csv,
            "%d,%s,%d,%.6f,%.6f,%.2f,%.2f,%.2f,%.2f\n",
            n,
            nome_cenario,
            RODADAS,
            media_tempo,
            desvio_tempo,
            media_comparacoes,
            desvio_comparacoes,
            media_trocas,
            desvio_trocas
        );
    }
}

// ---------- MAIN ----------
int main(void) {
    int tamanhos[] = {1000, 5000, 10000};
    int qtd_tamanhos = (int)(sizeof(tamanhos) / sizeof(tamanhos[0]));

    FILE *csv = fopen("resultados_quicksort_c.csv", "w");

    if (!csv) {
        printf("Aviso: nao foi possivel criar o arquivo CSV. Os resultados serao exibidos apenas no terminal.\n");
    } else {
        fprintf(
            csv,
            "tamanho,cenario,rodadas,tempo_medio_ms,tempo_desvio_ms,comparacoes_media,comparacoes_desvio,trocas_media,trocas_desvio\n"
        );
    }

    printf("=== Experimento: Quick Sort em C ===\n");
    printf("Pivo usado: primeiro elemento da particao.\n");
    printf("Rodadas por tamanho e cenario: %d\n\n", RODADAS);

    printf(
        "%-10s | %-12s | %-7s | %-14s | %-14s | %-18s | %-18s | %-14s | %-14s\n",
        "Tamanho",
        "Cenario",
        "Rodadas",
        "Tempo medio",
        "Desvio-padrao tempo",
        "Comparacoes media",
        "Desvio comparacoes",
        "Trocas media",
        "Desvio-padrao trocas"
    );

    printf("-----------------------------------------------------------------------------------------------------------------------------------------------------\n");

    for (int i = 0; i < qtd_tamanhos; i++) {
        int n = tamanhos[i];

        testar_cenario(csv, "Melhor", preencher_melhor_caso, n);
        testar_cenario(csv, "Medio", preencher_caso_medio, n);
        testar_cenario(csv, "Pior", preencher_pior_caso, n);

        printf("-----------------------------------------------------------------------------------------------------------------------------------------------------\n");
    }

    if (csv) {
        fclose(csv);
        printf("\nArquivo CSV gerado: resultados_quicksort_c.csv\n");
    }

    return 0;
}