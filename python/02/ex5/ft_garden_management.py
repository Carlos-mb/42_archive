class Plant:
    """Represents a plant with a name, height in cm, and age in days."""

    def __init__(self, name: str, water: int = 0,
                 broken: bool = False, max_sun: int = 0) -> None:
        """Initialize a plant.

        Args:
            name: Plant name.
            water: Initial water level.
            broken: Whether the sensor is broken.
            max_sun: Maximum sun hours tolerated.
        """
        self.name: str = name
        self.water: int = water
        self.broken: bool = broken
        self.max_sun: int = max_sun


class GardenError(Exception):
    """Base garden exception initialized with `message`."""
    def __init__(self, message: str = "Garden error") -> None:
        """Initialize the exception message.

        Args:
            message: Error message.
        """
        super().__init__(message)


class PlantError(GardenError):
    """Plant-specific garden exception initialized with `message`."""
    def __init__(self, message: str = "Plant error") -> None:
        """Initialize the plant error message.

        Args:
            message: Error message.
        """
        super().__init__(message)


class WaterError(GardenError):
    """Water-specific garden exception initialized with `message`."""
    def __init__(self, message: str = "Water error") -> None:
        """Initialize the water error message.

        Args:
            message: Error message.
        """
        super().__init__(message)


class GardenManager:
    """Manage garden plants and watering system."""

    def __init__(self) -> None:
        """Initialize the manager with default settings."""
        self.plants: list[Plant] = []
        self.irrigation_open: bool = False
        self.water_in_tank: int = 10
        self.sun: int = 8

    def add_plant(self, name: str, water: int = 0,
                  broken: bool = False, max_sun: int = 5) -> None:
        """Add a plant to the garden.

        Args:
            name: Plant name.
            water: Initial water level.
            broken: Whether the sensor is broken.
            max_sun: Maximum sun hours tolerated.
        """
        try:
            if name.strip() == "":
                raise PlantError(
                    "Error adding plant: Plant name cannot be empty!"
                )
            else:
                self.plants.append(Plant(name, water, broken, max_sun))
                print(f"Added {name} successfully.")
        except PlantError as e:
            print(e)

    def water_plants(self) -> None:
        """Water all plants and update tank levels."""
        status: str
        print("Watering plants...")
        try:
            print("Opening watering system")
            self.irrigation_open = True
            for plant in self.plants:
                status = f"Watering {plant.name} - "
                if plant.broken:
                    status += "sensor Error"
                else:
                    if self.water_in_tank <= 0:
                        status += "error"
                        raise GardenError("Not enough water in tank")
                    else:
                        plant.water += 1
                        self.water_in_tank -= 1
                        status += "success."
                print(status)
        except GardenError as e:
            print(f"Caught GardenError: {e}")
        finally:
            print("Closing watering system (cleanup)")
            self.irrigation_open = False

    def check_health(self) -> None:
        """Check plants for water and sun level issues."""

        for plant in self.plants:
            try:
                if plant.water > 10:
                    raise WaterError(
                        f"Error checking {plant.name} "
                        f"water level {plant.water} is too high (max 10)"
                    )
                if plant.water < 1:
                    raise WaterError(
                        f"Error checking {plant.name} "
                        f"water level {plant.water} is too low (min 1)"
                    )
                if plant.max_sun < self.sun:
                    raise PlantError(
                        f"Error checking {plant.name} "
                        f"sun level {self.sun} is too high "
                        f"(max {plant.max_sun})"
                    )
            except GardenError as e:
                print(f"Error checking {plant.name}: {e}")


def main() -> None:
    """Run a simple garden management system test."""
    manager = GardenManager()

    print("=== Garden Management System Test ===")

    print("\nAdding plants...")
    manager.add_plant("Tomato", water=5, max_sun=10)
    manager.add_plant("Lettuce", water=15, max_sun=5)
    manager.add_plant("  ")

    print("\nTesting watering system...")
    manager.water_plants()

    print("\nChecking plant health...")
    manager.check_health()

    print("\nTesting error recovery (tank empty)...")
    manager.water_in_tank = -1
    manager.water_plants()

    print("\nSystem test complete - program didn't crash!")


if __name__ == "__main__":
    main()
