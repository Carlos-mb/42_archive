from typing import Any


def start_time(meeting: list[int]) -> int:
    return meeting[0]


def py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]:
    rooms = []
    for meeting in sorted(meetings, key=start_time):
        placed = False
        for room in rooms:
            last_meeting = room[-1]
            if last_meeting[1] <= meeting[0]:
                room.append(meeting)
                placed = True
                break
        if not placed:
            rooms.append([meeting])
    return {"total_rooms": len(rooms), "schedule": rooms}
