#La clase que recibe todo los datos de chequeo y empleados
class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def obtener_empleados(self):
        return self.empleados
    
    def Horas_trabajadas_por_empleado(self, empleado_id):
        for emp in self.empleados:
            if emp.id == empleado_id:
                return emp.calcular_horas_trabajadas()
        return 0
    
    