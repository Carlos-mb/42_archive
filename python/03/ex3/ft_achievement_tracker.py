if __name__ == "__main__":
    """Entry point"""

    print("=== Achievement Tracker System ===")

    alice: set[str] = {
        "first_kill",
        "level_10",
        "treasure_hunter",
        "speed_demon"
    }

    bob: set[str] = {
        "first_kill",
        "level_10",
        "boss_slayer",
        "collector"
    }

    charlie: set[str] = {
        "level_10",
        "treasure_hunter",
        "boss_slayer",
        "speed_demon",
        "perfectionist"
    }

    print("")
    print(f"Player alice achievements: {alice}")
    print(f"Player bob achievements: {bob}")
    print(f"Player charlie achievements: {charlie}")

    print("")
    print("=== Achievement Analytics ===")

    all_achievements: set[str] = alice.union(bob, charlie)
    print(f"All unique achievements: {all_achievements}")
    print(f"Total unique achievements: {len(all_achievements)}")

    print("")
    common: set[str] = alice.intersection(bob, charlie)
    print(f"Common to all players: {common}")

    rare: set[str] = set()

    for element in all_achievements:
        count: int = 0
        if element in alice:
            count += 1
        if element in bob:
            count += 1
        if element in charlie:
            count += 1
        if count == 1:
            rare.add(element)

    print(f"Rare achievements (1 player): {rare}")

    print("")
    print(f"Alice vs Bob common: {alice.intersection(bob)}")
    print(f"Alice unique: {alice.difference(bob)}")
    print(f"Bob unique: {bob.difference(alice)}")
