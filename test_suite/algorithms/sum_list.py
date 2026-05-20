def sum_list(arr):
    total = 0
    i = 0
    n = len(arr)
    while i < n:
        total = total + arr[i]
        i = i + 1
    return total
