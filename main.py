import argparse
from generador import generar_LPSolve, generar_asignaturas, generar_salas
import random
import os
from reporte import generar_reporte


def main(arg_tamanos, rep):
    cantidad_asignaturas = {
        "Medianas": [
            [40, 45],
            [54, 58],
            [68, 72],
            [80, 85],
            [95, 99]
        ],
        "Grandes": [
            [180, 200],
            [210, 230],
            [250, 270],
            [300, 320],
            [340, 360]
        ]
    }

    cantidad_salas = {
        "Medianas": [
            [3, 3],
            [4, 4],
            [5, 5],
            [6, 6],
            [7, 7]
        ],
        "Grandes": [
            [9, 11],
            [12, 14],
            [15, 17],
            [18, 20],
            [21, 23]
        ]
    }

    tamanos = []

    if arg_tamanos == "Ambos":
        tamanos = ["Medianas", "Grandes"]
    elif arg_tamanos == "Medianas":
        tamanos = ["Medianas"]
    elif arg_tamanos == "Grandes":
        tamanos = ["Grandes"]

    print("Generando instancias...\n")

    for filename in os.listdir("instancias"):
        os.system(f"rm instancias/{filename}")

    for filename in os.listdir("resultados"):
        os.system(f"rm resultados/{filename}")

    if os.path.exists("reporte.txt"):
        os.system(f"rm reporte.txt")

    for t in range(len(tamanos)):
        tamano = tamanos[t]
        for index in range(5):
            for r in range(rep):
                c_asignaturas = random.randint(cantidad_asignaturas[tamano][index][0],
                                               cantidad_asignaturas[tamano][index][1])
                c_salas = random.randint(cantidad_salas[tamano][index][0],
                                         cantidad_salas[tamano][index][1])

                lp_file = f"instancias/{tamano}_{index + 1}_{r + 1}.lp"
                print(
                    f"{5 * rep * t + rep * index + (r + 1)}: "
                    f"Generando instancia numero de {c_asignaturas} asignaturas y {c_salas} salas "
                    f"en el archivo {lp_file}..."
                )

                asignaturas = generar_asignaturas(c_asignaturas)
                salas = generar_salas(c_salas)

                generar_LPSolve(asignaturas, salas, lp_file)
                out_file = lp_file.replace('.lp', '.txt').replace('instancias', 'resultados')
                os.system(f"lp_solve {lp_file} > {out_file}")

                generar_reporte(out_file, asignaturas, salas)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar y resolver instancias de asignaturas y salas.")
    parser.add_argument("tamano", choices=["Medianas", "Grandes", "Ambos"],
                        help="El tamaño de las asignaturas y salas (Medianas, Grandes o Ambos).")
    parser.add_argument("rep", type=int, help="La cantidad de instancias a generar y resolver por cada caso.")
    args = parser.parse_args()

    print(f"Generando y resolviendo {args.rep} caso por instancia de {args.tamano} tamaños.")

    main(args.tamano, args.rep)
