from ex4.TournamentCard import TournamentCard
from ex4.TournamentPlatform import TournamentPlatform


def main() -> None:
    print("=== DataDeck Tournament Platform ===\n")

    platform = TournamentPlatform()

    print("Registering Tournament Cards...\n")

    card1 = TournamentCard(
        name="Fire Dragon",
        cost=5,
        rarity="Legendary",
        attack=7,
        defense=3,
        health=20
    )

    card2 = TournamentCard(
        name="Ice Wizard",
        cost=4,
        rarity="Epic",
        attack=5,
        defense=4,
        health=18
    )

    id1 = platform.register_card(card1)
    id2 = platform.register_card(card2)

    # Print registration info (PDF-like structure)
    for card_id, card in [(id1, card1), (id2, card2)]:
        rank_info = card.get_rank_info()

        print()
        print(f"{card.name} (ID: {card_id}):")
        print("- Interfaces: [Card, Combatable, Rankable]")
        print(f"- Rating: {rank_info['rating']}")
        print(f"- Record: {rank_info['wins']}-{rank_info['losses']}")

    print("\nCreating tournament match...")

    match_result = platform.create_match(id1, id2)
    print(f"Match result: {match_result}")

    print("\nTournament Leaderboard:")

    leaderboard = platform.get_leaderboard()
    for position, entry in enumerate(leaderboard, start=1):
        print(
            f"{position}. {entry['name']} - "
            f"Rating: {entry['rating']} "
            f"({entry['record']})"
        )

    print("\nPlatform Report:")
    report = platform.generate_tournament_report()
    print(report)

    print("""
=== Tournament Platform Successfully Deployed! ===
All abstract patterns working together harmoniously""")


if __name__ == "__main__":
    main()
