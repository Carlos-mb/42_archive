from common import ZoneType

from collections.abc import Iterator


class Hub:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
    ):

        if max_drones <= 0:
            raise ValueError("Drones capacity must be positive number")

        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.connections: list["Connection"] = []

    # `is` compares object identity (same instance in memory).
    # `==` uses __eq__ for logical equality.
    # `__hash__` is used by hash-based containers (set, dict).

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Hub) and self.name == other.name

    # Human object name for debug
    def __repr__(self) -> str:
        return f"Hub({self.name})"

    # Iterable of neighbors
    def neighbors(self) -> Iterator["Hub"]:
        for conn in self.connections:
            other = conn.other(self)
            if other is not None:
                yield other


class Connection:
    def __init__(self, a: Hub, b: Hub, capacity: int = 1):

        if a == b:
            raise ValueError("Self connection not allowed")

        if capacity <= 0:
            raise ValueError("Connection capacity must be positive")

        for neighbor in a.neighbors():
            if neighbor == b:
                raise ValueError("Duplicated connection")

        for neighbor in b.neighbors():
            if neighbor == a:
                raise ValueError("Duplicated connection")

        self.hubs: tuple[Hub, Hub] = (a, b)
        self.capacity = capacity

        # hubs have connections and connections have hubs references
        a.connections.append(self)
        b.connections.append(self)

    def other(self, hub: Hub) -> Hub | None:
        if hub == self.hubs[0]:
            return self.hubs[1]
        if hub == self.hubs[1]:
            return self.hubs[0]
        return None


class Map:
    def __init__(self, nb_drones: int) -> None:
        self.nb_drones = nb_drones
        self.hubs: dict[str, Hub] = {}
        self.connections: list[Connection] = []
        self.start: Hub | None = None
        self.end: Hub | None = None

    def add_hub(self, hub: Hub) -> None:
        if hub.name in self.hubs:
            raise ValueError("Duplicate hub")
        self.hubs[hub.name] = hub

    def connect(self, a: str, b: str, capacity: int = 1) -> None:
        ha = self.hubs[a]
        hb = self.hubs[b]

        if (ha.zone_type == ZoneType.BLOCKED or
                hb.zone_type == ZoneType.BLOCKED):
            raise ValueError("Cannot connect blocked hubs")

        c = Connection(ha, hb, capacity)
        self.connections.append(c)

    def set_start(self, hub: Hub) -> None:

        # According to subject requirement
        if self.start is not None:
            raise ValueError("Start already defined")

        if hub.name not in self.hubs:
            raise ValueError("Hub not in map")

        self.start = hub

    def set_end(self, hub: Hub) -> None:

        # According to subject requirement
        if self.end is not None:
            raise ValueError("End already defined")

        if hub.name not in self.hubs:
            raise ValueError("Hub not in map")

        self.end = hub
