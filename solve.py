import os
import time
import subprocess





# Obtener el valor del timeout desde los argumentos o usar un valor por defecto
if len(os.sys.argv) > 1:
    timeout = float(os.sys.argv[1])
else:
    timeout = 1100

# Loop para recorrer archivos dentro del directorio "instancias"
for filename in os.listdir("instancias"):
    if not filename.endswith(".lp"):
        continue

    print(f"Resolviendo instancia {filename}...")

    # Inicio del temporizador
    time_0 = time.time()

    # Ejecutar el comando lp_solve
    os.system(f"lp_solve -timeout {timeout} instancias/{filename} > resultados/{filename.replace('.lp', '.txt')}")

    # Calcular el tiempo de ejecución
    time_f = time.time() - time_0
    print(f"Instancia resuelta en {time_f:.2f} segundos")

    # Leer el contenido del archivo de resultados
    result_file_path = f"resultados/{filename.replace('.lp', '.txt')}"
    with open(result_file_path, "r") as file:
        text = file.read()

    # Sobrescribir el archivo de resultados solo con el tiempo al principio
    with open(result_file_path, "r") as file:
        line_count = len(file.readlines())
        with open(result_file_path, "w") as file:
            file.write(f"{time_f:.2f} {line_count-4}")
            file.write(text)
