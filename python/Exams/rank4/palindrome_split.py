
""" 

Write a function called palindrome_splitter that takes a string s and returns the minimum
number of pieces the string must be cut into such that every piece is a palindrome.

A single character is always considered a palindrome.

If the entire string is already a palindrome, the function must return 1 (it requires no cuts).

If the string has no multi-character palindromes,
the function must return the length of the string (meaning it is split into individual characters).

If the input string is empty, return 0.

>>> palindrome_splitter("abcd")
4 
# Explanation: "a" | "b" | "c" | "d"

>>> palindrome_splitter("aabaa")
1 
# Explanation: "aabaa" is already a palindrome

>>> palindrome_splitter("aab")
2 
# Explanation: "aa" | "b"
 """


def palindrome_splitter2(s:str)->int:

    n = len(s)
    mini = [float("inf")] * (n + 1)
    mini[0] = 0

    for i in range(1, n + 1):
        for j in range(i):
            sub = s[j:i]
            if sub == sub[::-1]:
                mini[i] = min(mini[i], mini[j] + 1)
    return int(mini[n])

# Test cases
if __name__ == "__main__":
    print(palindrome_splitter2("racecarx") == 2)  # "racecar" | "x"    
    print(palindrome_splitter2("abcd") == 4)   # "a" | "b" | "c" | "d"
    print(palindrome_splitter2("aabaa") == 1)  # "aabaa"
    print(palindrome_splitter2("aab") == 2)    # "aa" | "b"
    print(palindrome_splitter2("") == 0)       # cadena vacía
    print(palindrome_splitter2("racecarx") == 2)  # "racecar" | "x"
    print(palindrome_splitter2("aaba") == 2)  # 