def water_plants(plant_list: list[str | None]) -> None:
    """Water each item in `plant_list`, handling invalid entries in-place."""
    print("Opening watering system")

    try:
        for plant in plant_list:
            try:
                print(f"Watering {plant.capitalize()}")
            except AttributeError:
                print(f"Error: Cannot water {plant} - invalid plant!")
    finally:
        print("Closing watering system (cleanup)")


def test_watering_system() -> None:
    """Run `water_plants` with normal data and an invalid mixed list."""
    print("=== Garden Watering System ===")

    print("\nTesting normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print("Watering completed successfully!")

    print("\nTesting with error...")
    water_plants(["tomato", None])

    print("\nCleanup always happens, even with errors!")


if __name__ == "__main__":
    test_watering_system()
