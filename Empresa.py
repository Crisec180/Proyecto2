#La clase que recibe todo los datos de chequeo y empleados
from CalculoConCOLAS import CalculaNetoEmpleado
from ListaEmpleados import ListaEmpleados
class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

    def guardar_registros_CSV(self, archivo):
        print("guardar")

    def calcular_neto_empleados(self, lista_empleados, horas_extras, otras_deducciones):
        calculadora = CalculaNetoEmpleado.CalculaNetoEmpleado(lista_empleados, horas_extras, otras_deducciones)
        for empleado in lista_empleados:
            neto = calculadora.calcula_neto(empleado)
            print(f"El salario neto de {empleado.nombre} es: {neto}")

