def compress(s: str) -> str:
    result = ""
    i = 0
    while i < len(s):
        char = s[i]
        count = 0
        while i < len(s) and s[i] == char:
            count += 1
            i += 1
        result += char
        if count > 1:
            result += str(count)
    return result


def decompress(s: str) -> str:
    result = ""
    i = 0
    while i < len(s):
        char = s[i]
        i += 1
        number = ""
        while i < len(s) and s[i].isdigit():
            number += s[i]
            i += 1
        if number == "":
            result += char
        else:
            result += char * int(number)
    return result
