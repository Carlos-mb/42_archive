from .basic import lead_to_gold  # relative same level
from ..potions import healing_potion  # relative upper level


def philosophers_stone():
    gold_result: str = lead_to_gold()
    healing_result: str = healing_potion()
    return ("Philosopher's stone created using " +
            gold_result + " and " + healing_result)


def elixir_of_life():
    return "Elixir of life: eternal youth achieved!"
