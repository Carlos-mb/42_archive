import time
from functools import wraps
from typing import Callable, Any


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def my_func(*a: Any, **ka: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        out = func(*a, **ka)
        end = time.perf_counter()
        print(f"Spell completed in {end - start:.3f} seconds")
        return out
    return my_func


def power_validator(min_power: int) -> Callable[..., Any]:
    """Apply a minimum poewr validator.
    Requires the signature ->
        def cast_spell(self, spell_name: str, power: int)"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Check if the first argument (power) is >= min_power
            # def cast_spell(self, spell_name: str, power: int)
            # power is the second explicit parameter
            # not the first
            power = kwargs.get("power")
            if power is None:
                power = args[2]
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable[..., Any]:
    """Retry spell up to max_attempts"""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:

        @wraps(func)
        def wrapper(*args: Any, **kargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kargs)
                except Exception:
                    if attempt == max_attempts:
                        return ("Spell casting failed after "
                                f"{attempt} attempts")
                    else:
                        print("Spell failed, retrying... "
                              f"(attempt {attempt}/{max_attempts})")
        return wrapper
    return decorator


class MageGuild:

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name.strip()) < 3:
            return False
        return all(c.isalpha() or c == " " for c in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":

    print("\nTesting spell timer...")

    @spell_timer
    def fireball():
        time.sleep(0.101)
        return "Fireball cast!"

    print(f"Result: {fireball()}\n")

    print("Testing MageGuild...")

    my_mage_guild = MageGuild()

    print(my_mage_guild.validate_mage_name("Norberto"))
    print(my_mage_guild.validate_mage_name("90"))

    print(my_mage_guild.cast_spell("Lightning", 15))
    print(my_mage_guild.cast_spell("Lightning", 5))
