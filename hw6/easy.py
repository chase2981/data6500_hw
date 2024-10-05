# /**
# 1. Given an array of integers, write a function to calculate the sum of all elements in the array.
# Analyze the time complexity of your solution using Big O notation, especially what is the Big O notation of the code you wrote, and include it in the comments of your program.
# */

# Unoptimized sum of array
def sum_of_array_unoptimized(arr):
    total = 0
    for i in range(len(arr)):
        total += arr[i]
    return total

# Time Complexity:
# This has a time complexity of O(n), where n is the number of elements in the array.
# We are iterating over the array and summing up each element, but this is still not the most Pythonic way.

# Optimized sum of array
def sum_of_array_optimized(arr):
    return sum(arr)

# Time Complexity:
# The time complexity remains O(n), where n is the number of elements in the array.
# Python’s built-in sum function is implemented in C, making it more efficient in terms of execution time, even though the Big-O is the same.
