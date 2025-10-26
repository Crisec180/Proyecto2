from CalculosConDICCIONARIOS.CalculaBrutoXHora import calculaBrutoXHora
from CalculosConDICCIONARIOS.CalcularDeduccionNormal import calcularDeduccionNormal
import PilasParaCalculos as Pila

BONO_DEPARTAMENTO = {
    "Ingeniería": 0.5,
    "Administración": 0.3,
    "Ventas": 0.4
}

class obtenerNetoXHoras:
    def __init__(self):
        self.pila = Pila.Pila()

    def calcular_y_guardar(self, empleado, horas_trabajadas, tarifa_hora):
        # Validaciones
        if not isinstance(horas_trabajadas, (int, float)) or horas_trabajadas < 0:
            return {"success": False, "detalle": "Horas trabajadas inválidas."}
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            return {"success": False, "detalle": "Tarifa por hora inválida."}

        try:
            bono = BONO_DEPARTAMENTO.get(getattr(empleado, "departamento", ""), 0.0)

            bruto = float(calculaBrutoXHora(empleado, horas_trabajadas, tarifa_hora))
            bruto = round(bruto, 2)

            bruto_bono = round(bruto * (1 + bono), 2)

            deducciones_obj = calcularDeduccionNormal(bruto_bono)
            monto_deducciones = round(float(deducciones_obj.calcular_deducciones()), 2)

            neto = round(bruto_bono - monto_deducciones, 2)

            resultado = {
                "id": getattr(empleado, "id", None),
                "nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "departamento": getattr(empleado, "departamento", ""),
                "horas trabajadas": horas_trabajadas,
                "tarifa hora": tarifa_hora,
                "bono departamento": bono,
                "bruto": bruto,
                "bruto con bono": bruto_bono,
                "deducciones normales": monto_deducciones,
                "neto": neto,
                "proceso": True,
                "detalle": ""
            }

            self.pila.push(resultado)
            return resultado

        except Exception as e:
            return {"success": False, "Detalle": f"Error al calcular... {e}"}

    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()
