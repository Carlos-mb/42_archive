from ex3.GameStrategy import GameStrategy
from ex0.Card import Card
from typing import Any


class AggressiveStrategy(GameStrategy):

    def __init__(self) -> None:
        self.name = "AggressiveStrategy"

    def execute_turn(
        self,
        hand: list[Card],
        battlefield: list[str]
    ) -> dict[str, Any]:

        mana_limit = 5
        mana_used = 0
        cards_played: list[str] = []
        damage_dealt = 0

        # Use battlefield through strategy logic
        targets_attacked = self.prioritize_targets(battlefield)

        # Play lowest cost first
        sorted_hand = sorted(hand, key=lambda c: c.cost)

        for card in sorted_hand:
            if mana_used + card.cost <= mana_limit:
                cards_played.append(card.name)
                mana_used += card.cost

                damage_dealt += card.get_impact()

        return {
            "cards_played": cards_played,
            "mana_used": mana_used,
            "targets_attacked": targets_attacked,
            "damage_dealt": damage_dealt
        }

    def get_strategy_name(self) -> str:
        return self.name

    def prioritize_targets(self, available_targets: list) -> list:
        # Aggressive strategy: attack any target containing "Enemy"
        # I don't know the actual battlefield content.
        return [t for t in available_targets if "Enemy" in t]
