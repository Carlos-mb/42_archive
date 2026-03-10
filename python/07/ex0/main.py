from ex0.CreatureCard import CreatureCard


def main() -> None:
    print("\n=== DataDeck Card Foundation ===\n")
    print("Testing Abstract Base Class Design:\n")

    # Create creature
    creature = CreatureCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        health=5
    )

    # Show card info
    print("CreatureCard Info:")
    print(creature.get_card_info())

    # Test playable with enough mana
    print("\nPlaying Fire Dragon with 6 mana available:")
    playable = creature.is_playable(6)
    print(f"Playable: {playable}")

    if playable:
        result = creature.play({})
        print("Play result:", result)

    # Attack demonstration
    print("\nFire Dragon attacks Goblin Warrior:")
    attack_result = creature.attack_target("Goblin Warrior")
    print("Attack result:", attack_result)

    # Test insufficient mana
    print("\nTesting insufficient mana (3 available):")
    playable_low = creature.is_playable(3)
    print(f"Playable: {playable_low}")

    print("\nAbstract pattern successfully demonstrated!")


if __name__ == "__main__":
    main()
