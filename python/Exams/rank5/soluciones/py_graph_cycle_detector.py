def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
    for node in graph:
        if visit(graph, node, []):
            return True
    return False


def visit(graph: dict[int, list[int]], node: int, path: list[int]) -> bool:
    if node in path:
        return True
    for neighbor in graph.get(node, []):
        if visit(graph, neighbor, path + [node]):
            return True
    return False

# py_graph_cycle_detector({0: [1], 1: [2], 2: [0]})    # True
# py_graph_cycle_detector({0: [1], 1: [2], 2: []})     # False
# py_graph_cycle_detector({})                          # False