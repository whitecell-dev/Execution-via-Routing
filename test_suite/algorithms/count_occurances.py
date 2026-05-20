def count_occurrences(arr, target):
    count = 0
    i = 0
    while i < len(arr):
        if arr[i] == target:
            count = count + 1
        i = i + 1
    return count
