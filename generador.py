
import random
import numpy as np

# Código generador de instancias
# Conjuntos:
class asignatura():
    def __init__(self,nombre, cant_bloques, indispensable, prioridad, profesor_nombre, tamaño):
        self.nombre = nombre
        self.cant_bloques = cant_bloques
        self.indispensable = indispensable
        self.prioridad = prioridad
        self.profesor = profesor_nombre
        self.tamaño = tamaño

class sala():
    def __init__(self, nombre, tamaño):
        self.ocupada = False
        self.nombre = nombre
        self.tamaño = tamaño
        
    def ocupar(self):
        self.ocupada = True

        
class profesor():
    def __init__(self, nombre, bloques_no_disponibles):
        self.nombre = nombre
        self.bloques_no_disponibles = bloques_no_disponibles


# Funciones:
def generador_asignatura(n_asignaturas):
    
    # Genera una lista de asignaturas y retorna una lista donde cada asignatura contiene: Nombre, cantidad de bloques,
    # indispensabilidad, prioridad y el nombre del profesor.
    
    # Conjunto de asignaturas
    asignaturas = []          
    for i in range(n_asignaturas):
        nombre = "ASIG" + str(i)
        
        # Se asigna los bloques para la asignatura, siendo 2 el máximo
        cant_bloques = random.randint(1, 2)
        
        # Se asigna el 20% (1/5) de las asignaturas como indispensables
        if i % 5 == 0:                 
            indispensable = True
        else:
            indispensable = False
            
        # Se asigna la prioridad a las asignaturas, siendo las indispensables [6,10] y las dispensables [1,5]         
        if indispensable:                        
            prioridad = random.randint(6, 10)    
        else:
            prioridad = random.randint(1, 5)
        
        # Se asgina un profesor a la asignatura, la cantidad de profesores son la misma cantidad de asignaturas    
        profesor_nombre = "PROF" + str(i)
        asignatura_i = [nombre, cant_bloques, indispensable, prioridad, profesor_nombre]
        
        # Se añade a la lista de asignaturas
        asignaturas.append(asignatura_i)
    return asignaturas

# Separador de indispensbles: checkea si la asignatura es indispensable y la separa en su propio array
def separador_de_indispensables(asignaturas):
    
    asignaturas_indispensables = []
    for i in asignaturas:
        if i[2] is True:
            # Si la asignatura es indispensable la añade al array de indispensables
            asignaturas_indispensables.append(i)  
    return asignaturas_indispensables

def separador_de_dispensables(asignaturas):
    
    asignaturas_dispensables = []
    for i in asignaturas:
        if i[2] is False:
            # Si la asignatura es indispensable la añade al array de indispensables
            asignaturas_dispensables.append(i)  
    return asignaturas_dispensables

def num_no_bloques_profes(n_profes): 
    
    # num_no_bloques_profes, randomiza entre 7 a 21 el número de bloques en el que los profesores no van a poder impartir
    # Al final se crea una lista con el profe y la cantidad de bloques en la que no puede impartir del tipo:
    # [['PROF0', 9], ['PROF1', 20], ['PROF2', 19]], en donde PROF0 tiene 9 bloques en los cuales no puede impartir
    
    profesores = []
    for i in range(n_profes):
        prof = "PROF" + str(i)

        # num_no_bloques es el número de bloques en los cuales el profe no puede hacer clases
        num_no_bloques = random.randint(7, 21)
        
        # Se añade a la lista el profesor y la cantidad de bloques en las que no puede
        profe = [prof, num_no_bloques]
        profesores.append(profe)
    return profesores

def randomizar_bloques_no_disponibles(lista_profes_con_bloques_no_disponibles):
    
    # La función randomiza los bloques en los que el profe no puede dentro de la semana incluyendo todos los días de esta
    # al final retorna una lista con el nombre del profesor y los valores de día y bloque, algo así: 
    # ('PROF0', [(1, 4), (5, 7), (4, 5), (1, 3), (4, 1), (2, 1), (3, 4), (5, 2), (5, 3), (2, 4), (3, 6)])
    # En donde cada (1,4), (5,7) representan que para el Lunes en el bloque 4 (7-8) y Viernes en el bloque 7 (13-14) no pueden impartir
    
    dias = 5
    bloques = 7
    profesores_bloques_no_disponibles = []
    
    for profe, num_no_bloques in lista_profes_con_bloques_no_disponibles:
        # Bloques por semana (Deberían ser 35)
        bloques_semana = [(dia, bloque)for dia in range(1, dias + 1) for bloque in range(1, bloques + 1)]
    
        # Se randomiza
        bloques_no_disponibles = random.sample(bloques_semana, num_no_bloques)
        
        # Se añade a la lista dependiendo del profe y sus bloques no disponibles
        profesores_bloques_no_disponibles.append((profe, bloques_no_disponibles))
        
    return profesores_bloques_no_disponibles
        
        
# Generación Función Objetivo:
def funcion_objetivo(asignaturas):
    # Genera la función objetivo de la forma: max: l0 * PRa1 .... + ln * PRan;
    fo = "max: "
    for i in asignaturas:
        nombre = i[0]
        prioridad = i[3]
        fo += f"l{i} * {prioridad} + "
    return fo.rstrip('+') + ';'
        
        
# Generación restricciones:



# Generación lp_solve:
def generar_lp(asignaturas, profesores):
    