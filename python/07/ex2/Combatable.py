from abc import ABC, abstractmethod
from typing import Any  # PDF attack() definion vs PDF hint requirement


class Combatable(ABC):
    """This is an contract to action.
    It has no knowledge of the game or cards.
    If you want to be 'combatable', you have to implement: """

    @abstractmethod
    def attack(self, target: Any) -> dict:
        """The PDF says attack(self, target) -> dict:
        and also says:
        • Use type hints for all function signatures and class methods.
        and, in the example, they appear to use .name when printing attack
        """
        ...

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict:
        """Handle incoming damage."""
        ...

    @abstractmethod
    def get_combat_stats(self) -> dict:
        """Return combat-related statistics."""
        ...
