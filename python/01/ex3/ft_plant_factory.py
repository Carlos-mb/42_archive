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


def main() -> None:
    """Create and print a predefined set of plants."""
    print("=== Plant Factory Output ===")

    plants = [
        Plant("Rose", 25, 30),
        Plant("Sunflower", 80, 45),
        Plant("Cactus", 5, 120),
        Plant("Baobab", 600, 1095),
        Plant("Carnation", 100, 365),
    ]

    for plant in plants:
        print(f"Created: {plant.name} ({plant.height}cm, {plant.days} days)")

    print(f"Total plants created: {len(plants)}")


if __name__ == "__main__":
    main()
