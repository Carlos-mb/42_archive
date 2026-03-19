import sys
from readconfig import readconfig, Cfg
import pprint
import os
from fly_in_map import Hub, Map
from engine import Engine
from typing import cast
from common import (ZoneType,
                    KW_CONNECTION,
                    KW_END_HUB,
                    KW_HUB,
                    KW_NB_DRONES,
                    KW_START_HUB
                    )


def build_map(cfg: Cfg) -> Map:
    new_map = Map(cast(int, cfg[KW_NB_DRONES]))

    hubs_cfg = cfg[KW_HUB]
    if not isinstance(hubs_cfg, dict):
        raise ValueError("Invalid hub configuration")
    hubs_cfg = cast(dict[str, dict[str, object]], hubs_cfg)

    for name, data in hubs_cfg.items():
        if not isinstance(data, dict):
            raise ValueError(f"Invalid hub data for '{name}'")

        hub = Hub(
            name=name,
            x=cast(int, data["x"]),
            y=cast(int, data["y"]),
            zone_type=cast(ZoneType, data["zone"]),
            color=cast(str, data["color"]),
            max_drones=cast(int, data["max_drones"]),
        )
        new_map.add_hub(hub)

    start_name = cfg[KW_START_HUB]
    end_name = cfg[KW_END_HUB]

    if not isinstance(start_name, str) or not isinstance(end_name, str):
        raise ValueError("Invalid start/end hub configuration")

    new_map.set_start(new_map.hubs[start_name])
    new_map.set_end(new_map.hubs[end_name])

    connections_cfg = cfg[KW_CONNECTION]
    if not isinstance(connections_cfg, dict):
        raise ValueError("Invalid connection configuration")
    connections_cfg = cast(dict[tuple[str, str], int], connections_cfg)

    for a, b in connections_cfg:
        new_map.connect(a, b, connections_cfg[(a, b)])

    return new_map


def main() -> tuple[Engine, Map]:

    colors = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "purple": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "orange": "\033[38;5;208m",
        "brown": "\033[38;5;94m",
        "maroon": "\033[38;5;52m",
        "darkred": "\033[38;5;88m",
        "violet": "\033[38;5;177m",
        "crimson": "\033[38;5;160m",
        "reset": "\033[0m"
        }

    def colored_hub_name(hub: Hub) -> str:
        if os.path.exists("nocolor"):
            return f"{hub.name}"
        hub_color = hub.color.strip().lower() if hub.color else ""
        selected_color = colors.get(hub_color, colors["reset"])
        return f"{selected_color}{hub.name}{colors['reset']}"

    if len(sys.argv) < 2:
        print("Usage: python fly-in.py <map_file>")
        sys.exit(1)

    # Read config
    try:
        cfg = readconfig(sys.argv[1])
        if os.path.exists("debug"):
            pprint.pprint(cfg)
    except Exception as e:
        print("Error:", str(e))
        sys.exit(0)

    # Create map
    try:
        map: Map = build_map(cfg)
        map.nb_drones = cast(int, cfg[KW_NB_DRONES])
    except Exception as e:
        print("Error:", e.args[0])
        sys.exit(0)

    # Create & configure engine
    try:
        engine = Engine(map)
        if os.path.exists("debug"):
            print("\nDistances:")
            for hub in engine.distance_to_goal:
                print(f"\tHub: {hub.name} - {engine.distance_to_goal[hub]}")

        if os.path.exists("debug"):
            print("\nPositions:")
            for i in range(map.nb_drones):
                print(f"\tD{i+1:02d}: {engine.drone_pos[i]}")

    except Exception as e:
        print("Error:", e.args[0])
        sys.exit(0)

    engine.turn = 0
    engine.hub_occupancy[cast(Hub, engine.map.start)] = engine.map.nb_drones

    while not all(pos == map.end for pos in engine.drone_pos) \
            and engine.turn < 300:

        moves_this_turn: list[str] = []
        notmoved: list[int] = []
        engine.turn += 1
        isdeadlock = True

        if os.path.exists("debug"):
            print(f"\n====== TURNO {engine.turn} ======:")
            for i in range(map.nb_drones):
                print(f"\tD{i+1:02d}: {engine.drone_pos[i]}")

        for conn in engine.connection_usage:
            engine.connection_usage[conn] = 0
        engine.hub_occupancy[cast(Hub, map.end)] = 0

        for ndrone in range(map.nb_drones):
            if engine.drone_pos[ndrone] != map.end:

                was_freezed = ndrone in engine.zzfreezed
                old_pos = engine.drone_pos[ndrone]
                engine.try_to_move(ndrone)
                new_pos = engine.drone_pos[ndrone]

                if new_pos != old_pos:  # If dron moved
                    isdeadlock = False
                    if ndrone in engine.zzfreezed:  # If now is in a connection
                        moves_this_turn.append(
                            f"D{ndrone + 1}-"
                            f"{colored_hub_name(old_pos)}-"
                            f"{colored_hub_name(new_pos)}"
                        )
                    else:
                        moves_this_turn.append(
                            f"D{ndrone + 1}-{colored_hub_name(new_pos)}"
                        )
                else:
                    if was_freezed:
                        moves_this_turn.append(
                            f"D{ndrone + 1}-{colored_hub_name(new_pos)}"
                        )
                        isdeadlock = False
                    else:
                        notmoved.append(ndrone)

        moved = True
        while moved:
            moved = False
            notmovedcopy = notmoved.copy()
            for ndrone in notmovedcopy:
                if engine.drone_pos[ndrone] != map.end:
                    old_pos = engine.drone_pos[ndrone]
                    engine.try_to_move(ndrone)
                    new_pos = engine.drone_pos[ndrone]

                    if new_pos != old_pos:
                        if ndrone in engine.zzfreezed:
                            # If now is in a connection
                            moves_this_turn.append(
                                f"D{ndrone + 1}-"
                                f"{colored_hub_name(old_pos)}-"
                                f"{colored_hub_name(new_pos)}"
                            )
                        else:
                            moves_this_turn.append(
                                f"D{ndrone + 1}-{colored_hub_name(new_pos)}"
                            )
                        notmoved.remove(ndrone)
                        moved = True
                        isdeadlock = False

        if True or moves_this_turn:
            # print(f"T{engine.turn}: " + " ".join(moves_this_turn))
            print(" ".join(moves_this_turn))

        if os.path.exists("debug"):
            print("\nPositions (pretended):")
            for i in range(map.nb_drones):
                print(f"\tD{i+1:02d}: {engine.drone_pos[i]}")

        if os.path.exists("debug"):
            print("\nCONN Usage:")
            for con in map.connections:
                print(f"\t{con.hubs[0]}-{con.hubs[1]}: "
                      f"{engine.connection_usage[con]}")

        if os.path.exists("debug"):
            print("\nHUB Ocupation:")
            for hub in map.hubs.values():
                print(f"\t{hub.name}: {engine.hub_occupancy[hub]}")
            print()

        if isdeadlock:
            break

    return engine, map


if __name__ == "__main__":
    main()
