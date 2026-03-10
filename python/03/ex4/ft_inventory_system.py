if __name__ == "__main__":
    """ Entry point """

    inventories: dict[str, dict[str, dict[str, str | int]]] = {
        "alice": {
            "sword": {
                "category": "weapon",
                "rarity": "rare",
                "quantity": 1,
                "value": 500
            },
            "potion": {
                "category": "consumable",
                "rarity": "common",
                "quantity": 5,
                "value": 50
            },
            "shield": {
                "category": "armor",
                "rarity": "uncommon",
                "quantity": 1,
                "value": 200
            }
        },
        "bob": {
            "potion": {
                "category": "consumable",
                "rarity": "common",
                "quantity": 0,
                "value": 50
            },
            "magic_ring": {
                "category": "accessory",
                "rarity": "rare",
                "quantity": 1,
                "value": 350
            }
        }
    }

    print("=== Player Inventory System ===")
    print("")
    print("=== Alice's Inventory ===")
    inv_value: int = 0
    inv_count: int = 0
    inv_cats: dict[str, int] = {}
    for name, data in inventories["alice"].items():
        print(f"{name} ({data['category']}, {data['rarity']}): "
              f"{data['quantity']}x @ {data['value']} gold each = "
              f"{data['quantity'] * data['value']} gold"
              )
        # int() maybe required because the data has been declared as str | int
        # It is only a warning and I don't use it in the rest of the code
        # I use it here just for learning the concept.
        inv_value += int(data["quantity"]) * int(data["value"])
        inv_count += int(data["quantity"])
        inv_cats[data["category"]] = (inv_cats.get(data["category"], 0) +
                                      int(data["quantity"]))

    print("")
    print(f"Inventory value: {inv_value} gold")
    print(f"Item count: {inv_count} items")
    category_output: str = ""
    for cat, count in inv_cats.items():
        if category_output != "":
            category_output += ", "
        category_output += f"{cat}({count})"

    print(f"Categories: {category_output}")

    print("")
    print("=== Transaction: Alice gives Bob 2 potions ===")
    if inventories["alice"]["potion"]["quantity"] >= 2:
        inventories["alice"]["potion"]["quantity"] -= 2
        inventories["bob"]["potion"]["quantity"] += 2
        print("Transaction successful!")
    else:
        print("Transaction failed!")
    print("")
    print("=== Updated Inventories ===")
    print(f"Alice potions: {inventories['alice']['potion']['quantity']}")
    print(f"Bob potions: {inventories['bob']['potion']['quantity']}")
    print("")
    print("=== Inventory Analytics ===")
    most_gold: str = ""
    most_items: str = ""
    highest_gold: int = 0
    highest_items: int = -1
    rare_items: list[str] = []
    for player in inventories:
        player_gold: int = 0
        player_items: int = 0

        for name, data in inventories[player].items():
            player_gold += int(data["quantity"]) * int(data["value"])
            player_items += int(data["quantity"])
            if data["rarity"] == "rare" and name not in rare_items:
                rare_items.append(name)

        if highest_gold < player_gold:
            highest_gold = player_gold
            most_gold = player

        if highest_items < player_items:
            highest_items = player_items
            most_items = player

    print(f"Most valuable player: {most_gold.capitalize()} "
          f"({highest_gold} gold)")
    print(f"Most items: {most_items.capitalize()} ({highest_items} items)")
    rare_output = ", ".join(rare_items)
    print(f"Rarest items: {rare_output}")
