
# /**
# 3. Write a function that takes an array of integers as input and returns the maximum difference between any two numbers in the array.
# Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.
# */

# Unoptimized max difference (brute-force)
def max_difference_unoptimized(arr):
    if len(arr) < 2:
        return 0

    max_diff = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            max_diff = max(max_diff, arr[j] - arr[i])

    return max_diff

# Time Complexity:
# This has a time complexity of O(n^2) because it uses two nested loops to compare each pair of elements.
# This becomes inefficient for large arrays.

# Optimized max difference
def max_difference_optimized(arr):
    if len(arr) < 2:
        return 0

    min_val = arr[0]
    max_diff = 0

    for num in arr[1:]:
        max_diff = max(max_diff, num - min_val)
        min_val = min(min_val, num)

    return max_diff

# Time Complexity:
# This has a time complexity of O(n), as it only requires a single pass through the array.
# This is significantly faster than the O(n^2) brute-force approach.
