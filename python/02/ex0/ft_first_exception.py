def check_temperature(temp_str: str) -> int | None:
    """Validate `temp_str` as an integer temperature in the 0-40C range."""
    try:
        temperature = int(temp_str)
    # flake8 "Do not use base except"
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")
        return None

    if temperature > 40:
        print(f"Error: {temperature}°C is too hot for plants (max 40°C)")
        return None

    if temperature < 0:
        print(f"Error: {temperature}°C is too cold for plants (min 0°C)")
        return None

    print(f"Temperature {temperature}°C is perfect for plants!")
    return temperature


def test_temperature_input() -> None:
    """Run sample calls to `check_temperature` with valid and invalid inputs"""
    print("=== Garden Temperature Checker ===")
    print("")
    print("Testing temperature: 25")
    check_temperature("25")
    print("")
    print("Testing temperature: abc")
    check_temperature("abc")
    print("")
    print("Testing temperature: 100")
    check_temperature("100")
    print("")
    print("Testing temperature: -50")
    check_temperature("-50")
    print("")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature_input()
