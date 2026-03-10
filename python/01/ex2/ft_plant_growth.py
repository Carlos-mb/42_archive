#!/usr/bin/env python3

class Plant:
    """Represents a plant with a name, height in cm, and age in days."""

    def __init__(self, name: str, height: int, days: int) -> None:
        """Initialize a plant with a name, height, and age.

        Args:
            name: Plant name.
            height: Height in centimeters.
            days: Age in days.
        """
        self.name = name
        self.height = height
        self.days = days

    def get_info(self) -> str:
        """Return plant information."""
        return (f"{self.name}: {self.height}cm, {self.days} days old")

    def grow(self, cm: int) -> None:
        """Increase plant height by the given centimeters.

        Args:
            cm: Height increment in centimeters.
        """
        self.height += cm

    def age(self, days: int) -> None:
        """Increase plant age by the given number of days.

        Args:
            days: Number of days to add.
        """
        self.days += days


def show_grow(plant: Plant, days: int, grow: int) -> None:
    """Print a 1-week growth simulation for one plant.

    Args:
        plant: Plant instance to simulate.
        days: Number of days to advance.
        grow: Height increment in centimeters.
    """
    print("=== Day 1 ===")
    print(plant.get_info())
    initial_height = plant.height
    print("=== Day 7 ===")
    plant.age(days)
    plant.grow(grow)
    print(plant.get_info())
    print(f"Growth this week: +{plant.height - initial_height}cm")


def main() -> None:
    """Entry point for the project."""
    days_passed = 6
    rose = Plant("Rose", 25, 30)
    sunflower = Plant("Sunflower", 80, 45)
    cactus = Plant("Cactus", 15, 120)
    show_grow(rose, days_passed, 6)
    show_grow(sunflower, days_passed, 2)
    show_grow(cactus, days_passed, 1)


if __name__ == "__main__":
    main()
