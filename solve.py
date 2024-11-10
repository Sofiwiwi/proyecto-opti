import os
import time

if os.sys.argv[1]:
    timeout = os.sys.argv[1]
else:
    timeout = 1100


# loop through files inside the directory "instancias"
for filename in os.listdir("instancias"):
    if not filename.endswith(".lp"):
        continue

    print(f"Solving instance {filename}...")
    # Start timer here
    time_0 = time.time()
    os.system(f"lp_solve -presolve -presolveb -presolvec -B3 -Bc -Bo -s2 -gr 0.05 -f -timeout {timeout} -i -v3 -S2 instancias/{filename} > resultados/{filename.replace('.lp', '.txt')}")
    time_f = time.time() - time_0
    print(f"Instance solved in {time_f} seconds")

    with open(f"resultados/{filename.replace('.lp', '.txt')}", "r") as file:
        text = file.read()

    with open(f"resultados/{filename.replace('.lp', '.txt')}", "w") as file:
        print(time_f)
        file.write(f"{float(time_f):.2f}\n")
        file.write(text)
