from abc import ABC, abstractmethod


class Magical(ABC):
    """Contract for magical capabilities.
    Defines required magic-related behavior."""

    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """Cast a spell on one or more targets."""
        ...

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        """Channel additional mana."""
        ...

    @abstractmethod
    def get_magic_stats(self) -> dict:
        """Return magic-related statistics."""
        ...
