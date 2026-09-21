def py_room_scheduler(meetings: list[list[int]]):

    rooms= []

    # No numero las salas, sólo creo una lista.
    # ordenar por orden de comienzo de reunión es importante
    for meeting in sorted(meetings,key=lambda m: m[0]):
        for room in rooms:
            # porque así sé que a las salas se les van añadiendo las reuniones
            # por orden
            if room[-1][1] <= meeting[0]:
                room.append(meeting)
                break
        else:
            rooms.append([meeting]) # IMPORTANTE; añadir con corchetes para que la nueva sala sea una lista con la primera tupla

    return {"total_rooms": len(rooms), "schedule": rooms}
