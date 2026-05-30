#define _POSIX_C_SOURCE 199309L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// --------------------------------------------------
// UTILIDADES
// --------------------------------------------------

void troca(int v[], int i, int j) {
    int aux = v[i];
    v[i] = v[j];
    v[j] = aux;
}

double tempo_decorrido(struct timespec inicio, struct timespec fim) {
    return (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
}

// --------------------------------------------------
// QUICKSORT - PIVÔ NO FIM (LOMUTO)
// --------------------------------------------------

int particao_fim(int v[], int inicio, int fim) {
    int pivot = v[fim];
    int indice = inicio;

    for (int i = inicio; i < fim; i++) {
        if (v[i] < pivot) {
            troca(v, i, indice);
            indice++;
        }
    }

    troca(v, indice, fim);
    return indice;
}

void quicksort_fim(int v[], int inicio, int fim) {
    if (inicio < fim) {
        int indice = particao_fim(v, inicio, fim);

        quicksort_fim(v, inicio, indice - 1);
        quicksort_fim(v, indice + 1, fim);
    }
}

// --------------------------------------------------
// QUICKSORT - PIVÔ MEDIANA
// --------------------------------------------------

int particao_mediana(int v[], int inicio, int fim) {
    int mediana = (inicio + fim) / 2;

    troca(v, mediana, fim);

    int pivot = v[fim];
    int indice = inicio;

    for (int i = inicio; i < fim; i++) {
        if (v[i] < pivot) {
            troca(v, i, indice);
            indice++;
        }
    }

    troca(v, indice, fim);
    return indice;
}

void quicksort_mediana(int v[], int inicio, int fim) {
    if (inicio < fim) {
        int indice = particao_mediana(v, inicio, fim);

        quicksort_mediana(v, inicio, indice - 1);
        quicksort_mediana(v, indice + 1, fim);
    }
}

// --------------------------------------------------
// GERADORES DE ENTRADA
// --------------------------------------------------

void vetor_ordenado(int* v, int n) {
    for (int i = 0; i < n; i++) {
        v[i] = i;
    }
}

void vetor_aleatorio(int* v, int n) {
    for (int i = 0; i < n; i++) {
        v[i] = rand();
    }
}

// --------------------------------------------------
// TESTE
// --------------------------------------------------

double testar_quicksort(void (*quicksort)(int*, int, int),
                        void (*gerador)(int*, int), int n) {
    int* v = malloc(n * sizeof(int));

    if (!v) {
        printf("Erro de alocacao\n");
        exit(1);
    }

    gerador(v, n);

    struct timespec inicio, fim;

    clock_gettime(CLOCK_MONOTONIC, &inicio);

    quicksort(v, 0, n - 1);

    clock_gettime(CLOCK_MONOTONIC, &fim);

    free(v);

    return tempo_decorrido(inicio, fim);
}

// --------------------------------------------------
// MAIN
// --------------------------------------------------

int main() {
    srand((unsigned int)time(NULL));

    FILE* arquivo = fopen("log_c.txt", "w");

    if (arquivo == NULL) {
        printf("Erro ao abrir arquivo.\n");
        return 1;
    }

    for (int n = 10; n <= 1000; n += 10) {
        double pior_caso_tempo = 0.0;
        double melhor_caso_tempo = 0.0;
        double caso_medio_tempo = 0.0;

        for (int t = 0; t < 30; t++) {
            pior_caso_tempo +=
                testar_quicksort(quicksort_fim, vetor_ordenado, n);

            melhor_caso_tempo +=
                testar_quicksort(quicksort_mediana, vetor_ordenado, n);

            caso_medio_tempo +=
                testar_quicksort(quicksort_fim, vetor_aleatorio, n);
        }

        fprintf(arquivo, "%d,%.9f,pior\n", n, pior_caso_tempo / 30.0);

        fprintf(arquivo, "%d,%.9f,melhor\n", n, melhor_caso_tempo / 30.0);

        fprintf(arquivo, "%d,%.9f,medio\n", n, caso_medio_tempo / 30.0);

        printf("n = %d concluido\n", n);
    }

    fclose(arquivo);

    return 0;
}