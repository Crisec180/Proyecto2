# CalculosPilas/CalcularNetoXContrato.py
from CalculosConDICCIONARIOS import CalcularDeduccionNormal
from CalculosConDICCIONARIOS import CalculaOtrasDeducciones

class CalcularNetoXContrato:
    def __init__(self, empleado,deducciones):
        self.empleado = empleado
        self.deducciones = deducciones

    def calcular_neto_por_contrato(self):

        deduccion_normal = CalcularDeduccionNormal.CalcularDeduccionNormal(self.empleado, self.deducciones)
        otras_deducciones = CalculaOtrasDeducciones.CalculaOtrasDeducciones(self.empleado, self.deducciones)

        neto = self.empleado.salario_base - deduccion_normal.calcular_deduccion() - otras_deducciones.calcular_deduccion()
        return neto
