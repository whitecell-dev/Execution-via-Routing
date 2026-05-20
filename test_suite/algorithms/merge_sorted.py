def merge_sorted(left, right):
    result = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result = result + [left[i]]
            i = i + 1
        else:
            result = result + [right[j]]
            j = j + 1
    while i < len(left):
        result = result + [left[i]]
        i = i + 1
    while j < len(right):
        result = result + [right[j]]
        j = j + 1
    return result
