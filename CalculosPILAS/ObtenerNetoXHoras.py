from CalculosConDICCIONARIOS import CalculaBrutoXHora
from CalculosConDICCIONARIOS import CalcularDeduccionNormal

class ObtenerNetoXHoras:
    def __init__(self, empleado, horas_trabajadas, valor_hora):
        self.horas_trabajadas = horas_trabajadas
        self.valor_hora = valor_hora

    #segun estiquetas de la parte grafica es un valor o otro
    #ejemplo si es Ingenieria le supa 0.5 
    #ventas 0.2 y  administracion 0.3
    def calcular_neto(self, empleado):
        if "Ingenieria":
            ""