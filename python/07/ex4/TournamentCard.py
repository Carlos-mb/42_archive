from ex0.Card import Card
from ex2.Combatable import Combatable
from ex4.Rankable import Rankable


class TournamentCard(Card, Combatable, Rankable):

    def __init__(
        self,
        name: str,
        cost: int,
        rarity: str,
        attack: int,
        defense: int,
        health: int
    ) -> None:
        super().__init__(name, cost, rarity)

        if attack <= 0 or defense < 0 or health <= 0:
            raise ValueError("Invalid combat stats")

        self.attack_power: int = attack
        self.defense: int = defense
        self.health: int = health

        self.wins: int = 0
        self.losses: int = 0
        self.rating: int = 1200

    # Card
    def play(self, game_state: dict) -> dict:
        # I keep game_state for compatibility by I don't use it
        available_mana = game_state.get("available_mana", 0)

        if not self.is_playable(available_mana):
            return {"error": "Not enough mana."}

        game_state["available_mana"] = available_mana - self.cost

        return {
            "card_played": self.name,
            "mana_used": self.cost,
            "effect": "Tournament card deployed"
        }

    # Combatable
    def attack(self, target) -> dict:
        try:
            target.defend(self.attack_power)
        except AttributeError:
            return {"error": "Target is not attackable"}

        return {
            "attacker": self.name,
            "target": target.name,
            "damage": self.attack_power
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

    def get_combat_stats(self) -> dict:
        return {
            "attack": self.attack_power,
            "defense": self.defense,
            "health": self.health
        }

    # Rankable
    def update_wins(self, wins: int) -> None:
        self.wins += wins

    def update_losses(self, losses: int) -> None:
        self.losses += losses

    def calculate_rating(self) -> int:
        self.rating = 1200 + (self.wins * 10) - (self.losses * 5)
        return self.rating

    def get_rank_info(self) -> dict:
        return {
            "rating": self.rating,
            "wins": self.wins,
            "losses": self.losses
        }

    # Extra helper
    def get_tournament_stats(self) -> dict:
        return {
            **self.get_card_info(),
            **self.get_combat_stats(),
            **self.get_rank_info()
        }
