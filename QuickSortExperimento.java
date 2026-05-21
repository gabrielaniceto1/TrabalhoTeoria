import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;

public class QuickSortExperimento {

    static final int RODADAS = 30;

    static long comparacoes = 0;
    static long trocas = 0;

    // ---------- INTERFACE PARA OS GERADORES ----------
    interface Gerador {
        void preencher(int[] v, int n, int rodada);
    }

    // ---------- FUNÇÃO TROCA ----------
    public static void troca(int[] v, int i, int j) {
        int aux = v[i];
        v[i] = v[j];
        v[j] = aux;
        trocas++;
    }

    // ---------- PARTICIONAMENTO ----------
    public static int particao(int[] v, int inicio, int fim) {
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
    public static void quicksort(int[] v, int inicio, int fim) {
        if (inicio < fim) {
            int indice = particao(v, inicio, fim);
            quicksort(v, inicio, indice - 1);
            quicksort(v, indice + 1, fim);
        }
    }

    // ---------- VERIFICA SE ORDENOU ----------
    public static boolean estaOrdenado(int[] v) {
        for (int i = 1; i < v.length; i++) {
            if (v[i - 1] > v[i]) {
                return false;
            }
        }

        return true;
    }

    // ---------- GERADOR PSEUDOALEATÓRIO REPRODUTÍVEL ----------
    public static int xorshift32(int[] estado) {
        int x = estado[0];

        x ^= x << 13;
        x ^= x >>> 17;
        x ^= x << 5;

        estado[0] = x;
        return x;
    }

    // ---------- CASO MÉDIO: VETOR ALEATÓRIO ----------
    public static void preencherCasoMedio(int[] v, int n, int rodada) {
        int[] estado = {246353424 + rodada * 747796405};

        for (int i = 0; i < n; i++) {
            v[i] = xorshift32(estado) & 0x7fffffff;
        }
    }

    // ---------- MELHOR CASO ----------
    /*
     * Como o pivô usado é sempre o primeiro elemento,
     * o melhor caso acontece quando esse primeiro elemento
     * divide a partição em duas partes aproximadamente iguais.
     */
    public static void gerarMelhorRec(int[] saida, int pos, int valorInicio, int quantidade) {
        if (quantidade <= 0) {
            return;
        }

        if (quantidade == 1) {
            saida[pos] = valorInicio;
            return;
        }

        int tamEsq = quantidade / 2;
        int pivot = valorInicio + tamEsq;
        int tamDir = quantidade - tamEsq - 1;

        saida[pos] = pivot;

        if (tamEsq > 0) {
            int[] permEsq = new int[tamEsq];

            gerarMelhorRec(permEsq, 0, valorInicio, tamEsq);

            for (int i = 1; i < tamEsq; i++) {
                saida[pos + i] = permEsq[i];
            }

            saida[pos + tamEsq] = permEsq[0];
        }

        gerarMelhorRec(saida, pos + 1 + tamEsq, pivot + 1, tamDir);
    }

    public static void preencherMelhorCaso(int[] v, int n, int rodada) {
        gerarMelhorRec(v, 0, 0, n);
    }

    // ---------- PIOR CASO ----------
    /*
     * Como o pivô é o primeiro elemento, um vetor já ordenado
     * gera partições muito desbalanceadas.
     */
    public static void preencherPiorCaso(int[] v, int n, int rodada) {
        for (int i = 0; i < n; i++) {
            v[i] = i;
        }
    }

    // ---------- MÉDIA ----------
    public static double media(double[] valores) {
        double soma = 0.0;

        for (double valor : valores) {
            soma += valor;
        }

        return soma / valores.length;
    }

    // ---------- DESVIO-PADRÃO AMOSTRAL ----------
    public static double desvioPadrao(double[] valores) {
        if (valores.length < 2) {
            return 0.0;
        }

        double m = media(valores);
        double soma = 0.0;

        for (double valor : valores) {
            double diferenca = valor - m;
            soma += diferenca * diferenca;
        }

        return Math.sqrt(soma / (valores.length - 1));
    }

    // ---------- TESTE DE UM CENÁRIO ----------
    public static void testarCenario(
            PrintWriter csv,
            String nomeCenario,
            Gerador gerador,
            int n
    ) {
        double[] tempos = new double[RODADAS];
        double[] comparacoesPorRodada = new double[RODADAS];
        double[] trocasPorRodada = new double[RODADAS];

        for (int rodada = 0; rodada < RODADAS; rodada++) {
            int[] v = new int[n];

            gerador.preencher(v, n, rodada);

            comparacoes = 0;
            trocas = 0;

            long inicio = System.nanoTime();

            quicksort(v, 0, n - 1);

            long fim = System.nanoTime();

            double tempoMs = (fim - inicio) / 1_000_000.0;

            if (!estaOrdenado(v)) {
                System.out.printf(
                        "ERRO: vetor nao foi ordenado corretamente. Cenario: %s | n = %d | Rodada = %d%n",
                        nomeCenario,
                        n,
                        rodada + 1
                );
            }

            tempos[rodada] = tempoMs;
            comparacoesPorRodada[rodada] = comparacoes;
            trocasPorRodada[rodada] = trocas;
        }

        double mediaTempo = media(tempos);
        double desvioTempo = desvioPadrao(tempos);

        double mediaComparacoes = media(comparacoesPorRodada);
        double desvioComparacoes = desvioPadrao(comparacoesPorRodada);

        double mediaTrocas = media(trocasPorRodada);
        double desvioTrocas = desvioPadrao(trocasPorRodada);

        System.out.printf(
                "%-10d | %-12s | %-7d | %14.6f | %14.6f | %18.2f | %18.2f | %14.2f | %14.2f%n",
                n,
                nomeCenario,
                RODADAS,
                mediaTempo,
                desvioTempo,
                mediaComparacoes,
                desvioComparacoes,
                mediaTrocas,
                desvioTrocas
        );

        if (csv != null) {
            csv.printf(
                    "%d,%s,%d,%.6f,%.6f,%.2f,%.2f,%.2f,%.2f%n",
                    n,
                    nomeCenario,
                    RODADAS,
                    mediaTempo,
                    desvioTempo,
                    mediaComparacoes,
                    desvioComparacoes,
                    mediaTrocas,
                    desvioTrocas
            );
        }
    }

    // ---------- MAIN ----------
    public static void main(String[] args) {
        int[] tamanhos = {1000, 5000, 10000};

        try (PrintWriter csv = new PrintWriter(new FileWriter("resultados_quicksort_java.csv"))) {

            csv.println(
                    "tamanho,cenario,rodadas,tempo_medio_ms,tempo_desvio_ms,comparacoes_media,comparacoes_desvio,trocas_media,trocas_desvio"
            );

            System.out.println("=== Experimento: Quick Sort em Java ===");
            System.out.println("Pivo usado: primeiro elemento da particao.");
            System.out.println("Rodadas por tamanho e cenario: " + RODADAS);
            System.out.println();

            System.out.printf(
                    "%-10s | %-12s | %-7s | %-14s | %-14s | %-18s | %-18s | %-14s | %-14s%n",
                    "Tamanho",
                    "Cenario",
                    "Rodadas",
                    "Tempo medio",
                    "Desvio tempo",
                    "Comp. media",
                    "Desvio comp.",
                    "Trocas media",
                    "Desvio trocas"
            );

            System.out.println(
                    "-----------------------------------------------------------------------------------------------------------------------------------------------------"
            );

            for (int n : tamanhos) {
                testarCenario(csv, "Melhor", QuickSortExperimento::preencherMelhorCaso, n);
                testarCenario(csv, "Medio", QuickSortExperimento::preencherCasoMedio, n);
                testarCenario(csv, "Pior", QuickSortExperimento::preencherPiorCaso, n);

                System.out.println(
                        "-----------------------------------------------------------------------------------------------------------------------------------------------------"
                );
            }

            System.out.println();
            System.out.println("Arquivo CSV gerado: resultados_quicksort_java.csv");

        } catch (IOException e) {
            System.out.println("Erro ao criar arquivo CSV: " + e.getMessage());
        }
    }
}