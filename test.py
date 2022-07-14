def sum_recursion(arr: list):
    if not arr:
        return 0
    return arr[0] + sum_recursion(arr[1:])


def count_recursive(arr: list):
    if not arr:
        return 0
    return 1 + count_recursive(arr[1:])


def max_recursive(arr: list):
    if len(arr) == 2:
        return arr[0] if arr[0] > arr[1] else arr[1]
    sub = max_recursive(arr[1:])
    return arr[0] if arr[0] > sub else sub


a = sum_recursion([1, 2, 3, 4, 5])
print(a)

b = count_recursive([1, 2, 3, 4, 5, 7, 0])
print(b)

c = max_recursive([1, 2, 3, 4, 5, 7, 50])
print(c)
