from CalculosConDICCIONARIOS import CalculaBrutoXHora
from CalculosConDICCIONARIOS import CalcularDeduccionNormal

class ObtenerNetoXHoras:
    def __init__(self, horas_trabajadas, valor_hora):
        self.horas_trabajadas = horas_trabajadas
        self.valor_hora = valor_hora

    def calcular_neto(self):
        return self.horas_trabajadas * self.valor_hora