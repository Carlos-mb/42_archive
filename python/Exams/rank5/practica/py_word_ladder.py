def essiguiente(uno: str, dos: str):

    strike = 0

    if len(uno) != len(dos):
        return False

    for i in range(len(uno)):
        if uno[i] != dos[i]:
            strike += 1
        if strike == 2:
            return False
    return True

def word_ladder(start: str, end: str, sentence: list[str]) -> int:

    if start == "" or end == "":
        return 0

    caminos = [[start]]

    visitados = [start]

    while caminos:
        camino = caminos.pop(0)
        ultima = camino[-1]

        if ultima == end:
            return (len(camino))

        for palabra in sentence:
            if palabra not in visitados:
                if essiguiente(ultima, palabra):
                    # camino.append(palabra) --> ¡¡ No funciona porque guarda la referencia a lista y se mezclan los caminos!!
                    # caminos.append(camino)
                    caminos.append(camino + [palabra])
                    visitados.append(palabra)

    return 0

print(word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5)
print(word_ladder("a", "a", []) == 1)
print(word_ladder("a", "b", []) == 0)
print(word_ladder("a", "ab", ["ab"]) == 0)
print(word_ladder("a", "b", ["b"]) == 2)
print(word_ladder("cat", "dog", ["cot", "cut"]) == 0)
print(word_ladder("hit", "hot", ["hot", "hot"]) == 2)
print(word_ladder("hit", "cog", ["hot", "dot", "lot", "log", "cog"]) == 5)
