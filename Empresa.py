#La clase que recibe todo los datos de chequeo y empleados
class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

    def guardar_registros_CSV(self, archivo):
        print("guardar")