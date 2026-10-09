# TODO здесь писать код
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    end_sym = arr[-1]
    smallest = [item for item in arr[:-1] if item < end_sym]
    reference = [item for item in arr if item == end_sym]
    biggest = [item for item in arr[:-1] if item > end_sym]
    return quicksort(smallest) + reference + quicksort(biggest)

problem = [5, 8, 9, 4, 2, 9, 1, 8]
sorted_problem = quicksort(problem)
print(sorted_problem)
