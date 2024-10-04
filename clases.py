import random

siglas = ["MAT", "FIS", "QUI", "INF"]
edificios = ["C", "F", "M", "P"]

apellidos = ["Gonzalez", "Rodriguez", "Gomez", "Fernandez", "Lopez", "Diaz", "Martinez", "Perez", "Garcia", "Sanchez"]


class Asignatura:
    def __init__(self, indispensable, CB):
        self.indispensable = indispensable
        self.cantBloques = CB

        if indispensable:
            self.prioridad = random.randint(6, 10)
        else:
            self.prioridad = random.randint(1, 5)

        self.cantEstudiantes = random.randint(40, 80)

        self.sigla = random.choice(siglas) + f"{random.randint(1, 599):03d}"

        self.profesor = Profesor()

    def __str__(self):
        return f"La asignatura {self.sigla} tiene {self.cantEstudiantes} estudiantes, prioridad {self.prioridad} y {self.cantBloques} bloques. Impartida por el profesor {self.profesor.nombre}"


class Sala:
    def __init__(self):
        self.capacidad = random.randint(45, 80)
        self.nombre = random.choice(edificios) + str(random.randint(1, 4)) + f"{random.randint(1, 3)}" + str(
            random.randint(1, 9))

    def __str__(self):
        return f"La sala {self.nombre} tiene una capacidad de {self.capacidad} estudiantes"


class Profesor:
    def __init__(self):
        # For the name choose a random letter and a random surname
        self.nombre = random.choice("ABCDEFGHIJKLMNOPQRSTUVW") + "." + random.choice(apellidos)
        n_bloques_ocupados = random.randint(7, 21)
        bloques = [[i + 1, j + 1] for i in range(7) for j in range(5)]
        bloques_ocupados = random.sample(bloques, n_bloques_ocupados)
        self.bloques = bloques_ocupados

    def __str__(self):
        return f"El profesor {self.nombre} tiene {len(self.bloques)} bloques ocupados: {self.bloques}"

