def main():
    print("=== Import Transmutation Mastery ===")
    print()
    print("Method 1 - Full module import:")
    import alchemy.elements
    print("alchemy.elements.create_fire():", alchemy.elements.create_fire())
    print()
    print("Method 2 - Specific function import:")
    from alchemy.elements import create_water
    print("create_water():", create_water())
    print()
    print("Method 3 - Aliased import:")
    from alchemy.potions import healing_potion as heal
    print("heal():", heal())
    print()
    print("Method 4 - Multiple imports:")
    from alchemy.elements import create_earth, create_fire
    print("create_earth():", create_earth())
    print("create_fire():", create_fire())
    from alchemy.potions import strength_potion
    print("strength_potion():", strength_potion())
    print()
    print("All import transmutation methods mastered!")


if __name__ == "__main__":
    main()
