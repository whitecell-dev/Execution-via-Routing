def fibonacci(n):
    if n <= 1:
        return n
    a = 0
    b = 1
    i = 2
    while i <= n:
        a, b = b, a + b
        i = i + 1
    return b
