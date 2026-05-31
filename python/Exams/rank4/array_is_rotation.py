"""Determine if two arrays are a rotated version of each other"""


def is_rotation(list1,list2):

    if len(list1) != len(list2):
        return False

    if len(list1) == 0 and len(list2) == 0:
        return True

    for n in range(len(list1)):
        sub = list1[n:] + list1[:n]
        if sub == list2:
            return True

    return False


print("\nTrues:")
print(is_rotation([],[]))
print(is_rotation([1, 2, 3], [3, 1, 2]))
print(is_rotation([1, 2, 3, 1, 2, 3],[3, 1, 2, 3, 1, 2]))
print(is_rotation([1, 2, 3, 1, 2, 3],[2, 3, 1, 2, 3, 1]))
print(is_rotation([1, 2, 3, 4, 5, 6],[5, 6, 1, 2, 3, 4]))
print("\nFalses:")
print(is_rotation([1, 2, 3],[3, 1, 4]))
print(is_rotation([1, 2, 3, 1, 2, 3], []))
print(is_rotation([], [1, 2, 3, 1, 2, 3]))
print(is_rotation(["", "", ""], []))