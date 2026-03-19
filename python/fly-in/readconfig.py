from io import TextIOWrapper
from typing import Any, TypeAlias
from common import (ZoneType,
                    KW_CONNECTION,
                    KW_END_HUB,
                    KW_HUB,
                    KW_NB_DRONES,
                    KW_START_HUB)


class ConfigError(Exception):
    """
    Exception raised for errors encountered in the configuration process.

    Attributes:
        message -- explanation of the error (optional)
    """
    pass


Cfg: TypeAlias = dict[str, Any]


def readconfig(filename: str) -> Cfg:
    """
    Read and validate a map configuration file.

    Loads required entries and returns them in `cfg` with this shape:

    {
        "nb_drones": int,
        "start_hub": str,
        "end_hub": str,
        "hub": {
            "<hub_name>": {
                "x": int,
                "y": int,
                "zone": ZoneType,      # default: ZoneType.NORMAL
                "color": str,           # default: ""
                "max_drones": int       # default: 1
            },
            ...
        },
        "connection": dict[tuple[str, str], int]
    }

    Args:
        filename: Path to the configuration file.

    Returns:
        Parsed configuration dictionary (`cfg`).

    Raises:
        ConfigError
    """
    cfg: Cfg = {}
    try:
        with open(filename) as f:

            cfg[KW_HUB] = {}
            cfg[KW_CONNECTION] = {}

            read_nbdrones(f, cfg)  # Mandatory, 1st line

            line = get_next_line(f)

            while line:
                if (line.startswith(f"{KW_START_HUB}:") or
                        line.startswith(f"{KW_END_HUB}:") or
                        line.startswith(f"{KW_HUB}:")):
                    read_hub(line, cfg)
                elif line.startswith(KW_CONNECTION):
                    read_connection(line, cfg)
                else:
                    raise ConfigError("Unknown key in "
                                      f"config file:'{line.strip()}'")

                line = get_next_line(f)
    except FileNotFoundError as e:
        raise ConfigError(f"Configuration file '{filename}' not found") from e

    for key in [KW_NB_DRONES, KW_START_HUB, KW_END_HUB, KW_CONNECTION]:
        if key not in cfg:
            raise ConfigError(f"Missing required configuration: {key}")

    if len(cfg[KW_CONNECTION]) == 0:
        raise ConfigError("Missing required configuration: connections")

    for conn in cfg[KW_CONNECTION]:
        if conn[0] not in cfg[KW_HUB] or \
           conn[1] not in cfg[KW_HUB]:
            raise ConfigError(f"Connection {conn} has undefined hub(s)")

    for hub in cfg[KW_HUB]:
        exist: bool = False
        for conn in cfg[KW_CONNECTION]:
            if conn[0] == hub or conn[1] == hub:
                exist = True
        if not exist:
            raise ConfigError(f"Hub {hub} has no connections")

        for hub2 in cfg[KW_HUB]:
            if hub != hub2:
                if cfg[KW_HUB][hub]["x"] == cfg[KW_HUB][hub2]["x"] and \
                   cfg[KW_HUB][hub]["y"] == cfg[KW_HUB][hub2]["y"]:
                    raise ConfigError(f"Hubs {hub} and {hub2}"
                                      " have same coords")

    return cfg


def get_next_line(f: TextIOWrapper) -> str:
    line: str = "#"
    while line and (line.strip() == "" or line.strip().startswith("#")):
        line = f.readline()

    return line


def read_nbdrones(f: TextIOWrapper, cfg: Cfg) -> None:
    line = get_next_line(f)
    if line.startswith(KW_NB_DRONES):
        try:
            value = int(line.split(':')[1].strip())
            if value <= 0:
                raise ConfigError("nb_drones must be a "
                                  "positive integer")
        except (IndexError, ValueError):
            raise ConfigError("Invalid value for nb_drones "
                              "in configuration file")
    else:
        raise ConfigError("nb_drones must be 1st entry "
                          "in configuration file")
    cfg[KW_NB_DRONES] = value


def read_connection(line: str, cfg: Cfg) -> None:

    line_split: list[str] = line.split(":")
    if len(line_split) > 2 or len(line_split) == 1 or \
            line_split[0] != KW_CONNECTION:
        raise ConfigError(f"Invalid format in config file:'{line.strip()}'")

    values = line_split[1].strip().split()

    if len(values) > 2:
        raise ConfigError(f"Invalid format in config file:'{line.strip()}'")

    max_capacity: int = 1  # cfg[KW_NB_DRONES]

    if len(values) > 1:
        values[1] = values[1].strip()
        if not values[1].startswith("[max_link_capacity=") or \
           values[1][-1] != "]":
            raise ConfigError("Invalid format in "
                              f"config file:'{line.strip()}'")
        else:
            try:
                max_capacity = int(values[1].split("=")[1][:-1])
            except ValueError:
                raise ConfigError(f"Invalid format capacity:'{line.strip()}'")

            if max_capacity <= 0:
                raise ConfigError(f"Capacity must be > 1:'{line.strip()}'")

    hubs = values[0].strip().split("-")

    if len(hubs) != 2 or not hubs[0] or not hubs[1]:
        raise ConfigError(f"Invalid format in config file:'{line.strip()}'")

    # To prevent duplicates a-b & b-a. Strip() shouldn't be necesary
    hubs = sorted([v.strip() for v in hubs])
    if (hubs[0], hubs[1]) in cfg[KW_CONNECTION]:
        raise ConfigError(f"Duplicated connection:'{line.strip()}'")

    cfg[KW_CONNECTION][(hubs[0], hubs[1])] = max_capacity


def read_hub(line: str, cfg: Cfg) -> None:

    output: dict[str, Any] = {}
    line_split: list[str] = line.split(":")
    if len(line_split) > 2 or len(line_split) == 1:
        raise ConfigError(f"Invalid format in config file:'{line.strip()}'")

    hub_type = line_split[0]
    value = line_split[1].strip().split()  # split(" ") fails if several spaces

    if "-" in value[0]:
        raise ConfigError(f"Invalid zone name:'{line.strip()}'")

    if len(value) < 3:
        raise ConfigError(f"Invalid format in config file:'{line.strip()}'")
    try:
        output["x"] = int(value[1])
        output["y"] = int(value[2])
        output["zone"] = ZoneType.NORMAL
        output["color"] = ""
        output["max_drones"] = 1

        if len(value) > 3:
            if (not (value[3].startswith("[")) or
                    not (value[-1].endswith("]"))):
                raise ConfigError("Invalid format in "
                                  f"config file:'{line.strip()}'")
            value[3] = value[3][1:]
            value[-1] = value[-1][:-1]

            for key_val in value[3:]:
                try:
                    key, val = key_val.split("=")
                except ValueError:
                    raise ConfigError(f"Invalid key-value format {key_val} "
                                      f"in config file:'{line.strip()}'")
                if key == "zone":
                    try:
                        output["zone"] = ZoneType[val.upper()]
                    except KeyError:
                        raise ConfigError("Invalid zone "
                                          f"type:'{line.strip()}'")
                elif key == "max_drones":
                    try:
                        output["max_drones"] = int(val)
                    except ValueError:
                        raise ConfigError("Invalid max_drones "
                                          f"value:'{line.strip()}'")

                else:
                    output[key] = val

        if value[0] in cfg[KW_HUB]:
            raise ConfigError(f"Duplicated hub: '{value[0]}'")

        cfg[KW_HUB][value[0]] = output

        if hub_type == KW_START_HUB:
            if KW_START_HUB in cfg:
                raise ConfigError("Multiple start hubs")
            cfg[hub_type] = value[0]

        if hub_type == KW_END_HUB:
            if KW_END_HUB in cfg:
                raise ConfigError("Multiple end hubs")
            cfg[hub_type] = value[0]

    except ConfigError:
        raise
    except Exception as e:
        raise ConfigError(
                        f"Invalid format in config file: '{line.strip()}'"
                        ) from e

    return
