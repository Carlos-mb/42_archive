from alchemy.elements import create_fire, create_earth  # absolute


def lead_to_gold():
    fire_result: str = create_fire()
    return "Lead transmuted to gold using " + fire_result


def stone_to_gem():
    earth_result: str = create_earth()
    return "Stone transmuted to gem using " + earth_result
