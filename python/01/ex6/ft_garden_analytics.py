#!/usr/bin/env python3

class Plant:
    """Represents a plant with a name, height in cm, and age in days."""

    def __init__(self, name: str, height: int, age: int) -> None:
        """Initialize plant attributes and validate values.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
        """
        self.name: str = name
        self.__age: int = 0
        self.__height: int = 0
        self.total_grow: int = 0
        self.human_name: str = "Regular"
        self.set_height(height)
        self.set_age(age)

    @staticmethod
    def is_positive(number: int) -> bool:
        """Return True when the provided number is non-negative.

        Args:
            number: Value to validate.
        """
        return number >= 0

    def get_info(self) -> str:
        """Return plant information."""
        return f"{self.name}: {self.get_height()}cm"

    def set_age(self, age: int) -> None:
        """Set plant age in days.

        Args:
            age: Age in days.
        """
        if not self.is_positive(age):
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
        else:
            self.__age = age

    def set_height(self, height: int) -> None:
        """Assign plant height in centimeters.

        Args:
            height: Height in centimeters.
        """
        if not self.is_positive(height):
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
        else:
            self.__height = height

    def get_height(self) -> int:
        """Return plant height in centimeters."""
        return (self.__height)

    def get_age(self) -> int:
        """Return plant age in days."""
        return (self.__age)

    def grow(self, cm: int) -> None:
        """Increase height by the given amount if it is non-negative.

        Args:
            cm: Height increment in centimeters.
        """
        if self.is_positive(cm):
            self.total_grow += cm
            self.set_height(self.get_height() + cm)
            print(f"{self.name} grew {cm}cm.")
        else:
            print("Height must be positive")


class FloweringPlant(Plant):
    """Represents a flowering plant with a color."""
    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        """Initialize a flowering plant with color.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
            color: Flower color.
        """
        super().__init__(name, height, age)
        self.color: str = color
        self.human_name = "Flowering"

    def bloom(self) -> None:
        """Display a blooming message."""
        print(f"{self.name} is blooming beautifully!")

    def get_info(self) -> str:
        """Return flowering plant information."""
        return (f"{self.name}: {self.get_height()}cm, "
                f"{self.color} flowers (blooming)")


class PrizeFlower(FloweringPlant):
    """Represents a flowering plant with prize points."""
    def __init__(self, name: str, height: int, age: int,
                 color: str, prize_points: int) -> None:
        """Initialize a prize flower with points.

        Args:
            name: Plant name.
            height: Height in centimeters.
            age: Age in days.
            color: Flower color.
            prize_points: Initial prize points.
        """
        super().__init__(name, height, age, color)
        self.prize_points: int = prize_points
        self.human_name = "Prize flowers"

    def add_prize(self) -> None:
        """Increase the prize points by one."""
        self.prize_points += 1

    def get_info(self) -> str:
        """Return full information for the prize flower."""
        return (f"{self.name}: {self.get_height()}cm, "
                f"{self.color} flowers (blooming), "
                f"Prize points: {self.prize_points}")


class GardenManager:
    """Manage a garden owner and their collection of plants.
    Each GardenManager instance has the information of each garden.
    GardenManager class keep the statistics in the class.
    """
    total_gardens: int = 0
    gardens: dict[int, "GardenManager"] = {}

    def __init__(self, owner: str) -> None:
        """Initialize a garden manager with an owner name.

        Args:
            owner: Garden owner name.
        """
        self.owner: str = owner
        self.stats: GardenManager.GardenStats = self.GardenStats(self)
        self.plants: list[Plant] = []
        self.total_plants: int = 0
        self.score: int = 0

        GardenManager.total_gardens += 1
        self.id: int = GardenManager.total_gardens
        GardenManager.gardens[self.id] = self

    def add_plant(self, plant: Plant) -> None:
        """Add one plant to the managed garden.

        Args:
            plant: Plant instance to add.
        """
        self.plants.append(plant)
        self.total_plants += 1
        self.stats.totals_types[plant.human_name] = (
            self.stats.totals_types.get(plant.human_name, 0) + 1
        )

        print(f"Added {plant.name} to {self.owner}'s garden.")

    def grow_all(self) -> None:
        """Grow all managed plants by one centimeter."""
        if self.plants:
            print(f"{self.owner} is helping all plants grow...")
            for plant in self.plants:
                plant.grow(1)

    class GardenStats():
        """Nested helper for calculating garden analytics.
        I think it make no sense to be a nested class instead of a method,
        but it appears to be a requirement of the exercise.
        """
        def __init__(self, garden: "GardenManager") -> None:
            """Initialize garden statistics for the given garden.

            Args:
                garden: Garden manager to analyze.
            """
            self.__garden: GardenManager = garden
            self.totals_types: dict[str, int] = {}
            self.__score: int = 0
            self.__height_ok: bool = True

        def show(self) -> None:
            """Display garden statistics report."""
            total_grow: int = 0
            print(f"=== {self.__garden.owner}'s Garden Report ===")
            if self.__garden.plants:
                print("Plants in garden:")
                for plant in self.__garden.plants:
                    print(f"- {plant.get_info()}")
                    total_grow += plant.total_grow
                msg: str = (
                    f"Plants added: {self.__garden.total_plants}, "
                    f"Total growth: {total_grow}cm"
                )
                print(msg)

                # Format plant types on one line
                type_parts: list[str] = []
                for plant_type, count in self.totals_types.items():
                    type_parts.append(f"{count} {plant_type.lower()}")
                print(f"Plant types: {', '.join(type_parts)}")
                print("")
            else:
                print("There is no plants.")

    @classmethod
    def create_garden_network(cls) -> None:
        """Analyze and print gardens status.
        I can't understand the reason for this, if we already have GardenStats
        and this is called "create network. What network????"
        This classmethod does exist only to demostrate I can use classmethod as
        a method that works on the class itself.
        """
        height_ok: bool = True
        if cls.total_gardens > 0:
            for garden in cls.gardens:
                cls.gardens[garden].score = 0
                for plant in cls.gardens[garden].plants:
                    if plant.get_height() < 0:
                        height_ok = False
                    else:
                        cls.gardens[garden].score += plant.get_height()
        print(f"Height validation test: {height_ok}")

        if cls.total_gardens > 0:
            garden_scores: list[str] = []
            for garden in cls.gardens:
                garden_scores.append(
                    f"{cls.gardens[garden].owner}: {cls.gardens[garden].score}"
                )
            print(f"Garden scores - {', '.join(garden_scores)}")

        print(f"Total gardens managed: {cls.total_gardens}")


def main() -> None:
    """Entry point for garden analytics.
       Using vars (rose) and direct creation
    """

    # Check behavior with no gardens
    GardenManager.create_garden_network()
    print("")

    print("=== Garden Management System Demo ===")
    print("")
    carlos_garden: GardenManager = GardenManager("Carlos")
    carlos_garden.add_plant(Plant(name="Oak Tree", height=100, age=5))
    rose: PrizeFlower = PrizeFlower(name="Rose", height=1, age=1,
                                    color="Red", prize_points=0)
    carlos_garden.add_plant(rose)
    carlos_garden.add_plant(FloweringPlant(name="Sunflower",
                                           height=10,
                                           age=3,
                                           color="Yellow"))

    print("")
    carlos_garden.stats.show()

    print("")
    carlos_garden.grow_all()

    print("")
    carlos_garden.stats.show()

    """Can't check validation height because it is protected.
    If I assing __height it will not work. Acording to debug info, the var
    is _Plant_height and it creates a new __height var when I asing it
    from outside the method.

    # Check Height validation test
    print("")
    print("Lets check wrong height")
    carlos_garden.plants[1].__height = - 5
    GardenManager.create_garden_network()
    """

    print("")
    paco_garden: GardenManager = GardenManager("Paco")
    paco_garden.add_plant(Plant("Sad", 1, 1))
    paco_garden.add_plant(Plant("LessSad", 10, 10))

    print("")
    paco_garden.stats.show()
    GardenManager.create_garden_network()


if __name__ == "__main__":
    main()
