def compress(s: str) -> str:

    if s == "":
        return ""

    i = 0
    salida = ""

    while i < len(s):
        char = s[i]
        count = 1
        salida = salida + char
        i = i + 1
        while i < len(s) and s[i] == char:
            count += 1
            i += 1
        if count > 1:
            salida = salida + str(count)

    return salida


def decompress(s: str) -> str:

    if s == "":
        return ""

    i:int = 0
    salida = ""

    while i < len(s):
        char = s[i]
        salida = salida + char
        count = 0
        i = i + 1
        while i < len(s) and s[i].isdigit():
            count = count * 10
            count += int(s[i])
            i += 1
        if count > 0:
            count = count -1
            salida = salida + (char * count)

    return salida
