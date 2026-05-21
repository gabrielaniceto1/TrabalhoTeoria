const quicksort = (array:number[]):any => {

    if (array.length < 2){
        return array
    }

    let pivot:number = array[array.length - 1];
    let right:number[] = [];
    let left:number[] = [];

    for (let i = 0 ; i < array.length - 1 ; i ++){
        if (array[i] > pivot){
            right.push(array[i]);
        }

        else{
            left.push(array[i]);
        }
    }

    return [...quicksort(left) , pivot , ...quicksort(right)];
}
