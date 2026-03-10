if __name__ == "__main__":
    """ Entry point
    It is not possible to generate the sample of subject"""
    print("=== Game Analytics Dashboard ===\n")

    # name and active y/n
    players: dict[str, bool] = {
        "alice": True,
        "bob": True,
        "charlie": True,
        "diana": False}

    player_scores: dict[str, int] = {
        "alice": 2300,
        "bob": 1800,
        "charlie": 2150,
        "diana": 2050}

    achievements: dict[str, list[str]] = {
        "alice": [
            "first_kill",
            "level_10",
            "treasure_hunter",
            "speed_demon",
            "boss_slayer"],
        "bob": [
            "first_kill",
            "level_10",
            "collector"],
        "charlie": [
            "level_10",
            "boss_slayer",
            "treasure_hunter",
            "speed_demon",
            "perfectionist",
            "first_kill",
            "explorer"],
        "diana": [
            "first_kill",
            "level_10",
            "boss_slayer",
            "strategist"]
    }

    player_regions: dict[str, str] = {
        "alice": "north",
        "bob": "east",
        "charlie": "central",
        "diana": "north"}

    scores: list[int] = list(player_scores.values())

    print("=== List Comprehension Examples ===")

    h_scores: list[str] = [
        player for player, score in player_scores.items()
        if score > 2000]

    double_score: list[int] = [score * 2 for score in scores]

    active_players: list[str] = [
        name for name, active in players.items()
        if active]

    print("High scorers (>2000):", h_scores)
    print("Scores doubled:", double_score)
    print("Active players:", active_players)

    print("")
    print("=== Dict Comprehension Examples ===")
    active_player_score: dict[str, int] = {
        player: score for player, score in player_scores.items()
        if player in active_players
        }

    # Len and sum usage
    score_categories: dict[str, int] = {
        "high": len([score for score in scores if score >= 2300]),
        "medium": len([score for score in scores
                       if score > 1800 and score < 2300]),
        "low": sum(1 for score in scores if score <= 1800)
        }

    achievement_counts: dict[str, int] = {
        player: len(achs) for player, achs in achievements.items()}
    print("Player scores (active):", active_player_score)
    print("Score categories:", score_categories)
    print("Achievement counts:", achievement_counts)

    print("")
    print("=== Set Comprehension Examples ===")
    unique_players: set[str] = {
        player for player, active in players.items()
        if active
    }
    unique_achievements: set[str] = {
        achievement
        for ach_list in achievements.values()
        for achievement in ach_list
    }

    active_regions: set[str] = {
        region for region in player_regions.values()
    }

    print("Unique players:", unique_players)
    print("Unique achievements:", unique_achievements)
    print("Active regions:", active_regions)

    print("")
    print("=== Combined Analysis ===")

    total_players: int = len(player_scores)
    total_unique_achievements: int = len(unique_achievements)
    average_score: float = sum(scores) / len(scores)
    # Key es la función a la que se le pasa cada elemento de player_scores
    top_player: str = max(player_scores, key=player_scores.get)

    print("Total players:", total_players)
    print("Total unique achievements:", total_unique_achievements)
    print("Average score:", average_score)
    print(
        f"Top performer: {top_player} "
        f"({player_scores[top_player]} points, "
        f"{achievement_counts[top_player]} achievements)")
