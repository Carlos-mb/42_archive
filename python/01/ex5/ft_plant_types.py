#!/usr/bin/env python3

class Plant:
    """Represents a plant with a name, height in cm, and age in days."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Create a Plant.

        Args:
            name: Plant name.
            height: Height in centimeters. Negative values are rejected.
            age: Age in days. Negative values are rejected.
        """
        self.name: str = name
        self.__age: int = 0
        self.__height: int = 0
        self.type: str = ""
        self.set_height(height)
        self.set_age(age)

    def get_info(self) -> str:
        """Return plant information."""
        return f"{self.name}: {self.get_height()}cm, {self.get_age()} days old"

    def set_age(self, age: int) -> None:
        """Set plant age in days."""
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
        else:
            self.__age = age

    def set_height(self, height: int) -> None:
        """Assign plant height in centimeters."""
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
        else:
            self.__height = height

    def get_height(self) -> int:
        """Return plant height in centimeters."""
        return (self.__height)

    def get_age(self) -> int:
        """Return plant age in days."""
        return (self.__age)


class Flower(Plant):
    """A flower type of `Plant`."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Create a Flower plant.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
        """
        super().__init__(name, height, age)
        self.color: str = ""
        self.type: str = "Flower"

    def bloom(self) -> None:
        """Print a message indicating the flower is blooming."""
        print(f"{self.name} is blooming beautifully!")

    def get_info(self) -> str:
        """Return flower information."""
        return (f"{self.name} (Flower): {self.get_height()}cm,"
                f" {self.get_age()} days, {self.color} color.")


class Tree(Plant):
    """A tree type of `Plant`."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Create a Tree plant.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
        """
        super().__init__(name, height, age)
        self.trunk_diameter: int = 0
        self.type: str = "Tree"

    def produce_shade(self) -> None:
        """Print an estimated shade area produced by the tree."""
        height_m = self.get_height() / 100
        trunk_m = self.trunk_diameter / 100
        shade_area = int(3.141592 * height_m * (trunk_m * 10))
        print(f"{self.name} provides {shade_area} square meters of shade")

    def get_info(self) -> str:
        """Return tree information."""
        return (f"{self.name} (Tree): {self.get_height()}cm, {self.get_age()}"
                f" days, {self.trunk_diameter} diameter")


class Vegetable(Plant):
    """A vegetable type of `Plant`."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Create a Vegetable plant.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
        """
        super().__init__(name, height, age)
        self.harvest_season: str = ""
        self.nutritional_value: str = ""

    def get_info(self) -> str:
        """Return vegetable information."""
        return (f"{self.name} (Vegetable): {self.get_height()}cm,"
                f" {self.get_age()} days, {self.harvest_season} harvest")


def main() -> None:
    """Specialized Plant Types."""
    print("=== Garden Plant Types ===")
    print()
    rose = Flower("Rose", 25, 30)
    rose.color = "red"
    print(rose.get_info())
    rose.bloom()
    print()
    tulip = Flower("Tulip", 20, 18)
    tulip.color = "yellow"
    print(tulip.get_info())
    tulip.bloom()
    print()
    oak = Tree("Oak", 500, 1825)
    oak.trunk_diameter = 50
    print(oak.get_info())
    oak.produce_shade()
    print()
    pine = Tree("Pine", 350, 1200)
    pine.trunk_diameter = 40
    print(pine.get_info())
    pine.produce_shade()
    print()
    tomato: Vegetable = Vegetable("Tomato", 80, 90)
    tomato.harvest_season = "summer"
    tomato.nutritional_value = "Vitamin C"
    print(tomato.get_info())
    print(f"{tomato.name} is rich in {tomato.nutritional_value}")
    print()
    carrot: Vegetable = Vegetable("Carrot", 25, 70)
    carrot.harvest_season = "fall"
    carrot.nutritional_value = "Vitamin A"
    print(carrot.get_info())
    print(f"{carrot.name} is rich in {carrot.nutritional_value}")


if __name__ == "__main__":
    main()
