def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
    quedan = list(graph)
    while len(quedan) >0:
        sinsalida = buscasinsalida(graph, quedan)
        if sinsalida is None:
            return True
        quedan.remove(sinsalida)
    return False

def buscasinsalida(graph, quedan):
    for node in quedan:
        existe = False

        for vecino in graph[node]:
            if vecino in quedan:
                existe = True
                break

        if not existe:
            return node
    return None



# def find_dead_end(graph: dict[int, list[int]], remaining: list[int]):
#     for node in remaining:
#         exits = 0
#         for neighbor in graph[node]:
#             if neighbor in remaining:
#                 exits += 1
#         if exits == 0:
#             return node
#     return None


# def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
#     remaining = list(graph)
#     while len(remaining) > 0:
#         dead_end = find_dead_end(graph, remaining)
#         if dead_end is None:
#             return True
#         remaining.remove(dead_end)
#     return False

# py_graph_cycle_detector({0: [1], 1: [2], 2: [0]})    # True
# py_graph_cycle_detector({0: [1], 1: [2], 2: []})     # False
# py_graph_cycle_detector({})                          # False



# remaining -> {0: [1],
#               1: [2],
#               2: [0]}

