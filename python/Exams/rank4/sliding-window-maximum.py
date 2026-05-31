"""YWrite a function called sliding_window_maximum that takes an array of integers nums and an integer k.
A "window" of size k moves from the far left of the array to the far right.
You can only see the k numbers in the window at a time.
Each time the window moves right by one position, you must record the maximum value within that window.

The function must return a list containing the maximum values for each window position.

If the input array nums is empty, return an empty list [].

If k is less than or equal to 0, return an empty list [].

If k is greater than the length of the array, return an empty list [].
>>> sliding_window_maximum([1, 2, 3, 4, 5], 3)
[3, 4, 5]
# Windows: [1,2,3] -> max is 3. [2,3,4] -> max is 4. [3,4,5] -> max is 5.

>>> sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3)
[3, 3, 5, 5, 6, 7]

>>> sliding_window_maximum([7, 2, 4], 5)
[]
>>> siding_window_maximum([], 2)
[]
"""


def maxSlidingWindow(nums: list[int], k: int) -> list[int]:

    out = []

    try:
        for n in range(len(nums) - k + 1):
            out.append(max(nums[n: n + k]))
    except Exception:
        return []

    return out


print(maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3))
print(maxSlidingWindow([1, 2, 3, 4, 5], 3))
print(maxSlidingWindow([7, 2, 4], 5))
print(maxSlidingWindow([], 2))
print("""[3, 3, 5, 5, 6, 7]
[3, 4, 5]
[]
[]""")
