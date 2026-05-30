let trocas = 0
let comparacoes = 0

function swap(arr, i, j){
  const temp = arr[i]
  arr[i] = arr[j]
  arr[j] = temp
  trocas++
}

function partition(arr, start, end){
  const pivo = arr[start]
  let idx = end
  for (let i = end; i > start; i--) {
    comparacoes++
    if(arr[i] > pivo){
      swap(arr, i, idx--)
    }
  }

  swap(arr, start, idx)
  return idx
}

function qsort(arr, start, end){
  if (start < end){
    const idx = partition(arr, start, end)
    qsort(arr, start, idx - 1)
    qsort(arr, idx + 1, end)
  }
}

function crescente(arr, n) {
  for (let i = 0; i < n; i++) {
    arr[i] = i
  }
}

function decrescente(arr, n){
  for (let i = 0; i < n; i++) {
    arr[i] = n - i
  }
}

function aleatorio(arr, n){
  for (let i = 0; i < n; i++) {
    arr[i] = Math.floor(Math.random() * n)
  }
}

function teste(n, gerador){
  trocas = 0
  comparacoes = 0

  const arr = new Array(n)
  gerador(arr, n)

  const inicio = performance.now()
  qsort(arr, 0, n - 1)
  const fim = performance.now()
  console.log(n, fim - inicio, comparacoes, trocas)
}

function main(){
  const tamanhos = [1000, 5000, 10000]
  for (const tamanho of tamanhos) {
    teste(tamanho, crescente)
    teste(tamanho, decrescente)
    teste(tamanho, aleatorio)
  }
}

main()
