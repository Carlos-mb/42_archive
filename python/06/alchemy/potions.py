from .elements import create_fire, create_water, create_earth, create_air


def healing_potion():
    fire_result: str = create_fire()
    water_result: str = create_water()
    return ("Healing potion brewed with " +
            fire_result + " and " + water_result)


def strength_potion():
    earth_result: str = create_earth()
    fire_result: str = create_fire()
    return ("Strength potion brewed with " +
            earth_result + " and " + fire_result)


def invisibility_potion():
    air_result = create_air()
    water_result = create_water()
    return ("Invisibility potion brewed with " +
            air_result + " and " + water_result)


def wisdom_potion():
    fire_result = create_fire()
    water_result = create_water()
    earth_result = create_earth()
    air_result = create_air()
    return ("Wisdom potion brewed with all elements: " +
            fire_result + ", " +
            water_result + ", " +
            earth_result + ", " +
            air_result)
