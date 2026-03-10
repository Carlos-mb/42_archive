from ex4.TournamentCard import TournamentCard


class TournamentPlatform:

    def __init__(self) -> None:
        self.registered_cards: dict[str, TournamentCard] = {}
        self.matches_played: int = 0
        self._id_counter: int = 1

    def register_card(self, card: TournamentCard) -> str:
        card_id = f"{card.name.lower().replace(' ', '_')}_{self._id_counter}"
        self._id_counter += 1

        self.registered_cards[card_id] = card
        return card_id

    def create_match(self, card1_id: str, card2_id: str) -> dict:

        card1 = self.registered_cards.get(card1_id)
        card2 = self.registered_cards.get(card2_id)

        if not card1 or not card2:
            return {"error": "Invalid card ID"}

        # Simple rule: higher attack wins
        if card1.attack_power >= card2.attack_power:
            winner, loser = card1, card2
            winner_id, loser_id = card1_id, card2_id
        else:
            winner, loser = card2, card1
            winner_id, loser_id = card2_id, card1_id

        winner.update_wins(1)
        loser.update_losses(1)

        winner.calculate_rating()
        loser.calculate_rating()

        self.matches_played += 1

        return {
            "winner": winner_id,
            "loser": loser_id,
            "winner_rating": winner.rating,
            "loser_rating": loser.rating
        }

    def get_leaderboard(self) -> list:

        sorted_cards = sorted(
            self.registered_cards.items(),
            key=lambda item: item[1].rating,
            reverse=True
        )

        leaderboard = []

        for card_id, card in sorted_cards:
            leaderboard.append({
                "id": card_id,
                "name": card.name,
                "rating": card.rating,
                "record": f"{card.wins}-{card.losses}"
            })

        return leaderboard

    def generate_tournament_report(self) -> dict:

        total_cards = len(self.registered_cards)

        if total_cards == 0:
            avg_rating = 0
        else:
            avg_rating = sum(
                card.rating for card in self.registered_cards.values()
            ) // total_cards  # No decimals

        return {
            "total_cards": total_cards,
            "matches_played": self.matches_played,
            "avg_rating": avg_rating,
            "platform_status": "active"
        }
