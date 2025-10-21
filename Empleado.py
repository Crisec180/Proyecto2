import Persona 

class Empleado(Persona):
    def __init__(self, nombre, edad, cedula, correo, salario, puesto):
        super().__init__(nombre, edad, cedula, correo)
        self.salario = salario
        self.puesto = puesto
        self.horas_extra = 0 

    def __str__(self):
        return f"{super().__str__()}, Salario: {self.salario}, Puesto: {self.puesto}, Horas Extra: {self.horas_extra}"
    
    def agregar_horas_extra(self, horas):
        self.horas_extra += horas

    