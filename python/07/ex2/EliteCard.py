from ex0.Card import Card
from ex2.Combatable import Combatable
from ex2.Magical import Magical


class EliteCard(Card, Combatable, Magical):

    card_type: str = "elite"

    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        attack: int,
        defense: int,
        health: int,
        mana: int,
        spell_power: int
    ) -> None:

        super().__init__(name, cost, rarity)

        if attack <= 0 or defense < 0 or health <= 0:
            raise ValueError("Invalid combat stats")
        if mana < 0 or spell_power < 0:
            raise ValueError("Invalid magic stats")

        # Combat attributes
        self.attack_power = attack
        self.defense = defense
        self.health = health

        # Magical attributes
        self.mana = mana
        self.spell_power = spell_power

    def play(self, game_state: dict) -> dict:
        available_mana = game_state.get("available_mana", 0)

        if not self.is_playable(available_mana):
            return {"error": "Not enough mana."}

        game_state["available_mana"] = available_mana - self.cost

        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Elite unit deployed"
        }

    def defend(self, incoming_damage: int) -> dict:
        damage_blocked = min(self.defense, incoming_damage)
        damage_taken = max(incoming_damage - self.defense, 0)

        self.health -= damage_taken

        return {
            "defender": self.name,
            "damage_taken": damage_taken,
            "damage_blocked": damage_blocked,
            "still_alive": self.health > 0
        }

    def attack(self, target) -> dict:
        try:
            target.defend(self.attack_power)
        except AttributeError:
            return {"error": "Target is not attackable"}

        return {
            "attacker": self.name,
            "target": target.name,
            "damage": self.attack_power,
            "combat_type": "melee"
        }

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack_power,
            "defense": self.defense,
            "health": self.health
        }

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        mana_cost = 3

        if self.mana < mana_cost:
            return {
                "caster": self.name,
                "spell": spell_name,
                "error": "Not enough mana"
            }

        self.mana -= mana_cost

        return {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "magic_damage": self.spell_power,
            "mana_cost": mana_cost
        }

    def channel_mana(self, amount: int) -> dict:
        self.mana += amount

        return {
            "caster": self.name,
            "mana_channeled": amount,
            "current_mana": self.mana
        }

    def get_magic_stats(self) -> dict:
        return {
            "mana": self.mana,
            "spell_power": self.spell_power
        }
