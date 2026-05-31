""" 
Write a function called intersection_finder that takes a list of lists of integers 
and returns a new list containing the common elements found in every sub-list.

An element is only included in the result if it appears in all provided sub-lists.

The resulting list must not contain duplicate values, even if the input lists do.

The order of elements in the result should follow their first appearance in the first sub-list.

If the input is an empty list of lists, or if there is no common intersection, return an empty list.

>>> intersection_finder([[1, 2, 3], [2, 4, 6], [2, 1]])
[2]

>>> intersection_finder([[1, 5, 10], [1, 10, 20], [1, 10, 30]])
[1, 10]

>>> intersection_finder([[1, 2], [3, 4]])
[]
 """


def intersection_finder(lists: list[list[int]]) -> list[int]:
    out = []
    if len(lists) == 0 or len(lists[0]) == 0:
        return out

    for n in lists[0]:
        if all(n in l for l in lists):
            out.append(n)
    return out


def intersection_finder2(lists: list[list[int]]) -> list[int]:
    out = []

    if len(lists) == 0 or len(lists[0]) == 0:
        return out

    found = True
    for i in lists[0]:
        found = True
        for l in lists:
            if i not in l:
                found = False
                break
        if found:
            out.append(i)

    return out

print(intersection_finder([]))
print(intersection_finder([[], []]))
print(intersection_finder([[1, 2, 3], [2, 4, 6], [2, 1]]))
print(intersection_finder([[1, 5, 10], [1, 10, 20], [1, 10, 30]]))
print(intersection_finder([[1, 2], [3, 4]]))
print("...........")
print(intersection_finder2([]))
print(intersection_finder2([[], []]))
print(intersection_finder2([[1, 2, 3], [2, 4, 6], [2, 1]]))
print(intersection_finder2([[1, 5, 10], [1, 10, 20], [1, 10, 30]]))
print(intersection_finder2([[1, 2], [3, 4]]))
