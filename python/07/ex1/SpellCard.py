from ex0.Card import Card


class SpellCard(Card):

    card_type: str = "spell"

    effect_types: dict[str, str] = {
            "damage": "Deal 3 damage to target",
            "heal": "Restore 3 health",
            "buff": "Increase attack by 2",
            "debuff": "Reduce enemy attack by 2"}

    def __init__(self, name: str, cost: int,
                 rarity: str, effect_type: str) -> None:
        super().__init__(name=name, cost=cost, rarity=rarity)

        if effect_type not in self.effect_types:
            raise ValueError("ERROR: Wrong effect_type")
        self.effect_type: str = effect_type
        self.damage = 5  # Just to create the same output than PDF in ex3

    def play(self, game_state: dict) -> dict:
        available_mana = game_state.get("available_mana", 0)

        if not self.is_playable(available_mana):
            return {"error": "Not enough mana."}

        targets = game_state.get("targets", [])

        result = self.resolve_effect(targets)
        result["card_played"] = self.name
        result["mana_used"] = self.cost

        game_state["available_mana"] = available_mana - self.cost

        return result

    def resolve_effect(self, targets: list) -> dict:
        return {
                "effect_type": self.effect_type,
                "targets": targets,
                "effect": self.effect_types[self.effect_type]}

    def get_impact(self) -> int:
        return self.damage
