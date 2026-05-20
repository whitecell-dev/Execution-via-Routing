def bubble_sort(arr):
    n = len(arr)
    result = arr

    i = 0
    while i < n:
        j = 0
        while j < n - i - 1:
            if result[j] > result[j + 1]:
                # Functional swap: create new list
                left = result[:j]
                middle = [result[j + 1], result[j]]
                right = result[j + 2 :]
                result = left + middle + right
            j = j + 1
        i = i + 1

    return result
