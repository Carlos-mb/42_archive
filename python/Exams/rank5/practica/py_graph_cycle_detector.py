# Tienes un grafo dirigido: cada nodo tiene una lista de destinos.
# Reviso reiteradamente la lista de destinos.
# Cuando un destino no apunta a un origen válido, elimino el destino
# Cuando un origen ya no tiene destinos, elimino el origen.
# Repito la operación hasta que ya no queda nada que quitar
# Si el grafo no está vacío, es que las cionxiones son válidas y devuelve True

def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:

  vivos = {}

  for element in graph:
      vivos[element] = graph[element].copy()

  cambio = True
  while cambio == True:
      cambio = False
      for nodo, conexiones in vivos.items():
          quitar = []
          for conexion in conexiones:
              if conexion not in vivos:
                  quitar.append(conexion)
                  cambio = True
          for conexion in quitar:
              vivos[nodo].remove(conexion)

      quitar = []
      for nodo, conexiones in vivos.items():
          if conexiones == []:
              cambio = True
              quitar.append(nodo)

      for nodo in quitar:
          del vivos[nodo]

  return len(vivos) > 0


# Esta versión es poco elegante y peligrosa, pq modifica la lista que está recorreindo,
# pero es más compacta. Aunque podría dar error... pero por ahora no lo hace :)

def py_graph_cycle_detector_2(graph: dict[int, list[int]]) -> bool:

    vivos = {}

    for element in graph:
        vivos[element] = graph[element].copy()

    cambio = True
    while cambio == True:
        cambio = False
        for nodo, conexiones in vivos.items():
            for conexion in conexiones:
                if conexion not in vivos:                    
                    vivos[nodo].remove(conexion)
                    cambio = True
                    break                    
            if vivos[nodo] == []:
                del vivos[nodo]
                cambio = True
                break

    return len(vivos) > 0

# py_graph_cycle_detector({0: [1], 1: [2], 2: [0]})    # True
print(py_graph_cycle_detector({0: [], 1: [], 2: []}))
# py_graph_cycle_detector({0: [1], 1: [2], 2: []})     # False
# py_graph_cycle_detector({})                          # False



# remaining -> {0: [1],
#               1: [2],
#               2: [0]}

