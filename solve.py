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
    os.system(f"lp_solve -timeout {timeout} -t instancias/{filename} > resultados/{filename.replace('.lp', '.txt')}")
    time_f = time.time() - time_0
    print(f"Instance solved in {time_f} seconds")

