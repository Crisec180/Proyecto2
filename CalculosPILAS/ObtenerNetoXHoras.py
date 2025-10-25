from CalculosConDICCIONARIOS import CalculaBrutoXHora
from CalculosConDICCIONARIOS import CalcularDeduccionNormal
import PilasParaCalculos as Pila

# Diccionario de bonos por departamento
BONO_DEPARTAMENTO = {
    "Ingeniería": 0.5,
    "Administración": 0.3,
    "Ventas": 0.4
}

class ObtenerNetoXHoras:
   def __init__(self):
        self.pila = Pila.Pila()

def calcular_y_guardar(self, empleado, horas_trabajadas, tarifa_hora, deducciones_extra=0):
    bono = BONO_DEPARTAMENTO.get(empleado.departamento, 0)
    bruto = CalculaBrutoXHora(empleado, horas_trabajadas, tarifa_hora)
    bruto_bono = bruto * (1 + bono)
    deducciones_normales = CalcularDeduccionNormal(empleado, bruto_bono)
    neto = bruto_bono - deducciones_normales - deducciones_extra

    resultado = {
        "id": empleado.id,
        "nombre": empleado.nombre,
        "departamento": empleado.departamento,
        "horas_trabajadas": horas_trabajadas,
        "tarifa_hora": tarifa_hora,
        "bono_departamento": bono,
        "bruto": bruto,
        "bruto_con_bono": bruto_bono,
        "deducciones_normales": deducciones_normales,
        "deducciones_extra": deducciones_extra,
        "neto": neto
    }
    self.pila.push(resultado)
    return resultado

def procesar(self):
    return self.pila.pop()

def mostrar_pila(self):
    self.pila.mostrar()