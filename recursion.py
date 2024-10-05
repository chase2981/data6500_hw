lst = [3,4,5,62,3,45,6,7,3]

def print_number(n, i):
    print(n)
    if i+1 < len(lst) and lst[i+1]:
        print_number(lst[i + 1], i+1)

print_number(lst[0], 0)