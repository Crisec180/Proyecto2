# CalculosPilas/CalcularNetoXContrato.py
from CalculosConDiccionarios import CalcularDeduccionNormal
from CalculosConDiccionarios import CalculaOtrasDeducciones
import PilasParaCalculos as Pila

# Diccionario de porcentajes de deducción según tipo de pago
PORCENTAJE_PAGO = {
    "Semanal": 0.08,
    "Quincenal": 0.12
}

class CalcularNetoXContrato:
    def __init__(self):
        self.pila = Pila.Pila()

    def calcular_y_guardar(self, empleado):
        porcentaje = PORCENTAJE_PAGO.get(empleado.tipo_contrato, 0)
        salario_bruto = float(empleado.salario_base)
        ajuste = salario_bruto * porcentaje
        deducciones_normales = CalcularDeduccionNormal(salario_bruto)
        otras_deducciones = CalculaOtrasDeducciones(salario_bruto - deducciones_normales - ajuste, deduccion_extra, tipo_deduccion)
        neto = salario_bruto - ajuste - deducciones_normales.calcular_deducciones() - otras_deducciones

        resultado = {
            "id": empleado.id,
            "nombre": empleado.nombre,
            "tipo_contrato": empleado.tipo_contrato,
            "salario_bruto": salario_bruto,
            "porcentaje_periodo": porcentaje,
            "ajuste": ajuste,
            "valor_deducciones_normales": deducciones_normales.calcular_deducciones(),
            "deducciones_normales": deducciones_normales.mostrar_deducciones(),
            "otras_deducciones": otras_deducciones.calcular_neto(),
            "deducciones_extra": otras_deducciones.nombre_deduccion(),
            #Deducciones extra se recibe tmb el nombre y tipo 
            "neto": neto
        }
        self.pila.push(resultado)
        return resultado

    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()