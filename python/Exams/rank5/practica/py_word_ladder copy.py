def essiguiente(uno: str, dos: str):

    if len (uno) != len (dos):
        return False

    if uno == dos:
        return False

    strikes = 0

    for i in range(len(uno)):
        if uno[i] != dos[i]:
            strikes += 1

        if strikes == 2:
            return False
        
    return True

def word_ladder(start: str, end: str, sentence: list[str]) -> int:

    # Todos los caminos que voy descubriendo. Una lista por camino.
    paths = [[start]]

    # Todas las palabras que ya están en un camino y no debo reusar
    visitados = [start]

    # Los caminos que agoten las palabras y no lleguen al final, morirán... ya verás
    while paths:

        # Quito el primer camino.
        # Si resultara que puede seguir, se añadirá al final.
        # Si no puede seguir, desaparecerá.
        # Así los más cortos quedan al principio.
        path = paths.pop(0)

        # Qué palabra estoy mirando ahora (la última del camino)
        current = path[-1]

        # Si es la que estoy buscando, ya he terminado.
        if current == end:
            return len(path)

        # Recorro todas la palabras 
        for candidato in sentence:

            # Si la palabra no ha sido visitada y puede ser continuación
            # de la anterior, creo el camino y lo pongo al final de la lista
            # de caminos posibles. 
            # Si no tiene siguiente palabra, habrá muerto.
            if candidato not in visitados and essiguiente(candidato, current):
                visitados.append(candidato)
                paths.append(path + [candidato]) # Suma dos listas: path y una lista con un único elemento

    return 0



print(word_ladder("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5)
print(word_ladder("a", "a", []) == 1)
print(word_ladder("a", "b", []) == 0)
print(word_ladder("a", "ab", ["ab"]) == 0)
print(word_ladder("a", "b", ["b"]) == 2)
print(word_ladder("cat", "dog", ["cot", "cut"]) == 0)
print(word_ladder("hit", "hot", ["hot", "hot"]) == 2)
print(word_ladder("hit", "cog", ["hot", "dot", "lot", "log", "cog"]) == 5)
