
def compress(s: str) -> str:

    if s == "":
        return("")

    salida = ""
    prev = ""
    i = 0

    while i < len(s):

        letter = s[i]
        salida += letter
        i += 1
        cont = 1

        while i < len(s) and letter == s[i]:
            cont += 1
            i += 1

        if cont > 1:
            salida += str(cont)

    return salida

def decompress(s: str) -> str:


    salida = ""
    prev = ""
    i = 0

    while i < len(s):

        letter = s[i]
        salida += letter
        i += 1
        cont = 0
        
        while i < len(s) and s[i].isdigit():
            cont = cont * 10 
            cont += int(s[i])
            i += 1

        while cont > 1:
            salida += letter
            cont -= 1

    return salida

# print(compress("aabcccccaaa"))
print (compress("aabcccccaaa")== "a2bc5a3")
print (decompress("a2bc5a3") == "aabcccccaaa")
print(("a"*21) +"bcccccaaa")
print(decompress("a21bc5a3"))
print (decompress("a21bc5a3") == (("a"*21) + "bcccccaaa"))
print(compress(("a"*21) +"bcccccaaa"))
print(compress("") == "")