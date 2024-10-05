# /**
# 2. Given an array of integers, write a function that finds the second largest number in the array.
# Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.
# */

# Unoptimized second largest (using sorting)
def second_largest_unoptimized(arr):
    if len(arr) < 2:
        return None
    sorted_arr = sorted(arr)  # Sorting the array takes O(n log n)
    return sorted_arr[-2]     # Accessing the second last element is O(1)

# Time Complexity:
# This solution has a time complexity of O(n log n) due to the sorting step.
# Sorting the array dominates the complexity, making it slower for large arrays.


# Optimized second largest
def second_largest_optimized(arr):
    if len(arr) < 2:
        return None

    first, second = float('-inf'), float('-inf')

    for num in arr:
        if num > first:
            second = first
            first = num
        elif first > num > second:
            second = num

    return second if second != float('-inf') else None

# Time Complexity:
# This has a time complexity of O(n) because we only iterate over the array once.
# This is much faster than O(n log n) for large arrays.
