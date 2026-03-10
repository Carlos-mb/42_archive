from ex3.CardFactory import CardFactory
from ex0.CreatureCard import CreatureCard
from ex1.SpellCard import SpellCard
from ex1.ArtifactCard import ArtifactCard
from ex0.Card import Card


class FantasyCardFactory(CardFactory):

    def __init__(self) -> None:
        self.name = "FantasyCardFactory"

    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        if name_or_power == "dragon":
            return CreatureCard("Fire Dragon", 5, "Legendary", 5, 5)
        elif name_or_power == "goblin":
            return CreatureCard("Goblin Warrior", 2, "Common", 3, 2)
        else:
            raise ValueError("Error. Name or power not allowed")

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        if name_or_power == "fireball":
            return SpellCard("Lightning Bolt", 3, "Common", "damage")
        else:
            raise ValueError("Error: name_or_power does not exist")

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        if name_or_power == "mana_ring":
            return ArtifactCard("Mana Ring", 2, "Rare", 3, "+1 mana")
        else:
            raise ValueError("Error: name_or_power does not exist")

    def create_themed_deck(self, size: int) -> dict:
        # deck can't be a dict of craetures because a deck has te be
        # ordered. In the PDF output it apperas as a list, limited
        # by []
        # But the method has to return a dict !!!. So, I create a
        # single element in the dict
        deck = [
            self.create_creature("dragon"),
            self.create_creature("goblin"),
            self.create_spell("fireball")
        ]
        return {"deck": deck[:size]}

    def get_supported_types(self) -> dict:
        return {
            "creatures": ["dragon", "goblin"],
            "spells": ["fireball"],
            "artifacts": ["mana_ring"]
        }
