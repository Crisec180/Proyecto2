from Empleado import Empleado
from collections import deque
#clases que necesita
from CalculosPILAS import CalcularNetoXContrato
from CalculosPILAS import ObtenerNetoXHoras
from ListaEmpleados import ListaEmpleados

class CalculaNetoEmpleado:
    def __init__(self, lista_empleados: ListaEmpleados, horas_extras, otras_deducciones):
        self.lista_empleados = lista_empleados
        self.horas_extras = horas_extras
        self.otras_deducciones = otras_deducciones

#COLA PARA GUARDAR LOS RESULTADOS--------------------------------------------------------
    def __init__(self):
        self.cola=deque()

    def encolar(self, cheque):
        self.cola.append(cheque)

    def desencolar(self):
        if not self.esta_vacia():
            return self.cola.popleft()
        return None
    
    def esta_vacia(self):
        cant = 0
        for _ in self.cola:
            cant += 1
        return cant == 0

#-----------------------------------------------------------------------------------------
    def calcular_neto(self):
        total_neto = 0
        for empleado in self.lista_empleados.obtener_empleados():
            if hasattr(empleado, 'contrato'):
                calculo = CalcularNetoXContrato(empleado, self.otras_deducciones)
            elif hasattr(empleado, 'horas_trabajadas'):
                calculo = ObtenerNetoXHoras(empleado, self.horas_extras, self.otras_deducciones)
            else:
                continue
            neto = calculo.calcular_neto()
            total_neto += neto
    
    def cola_neto(self, empleado: Empleado):
        cola = deque()
        salario_neto = self.calcular_neto()
        cola.append({
            "nombre": empleado.nombre,
            "apellido": empleado.apellido,
            "salario_neto": salario_neto
        })
        return cola