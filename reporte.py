import re
import os
import numpy as np
import pandas as pd

dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

def print_horario(horario):
    print("Horario")
    l_head = 16
    l_x = 5
    l_y = 7
    print("-"*(l_head*l_x + l_x+1))
    for dia in dias:
        print("|",end="")
        print(f"{dia:^16}",end="")
    print("|", end="\n")
    print("-"*(l_head*l_x + l_x+1)) 
    for bloque in horario:
        # print(bloque)
        filas = []
        max_asig = 0

        for dia in bloque:
            if max_asig < len(dia):
                max_asig = len(dia)

        if max_asig == 0:
            max_asig = 1

        filas = [[f"{' ':<16}" for _ in range(len(bloque))] for _ in range(max_asig)]

        for d, dia in enumerate(bloque):                            
            for i, asignacion in enumerate(dia):
                filas[i][d] = f" {asignacion:<15}"

        
        for fila in filas:
            print("|" + "|".join(fila), end="|\n")

        print("-"*(l_head*l_x + l_x+1))


def generar_reporte(out_file):
    df = pd.read_csv("reporte.csv", header=0)

    with open(out_file, "r") as out:
        text = out.read()

        instancia = out_file.split("/")[-1].replace(".txt", "")

        if "infactible" in text:
            # Set infactible to 1 in the csv
            df.loc[df["instancia"] == instancia, "infactible"] = 1
            df.loc[df["instancia"] == instancia, "tiempo"] = text.split()[0]
            # Save the csv
            df.to_csv("reporte.csv", index=False)
            return

        if "timeout" in text:
            # Set infactible to 1 in the csv
            df.loc[df["instancia"] == instancia, "infactible"] = 2
            df.loc[df["instancia"] == instancia, "tiempo"] = -1
            # Save the csv
            df.to_csv("reporte.csv", index=False)
            return

        pattern_l = re.compile(r"l(\d+)\s+(\d+)")

        ls = re.findall(pattern_l, text)
       

        total_asignaturas = len(ls)
        asignaturas_asignadas = sum([int(l[1]) for l in ls])
        df.loc[df["instancia"] == instancia, "asignadas"] = asignaturas_asignadas
        df.loc[df["instancia"] == instancia, "tiempo"] = float(text.split()[0])

        pattern_x = re.compile(r"x(\d+)_(\d+)_(\d+)_(\d+)\s+(\d+)")
        xs = re.findall(pattern_x, text)

        horario = [[[] for _ in range(5)] for _ in range(7)]
   
        for x in xs:
            s = f"A: {x[0]}, S: {x[3]}"
            horario[int(x[1])-1][int(x[2])-1].append(s)

        print_horario(horario)
        df.to_csv("reporte.csv", index=False)

for file in os.listdir("resultados_clean"):
    generar_reporte(f"resultados_clean/{file}")
