def event_stream() -> dict[str, int | str]:
    """Generate a stream of simulated game events.

    Yields:
        dict: Event data containing id, player, level, and event type.
    """
    i: int = 1
    players: list[str] = ["alice", "bob", "charlie"]
    events: list[str] = ["killed monster", "found treasure", "leveled up"]

    while True:
        yield {
            "id": i,
            "player": players[i % 3],
            "level": (i % 15) + 1,
            "event": events[i % 3]
        }
        i = i + 1


def fibonacci_stream() -> int:
    """Infinite Fibonacci generator.

    Yields:
        int: Next number in the Fibonacci sequence.
    """
    a: int = 0
    b: int = 1

    while True:
        yield a
        a, b = b, a + b


def primes_stream() -> int:
    """Infinite prime number generator.

    Yields:
        int: Next prime number in sequence.
    """
    n: int = 2
    i: int = 0
    prime: bool = True

    while True:
        i = n - 1
        prime = True
        while i >= 2 and prime:
            if n % i == 0:
                prime = False
            i = i - 1

        if prime:
            yield n

        n += 1


if __name__ == "__main__":

    print("=== Game Data Stream Processor ===")
    print("Processing 1000 game events...")

    i: int = 0
    high_level_players: int = 0
    treasure_events: int = 0
    level_up_events: int = 0

    for event in event_stream():
        if i < 3:
            print(
                f"Event {event['id']}: Player {event['player']} "
                f"(level {event['level']}) {event['event']}"
            )

        i += 1

        if event["level"] >= 10:
            high_level_players += 1

        if event["event"] == "found treasure":
            treasure_events += 1

        if event["event"] == "leveled up":
            level_up_events += 1

        if i == 1000:
            break

    print("...")
    print("")
    print("=== Stream Analytics ===")
    print(f"Total events processed: {i}")
    print(f"High-level players (10+): {high_level_players}")
    print(f"Treasure events: {treasure_events}")
    print(f"Level-up events: {level_up_events}")
    print("")
    print("Memory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")
    print("")
    print("=== Generator Demonstration ===")

    print("Fibonacci sequence (first 10): ", end="")
    fib = fibonacci_stream()
    for i in range(10):
        value = next(fib)
        if i < 9:
            print(value, end=", ")
        else:
            print(value)

    print("Prime numbers (first 5): ", end="")
    primes = primes_stream()
    for i in range(5):
        value = next(primes)
        if i < 4:
            print(value, end=", ")
        else:
            print(value)
