#!/usr/bin/env python3

class SecurePlant:
    """Represents a plant with a name, height in cm, and age in days."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize a secure plant and validate initial values.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
        """
        self.name = name
        if age >= 0:
            self.__age = age
        else:
            self.__age = 0
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
            print("Age set to 0")
        if height >= 0:
            self.__height = height
        else:
            self.__height = 0
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
            print("Height set to 0")

    def get_info(self) -> str:
        """Return plant information."""
        return f"{self.name}: {self.get_height()}cm, {self.get_age()} days old"

    def set_age(self, age: int) -> None:
        """Set plant age in days.

        Args:
            age: Age in days.
        """
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self.__age = age
            print(f"Age updated: {age} days [OK]")

    def set_height(self, height: int) -> None:
        """Assign plant height in centimeters.

        Args:
            height: Height in centimeters.
        """
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self.__height = height
            print(f"Height updated: {height}cm [OK]")

    def get_height(self) -> int:
        """Return plant height in centimeters."""
        return (self.__height)

    def get_age(self) -> int:
        """Return plant age in days."""
        return (self.__age)


def main() -> None:
    """SecurePlant class demonstration."""
    print("=== Garden Security System ===")
    print("Plant created: Rose")
    plant = SecurePlant("Rose", 25, 30)
    print("")
    plant.set_height(-5)
    print("")
    plant.set_age(-10)
    print("")
    print(f"Current plant: {plant.get_info()}")
    print("")
    plant = SecurePlant("Tulipan", -1, -10)


if __name__ == "__main__":
    main()
