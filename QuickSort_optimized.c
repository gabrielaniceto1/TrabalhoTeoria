#define _POSIX_C_SOURCE 199309L

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Limiar abaixo do qual subarrays são deixados para o insertion sort final.
// Valores entre 8 e 32 costumam ser ótimos em hardware moderno.
#define INSERTION_THRESHOLD 16

// log2(1000) < 10, e a eliminação da chamada recursiva mantém a pilha
// O(log n); 64 slots (32 níveis) sobra com folga.
#define STACK_SIZE 64

// --------------------------------------------------
// UTILIDADES
// --------------------------------------------------

static inline void troca(int v[], int i, int j) {
    int aux = v[i];
    v[i] = v[j];
    v[j] = aux;
}

static double tempo_decorrido(struct timespec inicio, struct timespec fim) {
    return (fim.tv_sec - inicio.tv_sec) + (fim.tv_nsec - inicio.tv_nsec) / 1e9;
}

// --------------------------------------------------
// INSERTION SORT (subarrays pequenos / passada final)
// --------------------------------------------------

static inline void insertion_sort(int v[], int inicio, int fim) {
    for (int i = inicio + 1; i <= fim; i++) {
        int chave = v[i];
        int j = i - 1;
        while (j >= inicio && v[j] > chave) {
            v[j + 1] = v[j];
            j--;
        }
        v[j + 1] = chave;
    }
}

// --------------------------------------------------
// QUICKSORT - MEDIANA-DE-TRÊS ITERATIVO
// --------------------------------------------------

static inline int particao_mediana(int v[], int inicio, int fim) {
    int meio = inicio + ((fim - inicio) >> 1);

    // Mediana de três real: ordena (inicio, meio, fim) e usa o do meio
    // como pivô. Reduz drasticamente o pior caso em entradas ordenadas.
    if (v[inicio] > v[meio]) troca(v, inicio, meio);
    if (v[inicio] > v[fim])  troca(v, inicio, fim);
    if (v[meio]  > v[fim])   troca(v, meio,  fim);

    troca(v, meio, fim);

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
    int original_inicio = inicio;
    int original_fim = fim;
    int stack[STACK_SIZE];
    int top = -1;

    while (1) {
        // Particiona até o subarray ficar pequeno; ranges menores que o
        // limiar são deixados para a passada final de insertion sort.
        while (fim - inicio >= INSERTION_THRESHOLD) {
            int indice = particao_mediana(v, inicio, fim);

            // Tail-call elimination: empilha a maior partição e itera
            // diretamente na menor. Garante profundidade O(log n).
            if ((indice - 1 - inicio) > (fim - indice - 1)) {
                stack[++top] = inicio;
                stack[++top] = indice - 1;
                inicio = indice + 1;
            } else {
                stack[++top] = indice + 1;
                stack[++top] = fim;
                fim = indice - 1;
            }
        }

        if (top < 0) break;
        fim = stack[top--];
        inicio = stack[top--];
    }

    insertion_sort(v, original_inicio, original_fim);
}

// --------------------------------------------------
// GERADORES DE ENTRADA
// --------------------------------------------------

// Melhor caso: vetor já ordenado.
// A mediana de três escolhe exatamente o elemento central como pivô,
// produzindo partições balanceadas perfeitas → O(n log n) ideal.
static void vetor_ordenado(int* v, int n) {
    for (int i = 0; i < n; i++) {
        v[i] = i;
    }
}

// Caso médio: vetor aleatório.
static void vetor_aleatorio(int* v, int n) {
    for (int i = 0; i < n; i++) {
        v[i] = rand();
    }
}

// Pior caso: vetor com elementos iguais.
// O particionamento de Lomuto degenera com duplicatas (todos os elementos
// vão para o mesmo lado), produzindo O(n²) mesmo com mediana de três.
static void vetor_constante(int* v, int n) {
    for (int i = 0; i < n; i++) {
        v[i] = 42;
    }
}

// --------------------------------------------------
// TESTE
// --------------------------------------------------

static double testar_quicksort(void (*quicksort)(int*, int, int),
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

    FILE* arquivo = fopen("log_c_optimized.txt", "w");

    if (arquivo == NULL) {
        printf("Erro ao abrir arquivo.\n");
        return 1;
    }

    for (int n = 10; n <= 5000; n += 10) {
        double pior_caso_tempo = 0.0;
        double melhor_caso_tempo = 0.0;
        double caso_medio_tempo = 0.0;

        for (int t = 0; t < 30; t++) {
            pior_caso_tempo +=
                testar_quicksort(quicksort_mediana, vetor_constante, n);

            melhor_caso_tempo +=
                testar_quicksort(quicksort_mediana, vetor_ordenado, n);

            caso_medio_tempo +=
                testar_quicksort(quicksort_mediana, vetor_aleatorio, n);
        }

        fprintf(arquivo, "%d,%.9f,pior\n", n, pior_caso_tempo / 30.0);

        fprintf(arquivo, "%d,%.9f,melhor\n", n, melhor_caso_tempo / 30.0);

        fprintf(arquivo, "%d,%.9f,medio\n", n, caso_medio_tempo / 30.0);

        printf("n = %d concluido\n", n);
    }

    fclose(arquivo);

    return 0;
}
