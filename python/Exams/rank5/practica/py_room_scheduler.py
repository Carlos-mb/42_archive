def py_room_scheduler(meetings: list[list[int]]):

    rooms= []
    
    for meeting in sorted(meetings, key=lambda m: m[0]):
        assigned = False
        for room in rooms:
            # print(room)
            # print(room[-1])
            if room[-1][1] <= meeting[0]:
                room.append([meeting[0], meeting[1]])
                assigned = True
                break
        if not assigned:
            rooms.append([[meeting[0], meeting[1]]])

    salida:dict = {}
    salida["total_rooms"] = len(rooms)
    salida["schedule"] = rooms

    return salida

print(py_room_scheduler([[0, 30], [5, 10], [15, 20]]))
# {"total_rooms": 2, "schedule": [[[0, 30]], [[5, 10], [15, 20]]]}

print(py_room_scheduler([]))
# {"total_rooms": 0, "schedule": []}