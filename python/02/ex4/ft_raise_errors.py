def check_plant_health(plant_name: str, water_level: int,
                       sunlight_hours: int) -> str:
    """Validate `plant_name`, `water_level`, and `sunlight_hours` or raise."""
    if not plant_name or plant_name.strip() == "":
        raise ValueError("Plant name cannot be empty!")
    if water_level > 10:
        raise ValueError(f"Water level {water_level} is too high (max 10)")
    if water_level < 1:
        raise ValueError(f"Water level {water_level} is too low (min 1)")
    if sunlight_hours > 12:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too high (max 12)")
    if sunlight_hours < 2:
        raise ValueError(f"Sunlight hours {sunlight_hours} is too low (min 2)")

    return f"Plant '{plant_name}' is healthy!"


def test_plant_checks() -> None:
    """Exercise `check_plant_health` with valid and invalid parameter sets."""
    print("=== Garden Plant Health Checker ===")

    print("Testing good values...", end=" ")
    try:
        print(check_plant_health("tomato", 5, 8))
    except ValueError as e:
        print(f"Error: {e}")

    print("Testing empty plant name...", end=" ")
    try:
        check_plant_health("", 5, 8)
    except ValueError as e:
        print(f"Error: {e}")

    print("Testing bad water level...", end=" ")
    try:
        check_plant_health("tomato", 15, 8)
    except ValueError as e:
        print(f"Error: {e}")

    print("Testing bad sunlight hours...", end=" ")
    try:
        check_plant_health("tomato", 5, 0)
    except ValueError as e:
        print(f"Error: {e}")

    print("All error raising tests completed!")


if __name__ == "__main__":
    test_plant_checks()
