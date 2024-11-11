def bloques_disponibles(bloques_ocupados):
    bloques = [[a+1,b+1]
               for a in range(7)
               for b in range(5)]

    for bloque in bloques_ocupados:
        bloques.remove(bloque)

    return bloques

