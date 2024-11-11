import os
import time
import subprocess





# Obtener el valor del timeout desde los argumentos o usar un valor por defecto
if len(os.sys.argv) > 1:
    timeout = float(os.sys.argv[1])
else:
    timeout = 1100


# loop through files inside the directory "instancias"
for filename in os.listdir("instancias"):
    if not filename.endswith(".lp"):
        continue

    print(f"Solving instance {filename}...")
    # Start timer here
    time_0 = time.time()
    os.system(f"lp_solve -presolve -presolveb -presolvec -B3 -Bc -Bo -s2 -gr 0.05 -f -timeout {timeout} instancias/{filename} > resultados/{filename.replace('.lp', '.txt')}")
    time_f = time.time() - time_0
    print(f"Instance solved in {time_f} seconds")

    # Leer el contenido del archivo de resultados
    result_file_path = f"resultados/{filename.replace('.lp', '.txt')}"
    with open(result_file_path, "r") as file:
        text = file.read()

    # Sobrescribir el archivo de resultados solo con el tiempo al principio
    with open(result_file_path, "r") as file:
        line_count = len(file.readlines())
        with open(result_file_path, "w") as file:
            file.write(f"{time_f:.2f} {line_count-4}\n")
            file.write(text)
