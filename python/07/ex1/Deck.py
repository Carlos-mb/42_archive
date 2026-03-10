from ex0.Card import Card
import random


class Deck:

    def __init__(self) -> None:
        self.cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.cards:
            if card.name == card_name:
                self.cards.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop(0)  # pop -> Eliminates and return the card

    def get_deck_stats(self) -> dict:

        statistics: dict[str, int | float] = {}

        total = len(self.cards)
        statistics["total_cards"] = total

        total_cost = 0

        for card in self.cards:
            statistics[card.card_type] = \
                statistics.get(card.card_type, 0) + 1
            total_cost += card.cost

        statistics["avg_cost"] = (
            # IF is applyed before division
            round(total_cost / total, 2) if total > 0 else 0
        )

        return statistics
