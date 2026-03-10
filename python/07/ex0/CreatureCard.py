from ex0.Card import Card


class CreatureCard(Card):

    card_type: str = "creature"

    def __init__(self,
                 name: str, cost: int, rarity: str,
                 attack: int, health: int) -> None:

        super().__init__(name, cost, rarity)

        if attack <= 0:
            raise ValueError("Error: attack must be positive integer.")
        elif health <= 0:
            raise ValueError("Error: health must be positive integer.")
        else:
            self.attack: int = attack
            self.health: int = health

    def play(self, game_state: dict) -> dict:
        # In this point of the exercise I'm not managing mana.
        return {
                "card_played": self.name,
                "mana_used": self.cost,
                "effect": "Creature summoned to battlefield"
                }

    def attack_target(self, target: str) -> dict:
        return {
            "attacker": self.name,
            "target": target,
            "damage_dealt": self.attack,
            "combat_resolved": True
            }

    def get_card_info(self) -> dict:
        output: dict[str, str | int] = super().get_card_info()
        output["attack"] = self.attack
        output["health"] = self.health
        return output

    def get_impact(self) -> int:
        return self.attack
