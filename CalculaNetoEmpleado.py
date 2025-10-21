from Empleado import Empleado

class CalculaNetoEmpleado:
    def __init__(self, empleado: Empleado, horas_extras, otras_deducciones):
        self.empleado = empleado
        self.horas_extras = horas_extras
        self.otras_deducciones = otras_deducciones

    def calcular_neto(self):
        salario_base = self.empleado.salario_base
        deducciones = self.empleado.deducciones
        horas_extras = self.empleado.horas_extras

        total_horas_extras = sum(
            hora_extra.valor_hora * hora_extra.horas_extra for hora_extra in horas_extras
        )

        salario_neto = salario_base + total_horas_extras - deducciones
        return salario_neto