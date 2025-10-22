from Empleado import Empleado
from collections import deque
#clases que necesita
from CalculosPILAS import CalcularNetoXContrato
from CalculosPILAS import ObtenerNetoXHoras
from ListaEmpleados import ListaEmpleados

class CalculaNetoEmpleado:
    def __init__(self, lista_empleados, horas_extras, otras_deducciones):
        self.lista_empleados = lista_empleados
        self.horas_extras = horas_extras
        self.otras_deducciones = otras_deducciones
        self.cola = deque()

#COLA PARA GUARDAR LOS RESULTADOS--------------------------------------------------------
    def encolar(self, resultado: dict):
        self.cola.append(resultado)
       
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
    def calcula_neto(self, empleado: Empleado):
        if empleado.tipo_contrato == "Contrato por horas":
            calculo_neto = ObtenerNetoXHoras.ObtenerNetoXHoras(empleado, self.horas_extras, self.otras_deducciones)
            neto = calculo_neto.calcular_neto()
        elif empleado.tipo_contrato == "Contrato mensual":
            calculo_neto = CalcularNetoXContrato.CalcularNetoXContrato(empleado, self.otras_deducciones)
            neto = calculo_neto.calcular_neto()
        else:
            neto = 0
        return neto