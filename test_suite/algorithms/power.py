def power(base, exp):
    if exp == 0:
        return 1
    result = 1
    i = 0
    while i < exp:
        result = result * base
        i = i + 1
    return result
