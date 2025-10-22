# CalculosPilas/CalcularNetoXContrato.py
from CalculosConDICCIONARIOS import CalcularDeduccionNormal
from CalculosConDICCIONARIOS import CalculaOtrasDeducciones

class CalcularNetoXContrato:
    def __init__(self, empleado,deducciones):
        self.empleado = empleado
        self.deducciones = deducciones

    def calcular_neto(self):
       bruto = self.empleado.salario_bruto()
       CalcularDeduccionNormal = CalcularDeduccionNormal.CalculoDeDeducciones(bruto)
       deduccion_normal = CalcularDeduccionNormal.calcular_deducciones()
       CalcularOtrasDeducciones = CalculaOtrasDeducciones.CalculoDeOtrasDeducciones(bruto)
       otras_deducciones = CalcularOtrasDeducciones.calcular_otras_deducciones()
       return bruto - deduccion_normal - otras_deducciones