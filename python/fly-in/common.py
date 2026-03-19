from enum import Enum

# Keywords de configuración (cambiables en un solo lugar)
KW_NB_DRONES = "nb_drones"
KW_START_HUB = "start_hub"
KW_END_HUB = "end_hub"
KW_HUB = "hub"
KW_CONNECTION = "connection"


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
