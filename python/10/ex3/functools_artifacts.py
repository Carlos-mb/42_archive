from functools import reduce, partial, lru_cache, singledispatch
import operator
from typing import Callable


def spell_reducer(spells: list[int], operation: str) -> int:

    operations: dict[str, Callable] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,  # "max": lambda x, y: x if x > y else y,
        "min": min  # "min": lambda x, y: x if x < y else y
    }

    if operation in operations:
        if len(spells) >= 2:
            return reduce(operations[operation], spells)
        else:
            raise ValueError("Invalid list. 2 or more items required")
    else:
        raise ValueError("Invalid operation")


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        "fire_enchant":      partial(base_enchantment,
                                     power=50, element="Fire"),
        "ice_enchant":       partial(base_enchantment,
                                     power=50, element="Ice"),
        "lightning_enchant": partial(base_enchantment,
                                     power=50, element="Lightning")
        }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:

    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable:

    @singledispatch
    def my_func(arg: object) -> str:
        return "Unknown spell"

    @my_func.register
    def _(arg: int) -> str:
        return f"Damage spell: {arg}"

    @my_func.register
    def _(arg: str) -> str:
        return f"Enchanting {arg}"

    @my_func.register
    def _(arg: list) -> str:
        return f"Multicast {arg}"

    return my_func


def main() -> None:
    # -----------------------------
    print("Testing spell reducer...")
    spells = [10, 20, 30, 40]

    print(f"Sum: {spell_reducer(spells, 'add')}")
    print(f"Product: {spell_reducer(spells, 'multiply')}")
    print(f"Max: {spell_reducer(spells, 'max')}")

    # -----------------------------
    print()
    print("Testing memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")

    # -----------------------------
    print()
    print("Testing partial enchanter...")

    def base_enchantment(*, power: int, element: str, target: str) -> str:
        return f"{element} enchantment on {target} with {power} power"

    enchantments = partial_enchanter(base_enchantment)
    print(enchantments["fire_enchant"](target="Sword"))
    print(enchantments["ice_enchant"](target="Shield"))

    # -----------------------------
    print()
    print("Testing spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(50))
    print(dispatcher("Armor"))
    print(dispatcher([10, 20, 30]))


if __name__ == "__main__":
    main()
