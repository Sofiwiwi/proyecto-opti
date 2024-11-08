import os
import re

def clean_instances(file_name):
    with open(f"resultados/{file_name}", "r") as file:
        lines = file.readlines()

    with open(f"resultados_clean/{file_name}", "w") as file:
        if len(lines) == 0:
            file.write("no ejecutado\n")
            return
        if lines[0].startswith("This problem is infeasible"):
            file.write("infactible\n")
            return

        if lines[0].startswith("Timeout"):
            file.write("infactible\n")
            return


        var_values = False
        pattern = re.compile(r"(\w+)\s+(\d+)")

        for line in lines:
            line = line.strip()
            
            if var_values:
                # Get the two values of the pattern
                match = pattern.match(line)
                if match:
                    var_name = match.group(1)
                    var_value = match.group(2)
                    if int(var_value) == 0:
                        continue
                    file.write(f"{var_name} {var_value}\n")
                continue

            if line.startswith("Value of objective"):
                line = line.replace("Value of objective function: ", "")
                file.write(line + "\n")
                continue
                
            if line.startswith("Actual values of the variables:"):
                var_values = True
                continue


def main():
    for file_name in os.listdir("resultados"):
        clean_instances(file_name)
        

main()
