from ex3.GameEngine import GameEngine
from ex3.FantasyCardFactory import FantasyCardFactory
from ex3.AggressiveStrategy import AggressiveStrategy


def main() -> None:
    print("=== DataDeck Game Engine ===\n")

    engine = GameEngine()
    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()

    print("Configuring Fantasy Card Game...")
    engine.configure_engine(factory, strategy)
    engine.setup_game(3)  # Not required

    # PDF-> Factory does not require getname
    print("Factory:", factory.name)
    print("Strategy:", strategy.get_strategy_name())
    print("Available types:", factory.get_supported_types())
    print()
    print("Simulating aggressive turn...")
    result = engine.simulate_turn()
    print()
    print("Turn execution:")
    print("Strategy:", strategy.get_strategy_name())
    print("Actions:", result)
    print()
    print("Game Report:")
    print(engine.get_engine_status())
    print()
    print("Abstract Factory + Strategy Pattern: Maximum flexibility achieved!")


if __name__ == "__main__":
    main()
