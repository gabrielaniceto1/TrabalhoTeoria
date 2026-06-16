import time
import random
import sys
sys.setrecursionlimit(50000)

# --------------------------------------------------
# UTILIDADES
# --------------------------------------------------


def troca(v, i, j):
    v[i], v[j] = v[j], v[i]


def tempo_decorrido(inicio, fim):
    return fim - inicio


# --------------------------------------------------
# QUICKSORT - PIVÔ NO FIM (LOMUTO)
# --------------------------------------------------


def particao_fim(v, inicio, fim):
    pivot = v[fim]
    indice = inicio

    for i in range(inicio, fim):
        if v[i] < pivot:
            troca(v, i, indice)
            indice += 1

    troca(v, indice, fim)
    return indice


def quicksort_fim(v, inicio, fim):
    if inicio < fim:
        indice = particao_fim(v, inicio, fim)

        quicksort_fim(v, inicio, indice - 1)
        quicksort_fim(v, indice + 1, fim)


# --------------------------------------------------
# QUICKSORT - PIVÔ MEDIANA
# --------------------------------------------------


def particao_mediana(v, inicio, fim):
    mediana = (inicio + fim) // 2

    troca(v, mediana, fim)

    pivot = v[fim]
    indice = inicio

    for i in range(inicio, fim):
        if v[i] < pivot:
            troca(v, i, indice)
            indice += 1

    troca(v, indice, fim)
    return indice


def quicksort_mediana(v, inicio, fim):
    if inicio < fim:
        indice = particao_mediana(v, inicio, fim)

        quicksort_mediana(v, inicio, indice - 1)
        quicksort_mediana(v, indice + 1, fim)


# --------------------------------------------------
# GERADORES DE ENTRADA
# --------------------------------------------------


def vetor_ordenado(n):
    return list(range(n))


def vetor_aleatorio(n):
    return [random.randint(0, 2**31 - 1) for _ in range(n)]


# --------------------------------------------------
# TESTE
# --------------------------------------------------


def testar_quicksort(quicksort, gerador, n):
    v = gerador(n)

    inicio = time.perf_counter()

    quicksort(v, 0, n - 1)

    fim = time.perf_counter()

    return tempo_decorrido(inicio, fim)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    random.seed(int(time.time()))

    with open("log_python.txt", "w") as arquivo:

        n = 10
        while n <= 1000:

            pior_caso_tempo = 0.0
            melhor_caso_tempo = 0.0
            caso_medio_tempo = 0.0

            for t in range(30):

                pior_caso_tempo += testar_quicksort(quicksort_fim, vetor_ordenado, n)

                melhor_caso_tempo += testar_quicksort(quicksort_mediana, vetor_ordenado, n)

                caso_medio_tempo += testar_quicksort(quicksort_fim, vetor_aleatorio, n)

            arquivo.write(f"{n},{pior_caso_tempo / 30.0:.9f},pior\n")

            arquivo.write(f"{n},{melhor_caso_tempo / 30.0:.9f},melhor\n")

            arquivo.write(f"{n},{caso_medio_tempo / 30.0:.9f},medio\n")

            print(f"n = {n} concluido")

            n += 10
