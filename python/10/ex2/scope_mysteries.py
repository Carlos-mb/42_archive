from typing import Callable, Any


def mage_counter() -> Callable:
    count: int = 0

    def my_func() -> int:
        nonlocal count
        count += 1
        return count
    return my_func


def spell_accumulator(initial_power: int) -> Callable:
    total: int = initial_power

    def my_func(to_sum: int) -> int:
        nonlocal total
        total += to_sum
        return total
    return my_func


def enchantment_factory(enchantment_type: str) -> Callable:
    def my_func(item_name: str) -> str:
        return enchantment_type + " " + item_name
    return my_func


def memory_vault() -> dict[str, Callable]:
    my_dict = {}

    def store(key: str, value: Any) -> None:
        my_dict[key] = value

    def recall(key: str) -> Any:
        return (my_dict.get(key, "Memory not found"))

    return {"store": store, "recall": recall}


def main() -> None:
    # -----------------------------
    print("Testing mage counter...")
    counter = mage_counter()
    print(f"Call 1: {counter()}")
    print(f"Call 2: {counter()}")
    print(f"Call 3: {counter()}")

    # -----------------------------
    print()
    print("Testing enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))


if __name__ == "__main__":
    main()
