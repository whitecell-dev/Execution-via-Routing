def reverse_array(arr):
    n = len(arr)
    result = []
    i = n - 1
    while i >= 0:
        result = result + [arr[i]]
        i = i - 1
    return result
