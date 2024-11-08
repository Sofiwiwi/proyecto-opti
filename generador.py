from clases import Asignatura, Sala, Profesor
from utility import bloques_disponibles
import numpy as np

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


def generar_LPSolve(asignaturas, salas, file_name):
    c_asignaturas = len(asignaturas)
    c_salas = len(salas)

    array_validez = np.ones((c_asignaturas, 7, 5, c_salas))

    with open(file_name, "w") as file:
        file.write("max: ")

        line = " + ".join([f"{asignaturas[i].prioridad} l{i+1}" for i in range(c_asignaturas)])
        file.write(line + ";\n")

        file.write("\n/* Restricciones */\n")
        file.write("\n/* Restriccion 1: Todas las asignaturas indispensables deben tener sala asignada */\n")

        c = 0
        t = ""
        for i in range(c_asignaturas):
            if asignaturas[i].indispensable:
                c += 1

                if t == "":
                    t = f"l{i+1} "
                else:
                    t += f"+ l{i+1} "

        file.write(f"{t} >= {c};\n")

        file.write("\n/* Restriccion 2: Bloques ocupados de los profesores */\n")

        bloqueados = []

        for a in range(c_asignaturas):
            for s in range(c_salas):
                for bloque in asignaturas[a].profesor.bloques:
                    bloqueados.append(f"x{a+1}_{bloque[0]}_{bloque[1]}_{s+1}")

                    array_validez[a, bloque[0]-1, bloque[1]-1, s] = 0

        '''if len(bloqueados) > 0:
            t = " + ".join(bloqueados)
            file.write(f"{t} <= 0;\n")'''

        file.write("\n/* Restriccion 7: Una asignatura a solo se puede asignar a una sala r que pueda recibir la cantidad de estudiantes de a. */\n")
        for a in range(c_asignaturas):
            for s in range(c_salas):
                if salas[s].capacidad < asignaturas[a].cantEstudiantes:
                    salas_no_disponibles = []

                    for b in range(7):
                        for d in range(5):
                            salas_no_disponibles.append(f"x{a+1}_{b+1}_{d+1}_{s+1}")
                            array_validez[a, b, d, s] = 0

                    if len(salas_no_disponibles) == 0:
                        continue

                    '''t = " + ".join(salas_no_disponibles)
                    file.write(t + " <= 0;\n")'''

        file.write("\n/* Restriccion 3: Si a la asignatura a se le asigna horario serán CBA bloques, si no es asignada serán 0 */\n")
        for a in range(c_asignaturas):
            asignatura = asignaturas[a]
            profesor = asignatura.profesor
            bloques_ocupados = profesor.bloques
            bloques_disp = bloques_disponibles(bloques_ocupados)

            x_arr = [f"x{a+1}_{bloque[0]}_{bloque[1]}_{s+1}"
                    for s in range(c_salas)
                    for bloque in bloques_disp
                    if array_validez[a, bloque[0]-1, bloque[1]-1, s] == 1]
            if len(x_arr) == 0:
                continue
            t = " + ".join(x_arr)
            file.write(f"{t} = {asignatura.cantBloques} l{a+1};\n")

        file.write("\n/* Restriccion 4: Relación entre l_a y x_a_b_d_r o c_a_b_d_r */\n")
        for a in range(c_asignaturas):
            asignatura = asignaturas[a]

            if asignatura.cantBloques == 1:
                x_arr = [f"x{a + 1}_{b+1}_{d+1}_{s + 1}"
                                for b in range(7)
                                for d in range(5)
                                for s in range(c_salas)
                                if array_validez[a, b, d, s] == 1]
                if len(x_arr) == 0:
                    continue
                t = " + ".join(x_arr)
            else:
                x_arr = [f"c{a+1}_{b+1}_{d+1}_{s+1}"
                                for b in range(6)
                                for d in range(5)
                                for s in range(c_salas)
                                if array_validez[a, b, d, s] == 1 and array_validez[a, b+1, d, s] == 1]
                if len(x_arr) == 0:
                    continue
                t = " + ".join(x_arr)
            file.write(t + f" = l{a+1};\n")

        file.write("\n/* Restriccion 5: Bloques consecutivos en la misma sala */\n")
        for a in range(c_asignaturas):
            if asignaturas[a].cantBloques == 1:
                continue

            for b in range(6):
                for d in range(5):
                    for s in range(c_salas):
                        if array_validez[a, b, d, s] == 0 or array_validez[a, b+1, d, s] == 0:
                            continue

                        t = f"x{a+1}_{b+1}_{d+1}_{s+1} + x{a+1}_{b+2}_{d+1}_{s+1}"

                        file.write(t+f" <= c{a+1}_{b+1}_{d+1}_{s+1} + 1;\n")
                        file.write(t+f" >= 2 c{a+1}_{b+1}_{d+1}_{s+1};\n")

        file.write("\n/* Restriccion 6: En una sala se imparte solo una asignatura por bloque */\n")
        for b in range(7):
            for d in range(5):
                for s in range(c_salas):
                    x_arr = [f"x{a+1}_{b+1}_{d+1}_{s+1}"
                                    for a in range(c_asignaturas)
                                    if array_validez[a, b, d, s] == 1]
                    if len(x_arr) == 0:
                        continue

                    t = " + ".join(x_arr)
                    file.write(t + " <= 1;\n")

        file.write("\n/* Variables binarias */\n")
        ls = []
        xs = []
        cs = []
        for a in range(c_asignaturas):
            ls.append(f"l{a + 1}")

            asignatura = asignaturas[a]

            for b in range(7):
                for d in range(5):
                    for s in range(c_salas):
                        if array_validez[a, b, d, s] == 0:
                            continue
                        xs.append(f"x{a + 1}_{b + 1}_{d + 1}_{s + 1}")

                        if asignatura.cantBloques == 2 and b < 6:
                            if array_validez[a, b + 1, d, s] == 0:
                                continue
                            cs.append(f"c{a + 1}_{b + 1}_{d + 1}_{s + 1}")

        file.write("bin ")
        file.write(",".join(ls) + ";\n")

        file.write("bin ")
        file.write(",".join(xs) + ";\n")

        file.write("bin ")
        file.write(",".join(cs) + ";\n")