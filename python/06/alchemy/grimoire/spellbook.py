def record_spell(spell_name: str, ingredients: str) -> str:
    from .validator import validate_ingredients

    validation_result = validate_ingredients(ingredients)

    if "VALID" in validation_result:
        return "Spell recorded: " + spell_name + " (" + validation_result + ")"
    else:
        return "Spell rejected: " + spell_name + " (" + validation_result + ")"
