def is_palindrome(arr):
    left = 0
    right = len(arr) - 1
    while left < right:
        if arr[left] != arr[right]:
            return 0
        left = left + 1
        right = right - 1
    return 1
