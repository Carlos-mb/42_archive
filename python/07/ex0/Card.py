from abc import ABC, abstractmethod


class Card(ABC):

    def __init__(self, name: str, cost: int, rarity: str) -> None:
        self.name: str = name
        self.cost: int = cost
        self.rarity: str = rarity

    # Not required, but it make the system more flexible
    card_type: str = "Generic"

    @abstractmethod
    def play(self, game_state: dict) -> dict:
        ...

    def get_card_info(self) -> dict:
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "type": self.__class__.__name__
            }

    def is_playable(self, available_mana: int) -> bool:
        return available_mana >= self.cost

    def get_impact(self) -> int:
        return 0
