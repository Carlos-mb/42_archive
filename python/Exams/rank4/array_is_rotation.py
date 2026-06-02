"""Determine if two arrays are a rotated version of each other"""


def is_rotation(list1,list2):

    if len(list1) != len(list2):
        return False

    if len(list1) == 0:
        return True

    for n in range(len(list1)):
        sub = list1[n:] + list1[:n]
        if sub == list2:
            return True

    return False


def is_rotation_friki(list1, list2):
    # Versión válida para list[int]

    if len(list1) != len(list2):
        return False

    if len(list1) == 0:
        return True


    if sorted(list1) != sorted(list2):
        return False

    doubled = ','.join(map(str, list1 + list1))
    candidate = ','.join(map(str, list2))

    return candidate in doubled

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
print(is_rotation([1, 1, 0], [1, 0, 1]))