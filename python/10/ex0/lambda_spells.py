
def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: "* "+spell+" *", spells))


def mage_stats(mages: list[dict]) -> dict[str, int | float]:

    if len(mages) > 0:
        max_power = max(mages, key=lambda mage: mage["power"])["power"]
        min_power = min(mages, key=lambda mage: mage["power"])["power"]
        # sum(mage["power"] for mage in mages)
        # sum(map(lambda mage: mage["power"], mages)) /
        #                                 sum(map(lambda mage: 1, mages))
        # avg_power = round(sum(map(lambda mage: mage["power"], mages)) /
        #               len(mages), 2) if len(mages) > 0 else 0
        avg_power = round(sum(map(lambda mage: mage["power"], mages)) /
                          len(mages), 2)
    else:
        max_power = 0
        min_power = 0
        avg_power = 0

    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power
    }


if __name__ == "__main__":

    artifacts = [
        {"name": "Fire Staff", "power": 2, "type": "weapon"},
        {"name": "Crystal Orb", "power": 3, "type": "spell"},
        {"name": "Shadow Cloak", "power": 1, "type": "armor"}
    ]

    mages = [
        {"name": "Aldor", "power": 200, "element": "fire"},
        {"name": "Lyra", "power": 100, "element": "ice"},
        {"name": "Dain", "power": 0, "element": "earth"}
    ]

    spells = ["fireball", "heal", "shield"]

    print("Testing artifact_sorter:")
    sorted_artifacts = artifact_sorter(artifacts)
    for artifact in sorted_artifacts:
        print(f"{artifact['name']} ({artifact['power']} power)")
    print()

    print("Testing power_filter (min_power=60):")
    filtered_mages = power_filter(mages, 60)
    for mage in filtered_mages:
        print(f"{mage['name']} ({mage['power']} power)")
    print()

    print("Testing spell_transformer:")
    transformed_spells = spell_transformer(spells)
    for spell in transformed_spells:
        print(spell)
    print()

    print("Testing mage_stats:")
    stats = mage_stats(mages)
    for name, value in stats.items():
        print(f"{name}: {value}")
