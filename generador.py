#Para las instancias pequeñas, se cuenta con una sala
# Sin embargo, se deberá identificar cuántas asignaturas son 
# necesarias para que la solución se vuelva infactible. Para ello, es necesario generar al menos 5
# instancias y analizar los resultados obtenidos.

import random
import numpy as np

class asignatura():
    
    def __init__(self,nombre, cant_bloques, indispensable, prioridad,profesor,tamaño):
        self.nombre = nombre
        self.cant_bloques = cant_bloques
        self.indispensable = indispensable
        self.prioridad = prioridad
        self.profesor = profesor
        self.tamaño = tamaño

class sala():
    def __init__(self, ocupada, nombre,tamaño, tipo):
        self.ocupada = False
        self.nombre = nombre
        self.tamaño = tamaño

        

    def ocupar(self):
        self.ocupada = True

        
class profesor():
    def __init__(self, nombre, bloques_disponibles):
        self.nombre = nombre
        self.bloques_disponibles = bloques_disponibles


def generador_instancia_asignatira(n_asignaturas, n_bloques):
    asignaturas = []
    for i in range(n_asignaturas):
        nombre = "ASIG" + str(i)
        cant_bloques = random.randint(1, 2)
        if i % 5 == 0:
            indispensable = True
        else:
            indispensable = False
        if indispensable:
            prioridad = random.randint(6, 10)
        else:
            prioridad = random.randint(1, 5)
        profesor = "PROF" + str(random.randint(1, 5))
        asignatura_i = [nombre, cant_bloques, indispensable, prioridad,profesor]
        asignaturas.append(asignatura_i)
    return asignaturas

print(generador_instancia(8, 7))
