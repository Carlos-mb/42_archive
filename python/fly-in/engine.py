from fly_in_map import Map, Hub, Connection
from collections.abc import Iterator
from common import ZoneType


class EngineException(Exception):
    pass


class Engine:
    def __init__(self, map: Map):

        self.map: Map = map
        self.hub_occupancy: dict[Hub, int] = {}
        self.connection_usage: dict[Connection, int] = {}
        self.distance_to_goal: dict[Hub, int] = {}
        self.turn: int = 0
        self.zzvisited: dict[int, dict[Hub, float]] = {}
        self.zzfreezed: list[int] = []

        if not self.map.start:
            raise EngineException("Engine error: no start defined")
        else:
            # Drones are not stored, just referenced in two lists
            # List[0] is related to Drone 0

            self.finished: list[bool] = []
            self.drone_pos: list[Hub] = []
            for i in range(map.nb_drones):
                self.drone_pos.append(self.map.start)
                self.finished.append(False)
                self.zzvisited[i] = {}  # Agregar esta línea

        # Dicts intialitation.
        for conn in map.connections:
            self.connection_usage[conn] = 0

        for hub in map.hubs.values():
            self.hub_occupancy[hub] = 0

        # if self.map.start:
        #     self.hub_occupancy[self.map.start] = self.map.nb_drones
        # else:
        #     raise EngineException("Error: not start deffined")

        self.calc_distances()

    def calc_distances(self) -> None:

        # Distance is not the same than cost. restristed hubs have the same
        # distance, but more cost. In this method we only calc the distance.

        if not self.map.end:
            raise EngineException("Engine error: not end assigned")

        # block deadlocks
        deleted: bool = True
        while deleted:
            deleted = False
            connections = self.map.connections.copy()
            for con in connections:
                for hub in con.hubs:
                    if hub != self.map.start and hub != self.map.end:
                        summ: int = 0
                        for con2 in self.map.connections:
                            if con2.hubs[0] == hub or con2.hubs[1] == hub:
                                summ += 1
                        if summ <= 1:
                            if con in self.map.connections:
                                deleted = True
                                self.map.connections.remove(con)

        self.distance_to_goal[self.map.end] = 0
        changed: bool = True
        i: int = 0
        while changed:
            changed = False
            for con in self.map.connections:
                hub1, hub2 = con.hubs
                if self.distance_to_goal.get(hub1, -1) == -1 and \
                   self.distance_to_goal.get(hub2, -1) == i:

                    self.distance_to_goal[hub1] = i + 1

                    changed = True

                elif self.distance_to_goal.get(hub2, -1) == -1 and \
                        self.distance_to_goal.get(hub1, -1) == i:

                    self.distance_to_goal[hub2] = i + 1

                    changed = True
            i = i + 1

    def put(self, drone: int, dst: Hub) -> bool:

        if dst.max_drones > self.hub_occupancy.get(dst, 0):  # double check

            src = self.drone_pos[drone]
            self.hub_occupancy[src] -= 1
            self.drone_pos[drone] = dst
            self.hub_occupancy[dst] = self.hub_occupancy.get(dst, 0) + 1

            for conn in self.map.connections:
                if src in conn.hubs and dst in conn.hubs:
                    self.connection_usage[conn] += 1

            # Increase cost each time it's visited
            self.zzvisited[drone][dst] = self.zzvisited[drone].get(dst, 0)+0.2

            if dst.zone_type == ZoneType.RESTRICTED:
                if drone in self.zzfreezed:
                    raise EngineException("Engine: can't mmove "
                                          f"freesed drone {drone} !!")
                self.zzfreezed.append(drone)
            return True

        return False

    def able_neighbors(self, hub: Hub) -> Iterator["Hub"]:
        for conn in self.map.connections:
            if self.connection_usage[conn] < conn.capacity:
                other = conn.other(hub)
                if (
                    other is not None
                    and other is not self.map.start
                    and other.zone_type != ZoneType.BLOCKED
                ):
                    if other.max_drones > self.hub_occupancy[other]:
                        yield other

    def movement_cost(self, hub: Hub) -> float:
        cost: float = self.distance_to_goal[hub]
        if hub.zone_type == ZoneType.RESTRICTED:
            cost += 1
        elif hub.zone_type == ZoneType.PRIORITY:
            cost -= 0.1

        return cost

    def try_to_move(self, ndrone: int) -> None:

        if ndrone in self.zzfreezed:
            self.zzfreezed.remove(ndrone)
            return

        try:
            hub_src = self.drone_pos[ndrone]
            hub_closest: Hub | None = None
            # others_neighbors: list[Hub] = []

            for neighbor in self.able_neighbors(hub_src):
                if hub_closest is None or \
                        self.movement_cost(neighbor)  \
                        < (
                            self.movement_cost(hub_closest)
                            + self.zzvisited[ndrone].get(hub_closest, 0)
                        ):

                    hub_closest = neighbor
#                    others_neighbors.append(hub_closest)

            if hub_closest is not None:
                if not self.put(ndrone, hub_closest):
                    pass
                    # for planb in others_neighbors:
                    #     if self.put(ndrone, planb):
                    #         break
        except Exception:
            raise EngineException("Engine error: "
                                  f"no position for drone {ndrone}")
