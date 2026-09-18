def differ_by_one(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    differences = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            differences += 1
    return differences == 1


def word_ladder(start: str, end: str, sentence: list[str]) -> int:
    pending = [(start, 1)]
    visited = [start]
    while pending:
        word, steps = pending.pop(0)
        if word == end:
            return steps
        for candidate in sentence:
            if candidate not in visited and differ_by_one(word, candidate):
                visited.append(candidate)
                pending.append((candidate, steps + 1))
    return 0
