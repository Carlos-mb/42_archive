from ex3.CardFactory import CardFactory
from ex3.GameStrategy import GameStrategy


class GameEngine:

    def __init__(self) -> None:
        self.turns_simulated = 0
        self.total_damage = 0
        self.cards_created = 0

    def configure_engine(self, factory: CardFactory,
                         strategy: GameStrategy) -> None:
        self.factory: CardFactory = factory
        self.strategy: GameStrategy = strategy

    def setup_game(self, deck_size: int) -> None:
        themed = self.factory.create_themed_deck(deck_size)
        self.hand = themed["deck"]
        self.cards_created = len(self.hand)

    def simulate_turn(self) -> dict:

        hand_str = ", ".join(f"{c.name} ({c.cost})" for c in self.hand)
        print(f"Hand: [{hand_str}]")

        battlefield = ["Enemy Player"]
        result = self.strategy.execute_turn(self.hand, battlefield)

        self.turns_simulated += 1
        self.total_damage += result["damage_dealt"]

        return result

    def get_engine_status(self) -> dict:
        return {
            "turns_simulated": self.turns_simulated,
            "strategy_used": self.strategy.get_strategy_name(),
            "total_damage": self.total_damage,
            "cards_created": self.cards_created
        }
