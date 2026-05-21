#include <stdlib.h>
#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int particao(int *v, int inicio, int fim) {
    int pivo = v[fim];
    int i = inicio - 1;

    for (int j = inicio; j < fim; j++) {
        if (v[j] <= pivo) {
            i++;
            swap(&v[i], &v[j]);
        }
    }

    swap(&v[i + 1], &v[fim]);

    return i + 1;
}

void quicksort(int *v, int inicio, int fim) {
    if (inicio < fim) {
        int indice = particao(v, inicio, fim);

        quicksort(v, inicio, indice - 1);
        quicksort(v, indice + 1, fim);
    }
}