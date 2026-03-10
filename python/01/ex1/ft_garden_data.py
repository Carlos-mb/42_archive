#!/usr/bin/env python3

class Plant:
    """Represents a plant with a name, height, and days."""
    def __init__(self, name: str, height: int, days: int) -> None:
        """Initialize a Plant instance.

        Args:
            name: Plant name.
            height: Plant height in centimeters.
            days: Plant age in days.
        """
        self.name = name
        self.height = height
        self.days = days

    def show(self) -> None:
        """Print plant information."""
        print(f"{self.name}: {self.height}cm, {self.days} days old")


def main() -> None:
    """Entry point of the program."""
    plant1 = Plant("Rose", 25, 30)
    plant2 = Plant("Sunflower", 80, 45)
    plant3 = Plant("Cactus", 15, 120)
    print("=== Garden Plant Registry ===")
    plant1.show()
    plant2.show()
    plant3.show()


if __name__ == "__main__":
    main()
