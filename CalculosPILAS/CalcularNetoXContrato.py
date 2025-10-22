# CalculosPilas/CalcularNetoXContrato.py
from CalculosConDICCIONARIOS import CalcularDeduccionNormal
from CalculosConDICCIONARIOS import CalculaOtrasDeducciones

class CalcularNetoXContrato:
    def __init__(self, bruto, deducciones):
        self.bruto = bruto
        self.deducciones = deducciones

    def calcular_neto(self):
        return self.bruto - self.deducciones