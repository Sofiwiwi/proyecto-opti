import re

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]


def generar_reporte(out_file, asignaturas, salas):
    with open(out_file, "r") as out:
        with open(f"reporte.txt", "a") as reporte:
            text = out.read()

            reporte.write(f"REPORTE ({out_file})\n\n")

            count_indispensables = 0

            for asignatura in asignaturas:
                if asignatura.indispensable:
                    count_indispensables += 1

            reporte.write(f"TOTAL SALAS: {len(salas)}\n")
            reporte.write(f"TOTAL ASIGNATURAS: {len(asignaturas)}\n")
            reporte.write(f"ASIGNATURAS INDISPENSABLES: {count_indispensables}\n\n")

            if "infeasible" in text:
                reporte.write("No se encontro solucion.")
                reporte.write("\n" + "-" * 30 + "\n")
                return

            reporte.write("ASIGNACIONES:\n\n")

            pattern_x = re.compile(r"x(\d+)_(\d+)_(\d+)_(\d+).+1")

            count_indispensables_asignadas = 0

            asignaciones = pattern_x.findall(text)

            print(f"{"ASIGNATURA":^12}|{"CBA":^5}|{"BLOQUE":^8}|{"DIA":^12}|{"SALA":^12}|{"C":^3}|{"sC":^3}|{"tupC":^12}|{"l":^3}")
            for asignacion in asignaciones:
                pattern_c = rf"c{asignacion[0]}_{asignacion[1]}_{asignacion[2]}_{asignacion[3]}.+(\d)"
                pattern_c = re.compile(pattern_c)

                pattern_sC = rf"c{asignacion[0]}_(\d)_(\d)_(\d).+(\d)"
                pattern_sC = re.compile(pattern_sC)

                c = "-"

                asignatura = asignaturas[int(asignacion[0]) - 1]
                tup = "-"
                s = "-"

                if asignatura.cantBloques == 2 and asignacion[1] != "7":
                    c = pattern_c.findall(text)[0]
                    sC = pattern_sC.findall(text)

                    s = 0


                    for tup_c in sC:
                        if int(tup_c[3]) == 1:
                            if s == 0:
                                tup = f"({tup_c[0]},{tup_c[1]},{tup_c[2]})"
                            s += 1
                else:
                    sC = "-"

                pattern_l = rf"l{asignacion[0]}.+(\d)"
                l = re.compile(pattern_l).findall(text)[0]

                print(f"{asignacion[0]:^12}|"
                      f"{asignatura.cantBloques:^5}|"
                      f"{asignacion[1]:^8}|"
                      f"{asignacion[2]:^12}|"
                      f"{asignacion[3]:^12}|"
                      f"{c:^3}|"
                      f"{s:^3}|"
                      f"{tup:^12}|"
                      f"{l:^3}")

            CBA2_asignados = []

            for asignacion in asignaciones:
                sala = salas[int(asignacion[3]) - 1]
                asignatura = asignaturas[int(asignacion[0]) - 1]

                if asignatura in CBA2_asignados:
                    continue

                if asignatura.indispensable:
                    count_indispensables_asignadas += 1

                if asignatura.cantBloques == 2:
                    CBA2_asignados.append(asignatura)

                reporte.write(f"La asignatura {asignatura.sigla} ({asignatura.indispensable}) "
                              f"se asigno a la sala {sala.nombre} "
                              f"el dia {dias[int(asignacion[2]) - 1]} "
                              f"en el bloque {asignacion[1]}.\n")

            reporte.write(f"\nASIGNATURAS INDISPENSABLES ASIGNADAS: {count_indispensables_asignadas} "
                          f"({count_indispensables_asignadas / count_indispensables * 100:.2f}%)\n")

            reporte.write("\n" + "-" * 30 + "\n")
