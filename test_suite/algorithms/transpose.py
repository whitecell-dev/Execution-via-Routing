def transpose(matrix):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    result = []
    j = 0
    while j < cols:
        row = []
        i = 0
        while i < rows:
            row = row + [matrix[i][j]]
            i = i + 1
        result = result + [row]
        j = j + 1
    return result
