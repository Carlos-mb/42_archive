class GardenError(Exception):
    """Base garden exception initialized with `message`."""
    def __init__(self, message: str = "Garden error") -> None:
        """Store the optional `message` in the exception."""
        super().__init__(message)


class PlantError(GardenError):
    """Plant-specific garden exception initialized with `message`."""
    def __init__(self, message: str = "Plant error") -> None:
        """Store the optional plant `message` in the exception."""
        super().__init__(message)


class WaterError(GardenError):
    """Water-specific garden exception initialized with `message`."""
    def __init__(self, message: str = "Water error") -> None:
        """Store the optional water `message` in the exception."""
        super().__init__(message)


def test_specific_errors() -> None:
    """Raise and catch `PlantError` and `WaterError` individually."""
    print("Testing PlantError...")
    try:
        raise PlantError("The tomato plant is wilting!")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print("")
    print("Testing WaterError...")
    try:
        raise WaterError("Not enough water in the tank!")
    except WaterError as e:
        print(f"Caught WaterError: {e}")


def test_inheritance_catch() -> None:
    """Show that `GardenError` catches both plant and water subclasses."""
    print("Testing catching all garden errors...")

    try:
        raise PlantError("The tomato plant is wilting!")
    except GardenError as e:
        print(f"Caught a garden error: {e}")

    try:
        raise WaterError("Not enough water in the tank!")
    except GardenError as e:
        print(f"Caught a garden error: {e}")


def main() -> None:
    """Run both custom-exception demos and print final status."""
    print("=== Custom Garden Errors Demo ===")
    print("")
    test_specific_errors()
    print("")
    test_inheritance_catch()
    print("")
    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    main()
