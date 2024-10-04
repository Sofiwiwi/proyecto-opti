import random
import numpy as np
from clases import Asignatura, Sala, Profesor

cantidad_asignaturas = {
    "Medianas": [
        [40,45],
        [54,58],
        [68,72],
        [80,85],
        [95,99]
    ],
    "Grandes": [
        [180,200],
        [210,230],
        [250,270],
        [300,320],
        [340,360]
    ]
}

cantidad_salas = {
    "Medianas": [
        [3,3],
        [4,4],
        [5,5],
        [6,6],
        [7,7]
    ],
    "Grandes": [
        [9,11],
        [12,14],
        [15,17],
        [18,20],
        [21,23]
    ]
}


def generar_asignaturas(c_asignaturas):
    ca_indispensables = round(0.2 * c_asignaturas)
    ca_dispensables = c_asignaturas - ca_indispensables

    cai_cb1 = round(0.65 * ca_indispensables)
    cai_cb2 = ca_indispensables - cai_cb1

    cad_cb1 = round(0.65 * ca_dispensables)
    cad_cb2 = ca_dispensables - cad_cb1

    asignaturas = []

    for i in range(cai_cb1):
        asignaturas.append(Asignatura(True, 1))

    for i in range(cai_cb2):
        asignaturas.append(Asignatura(True, 2))

    for i in range(cad_cb1):
        asignaturas.append(Asignatura(False, 1))

    for i in range(cad_cb2):
        asignaturas.append(Asignatura(False, 2))

    print(f"Indispensables: {ca_indispensables}")

    return asignaturas


def generar_profesores(c_profesores):
    profesores = []

    for i in range(c_profesores):
        profesores.append(Profesor())

    return profesores


def generar_salas(c_salas):
    salas = []

    for i in range(c_salas):
        salas.append(Sala())

    return salas


tamano = "Medianas"
index = 0

c_asignaturas = random.randint(cantidad_asignaturas[tamano][index][0], cantidad_asignaturas[tamano][index][1])
c_salas = random.randint(cantidad_salas[tamano][index][0], cantidad_salas[tamano][index][1])

print(f"Cantidad asignaturas: {c_asignaturas}")
print(f"Cantidad salas: {c_salas}")

asignaturas = generar_asignaturas(c_asignaturas)
salas = generar_salas(c_salas)

# Print funcion objetivo
print("max: ", end="")

print(" + ".join([f"{asignaturas[i].prioridad} l{i+1}" for i in range(c_asignaturas)]), end=";\n")

print("\n/* Restricciones */")
print("\n/* Restriccion 1: Todas las asignaturas indispensables deben tener sala asignada */")

c = 0
t = ""
for i in range(c_asignaturas):
    if asignaturas[i].indispensable:
        c += 1

        if t == "":
            t = f"l{i+1} "
        else:
            t += f"+ l{i+1} "

print(f"{t} = {c};")

print("\n/* Restriccion 2: Bloques ocupados de los profesores */")
for a in range(c_asignaturas):
    asignatura = asignaturas[a]
    profesor = asignatura.profesor
    bloques = profesor.bloques

    t = " + ".join([f"x[{a+1},{bloque[0]},{bloque[1]}, {s+1}]" for s in range(c_salas) for bloque in bloques])
    print(f"{t} <= 0;")

print("\n/* Restriccion 3: Bloques deben ser consecutivos y en la misma sala para asignaturas con 2 bloques a la semana */")
for a in range(c_asignaturas):
    asignatura = asignaturas[a]
    profesor = asignatura.profesor
    bloques = profesor.bloques

    t = " + ".join([f"x[{a+1},{bloque[0]},{bloque[1]}, {s+1}]" for s in range(c_salas) for bloque in bloques])
    print(f"{t} <= 0;")