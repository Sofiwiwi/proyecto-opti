A la hora de ejecutar el código se deben pasar dos argumentos, los tamaños de las instancias y el número de repeticiones. De esta forma:
```
python3 main.py [Grandes|Medianas|Ambos] <numero de repeticiones por instancia>
```
Se debe tener instalado el programa lp_solve.

El repositorio cuenta con los siguientes archivos:

- clases.py:
Almacena las clases de las salas, los profesores y las asignaturas. Asigna de forma aleatoria los nombres.
- utility.py:
Genera los bloques disponibles en la semana
- generador.py:
Genera listas que contienen los datos de las asignaturas, los profesores y las salas.
La función generar_asignaturas() asigna que el 20% de las asignaturas sean indispensables y el resto dispensables. La restricción adicional es que el 65% de asignaturas tengan 1 bloque y el resto 2.
La función generar_LPSolve() crea archivos que contienen la función objetivo y las restricciones según la instancia.
- main.py:
Crea las instancias, según el tamaño y el número de repeticiones entregados y las resuelve.
- reporte.py:
Se crea un archivo reporte.txt en el cual se especifican las soluciones encontradas.
