
import random
import numpy as np

# Código generador de instancias

# Conjuntos:
# Asignaturas: [Nombre, cantidad de bloques, indispensabilidad, prioridad, nombre del profesor]
# Profesores: [Nombre, cantidad de bloques en los que no puede hacer clases]
# Salas: [Nombre]
# Bloques: [1, 2, 3, 4, 5, 6, 7]
# Días: [1, 2, 3, 4, 5]

# Variables: [x{Nombre de la asignatura}, {Bloque}, {Día}, {Sala}, {Profesor}]
# Variables: [l{a} es la variable que representa si la asignatura a se asigna o no]

# Parametros: [P{a,b,d} disponibilidad del profesro, [0,1]]
# Parametros: PR{a} es la prioridad de la asignatura a

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

# Generador de salas

def generador_de_salas(n_salas):
    salas = []
    for i in range(n_salas):
        sala = "SALA" + str(i)
        salas.append(sala)
    return salas


# Separador de indispensbles: checkea si la asignatura es indispensable y la separa en su propio array
def separador_de_indispensables(asignaturas):
    # Se abre un array de asignaturas indispensables
    asignaturas_indispensables = []
    for i in asignaturas:
        if i[2] is True:
            # Si la asignatura es indispensable la añade al array de indispensables
            asignaturas_indispensables.append(i)
    return asignaturas_indispensables


# Separador de asignaturas dispensables:  checkea si la asignatura es dispensable y la separa en su propio array
def separador_de_dispensables(asignaturas):
    # Se abre un array de asignaturas dispensables
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
    # al final retorna una lista con el nombre del profesor y los valores de bloque y día, algo así: 
    # ('PROF0', [(4, 1), (7, 5), (5, 4), (3, 1), (1, 4), (1, 2), (4, 3), (2, 5), (3, 5), (4, 2), (6, 3)])
    # En donde cada (4,1), (7,5) representan que para el bloque 4 (7-8) del día Lunes y que para el bloque 7 (13-14) del día Viernes no pueden impartir
    
    dias = 5
    bloques = 7
    profesores_bloques_no_disponibles = []
    
    for profe, num_no_bloques in lista_profes_con_bloques_no_disponibles:
        # Bloques por semana (Deberían ser 35)
        bloques_semana = [(bloque, dia) for bloque in range(1, bloques + 1) for dia in range(1, dias + 1)]
    
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
        prioridad = i[3]
        fo += f"l{i} * {prioridad} + "
    return fo.rstrip('+') + ';'
                
# Generación restricciones:

# 1) Todas las asignaturas indispensables deben ser asignadas

def rest1(asignaturas, asignaturas_indispensables):
    res = ''
    for i in asignaturas:
        if i[2] is True:
            res += f"l{i[0]} + "
    return res.rstrip('+') + " = " + len(asignaturas_indispensables) + ';'

# 2) Los profesores tienen bloques en donde no pueden enseñar.

def rest2(asignaturas, profesores, profesores_bloques_no_disponibles):
    restriccion = ""


# 3.1) Si la asignatura necesita dos bloques estos deben ser seguidos y en la misma sala y el mismo profesor
def rest3_1(asignaturas, salas):
    restriccion = ""
    bloque = [1,2,3,4,5,6]
    dia = [1, 2, 3, 4, 5]
    for a in asignaturas: 
        for r in salas:
            nombre = a[0]
            p = a[4] # p s Profesor
            if a[1] == 2:
                for d in dia:
                    for b in bloque:
                        restriccion += f"x{nombre},{b},{d},{r},{p} + x{nombre},{b+1},{r}.{p} = 2; \n"
    return restriccion

# 3.1.1) Limitar a dos bloques por semana
def rest3_1_1(asignaturas, salas):
    restriccion = ""
    dias = [1,2,3,4,5]
    for a in asignaturas:
        p = a[4]
        for r in salas:
            nombre = a[0]
            if a[1] == 2:
                for d in dias:
                    restriccion += f"x{nombre},1,{d},{r},{p} + x{nombre},2,{d},{r},{p} + x{nombre},3,{d},{r},{p} + "
                    restriccion += f"x{nombre},4,{d},{r},{p} + x{nombre},6,{d},{r},{p} + x{nombre},7,{d},{r},{p} <= 2; \n"
    return restriccion
            
# 4) En una sala solo se imparte una asignatura:
def rest4(asignaturas, salas):
    restriccion = ""
    bloques = [1, 2, 3, 4, 5, 6, 7]  
    dias = [1, 2, 3, 4, 5]
    for r in salas:
        for d in dias:  
            for b in bloques:
                # Restricción para que en el bloque b de la sala r en el día d solo haya una asignatura
                restriccion += " + ".join([f"x{a[0]},{b},{d},{r},{a[4]}" for a in asignaturas])
                restriccion += " <= 1; \n"
    return restriccion


# Generación lp_solve:
def generar_lp(asignaturas, profesores, salas):
    
    # Se entrega una lista con las asignaturas indispensables
    asignaturas_indispensables = separador_de_indispensables(asignaturas)
    
    # Entrega la lista de los bloques y días en los cuales los profes no pueden
    lista_profes_no_disponible = randomizar_bloques_no_disponibles(num_no_bloques_profes(profesores))
    
    
  