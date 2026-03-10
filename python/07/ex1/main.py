from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex1.Deck import Deck


def main() -> None:
    print("=== DataDeck Deck Builder ===\n")
    print("Building deck with different card types...")

    deck = Deck()

    creature = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    spell = SpellCard("Lightning Bolt", 3, "Common", "damage")
    artifact = ArtifactCard("Mana Crystal", 4, "Rare", 3, "+1 mana per turn")

    deck.add_card(creature)
    deck.add_card(spell)
    deck.add_card(artifact)

    print("Deck stats:", deck.get_deck_stats())

    print("\nDrawing and playing cards:")
    deck.shuffle()

    game_state = {
        "available_mana": 10,
        "targets": ["Enemy Player"]
    }

    while True:
        try:
            card = deck.draw_card()
        except ValueError:
            break

        print(f"\nDrew: {card.name} ({card.card_type.capitalize()})")
        print("Play result:", card.play(game_state))

    print()
    print("Polymorphism in action: Same interface, different card behaviors!")


if __name__ == "__main__":
    main()
