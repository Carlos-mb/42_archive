from typing import Callable, Any


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:

    def spell3(*args: Any, **kwargs: Any) -> Any:
        return spell1(*args, **kwargs), spell2(*args, **kwargs)
    return spell3


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def power_mult(*a: Any, **ka: Any) -> Any:
        return base_spell(*a, **ka) * multiplier
    return power_mult


def conditional_caster(condition: Callable, spell: Callable) -> Callable:

    def my_func(*a: Any, **ka: Any) -> Any:
        if condition(*a, **ka):
            return spell(*a, **ka)
        else:
            return "Spell fizzled"

    return my_func


def spell_sequence(spells: list[Callable]) -> Callable:
    def my_func(*a: Any, **ka: Any) -> Any:
        result: list = []
        for spell in spells:
            result.append(spell(*a, **ka))
        return result

    return my_func


def main() -> None:
    # --- Base spells ---
    def fireball(target: str) -> str:
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        return f"Heals {target}"

    def damage_spell(power: int) -> int:
        return power

    def strong_enough(power: int) -> bool:
        return power >= 10

    # -----------------------------
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon")
    print(f"Combined spell result: {result[0]}, {result[1]}")

    # -----------------------------
    print()
    print("Testing power amplifier...")
    amplified = power_amplifier(damage_spell, 3)
    original = damage_spell(10)
    boosted = amplified(10)
    print(f"Original: {original}, Amplified: {boosted}")

    # -----------------------------
    print()
    print("Testing conditional caster...")
    conditional = conditional_caster(strong_enough, damage_spell)
    print(conditional(5))     # Should fizz
    print(conditional(15))    # Should cast

    # -----------------------------
    print()
    print("Testing spell sequence...")
    sequence = spell_sequence([fireball, heal])
    results = sequence("Goblin")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
