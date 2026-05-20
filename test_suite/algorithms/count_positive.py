def count_positive(arr):
    i = 0
    count = 0
    n = len(arr)

    while i < n:
        if arr[i] > 0:
            count = count + 1
        i = i + 1

    return count
