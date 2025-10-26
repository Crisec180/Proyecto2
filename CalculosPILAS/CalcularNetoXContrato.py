from CalculosConDICCIONARIOS.CalcularDeduccionNormal import calcularDeduccionNormal
from CalculosConDICCIONARIOS.CalculaOtrasDeducciones import calculaOtrasDeducciones
import PilasParaCalculos as Pila

PORCENTAJE_PAGO = {
    "Semanal": 0.08,
    "Quincenal": 0.12
}

class calcularNetoXContrato:
    def __init__(self):
        self.pila = Pila.Pila()

    def calcular_y_guardar(self, empleado, deduccion_extra=None, tipo_deduccion=None):
        try:
            salario_bruto = float(getattr(empleado, "salario_base", 0.0))
            if salario_bruto < 0:
                return {"success": False, "detalle": "Salario base no puede ser negativo.", "id": getattr(empleado, "id", None)}

            tipo_contrato = getattr(empleado, "tipo_contrato", "")
            porcentaje = PORCENTAJE_PAGO.get(tipo_contrato, 0.0)
            ajuste = round(salario_bruto * porcentaje, 2)

            # Deducciones normales
            deducciones_normales_obj = calcularDeduccionNormal(salario_bruto)
            monto_deducciones_normales = round(float(deducciones_normales_obj.calcular_deducciones()), 2)
            desglose_normales = deducciones_normales_obj.mostrar_deducciones()

            # Deducciones extras
            base_para_extras = round(salario_bruto - ajuste - monto_deducciones_normales, 2)
            deducciones_extras_obj = calculaOtrasDeducciones(base_para_extras, deduccion_extra, tipo_deduccion)
            resultado_extras = deducciones_extras_obj.calcular_deduccion_extra()

            monto_extra = round(float(resultado_extras.get("total", 0.0)), 2) if isinstance(resultado_extras, dict) else round(float(resultado_extras or 0.0), 2)
            desglose_extras = resultado_extras.get("desglose", {}) if isinstance(resultado_extras, dict) else {}

            neto = round(salario_bruto - ajuste - monto_deducciones_normales - monto_extra, 2)

            resultado = {
                "id": getattr(empleado, "id", None),
                "nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "tipo contrato": tipo_contrato,
                "salario bruto": round(salario_bruto, 2),
                "porcentaje periodo": porcentaje,
                "ajuste": ajuste,
                "valor deducciones normales": monto_deducciones_normales,
                "deducciones normales": desglose_normales,
                "otras deducciones": desglose_extras,
                "deducciones extra": deduccion_extra,
                "neto": neto,
                "proceso": bool(resultado_extras.get("success", True)) if isinstance(resultado_extras, dict) else True,
                "detalle": resultado_extras.get("detalle", "") if isinstance(resultado_extras, dict) else ""
            }

            self.pila.push(resultado)
            return resultado

        except Exception as e:
            return {
                "id": getattr(empleado, "id", None),
                "proceso": False,
                "detalle": f"Error al calcular... {e}"
            }

    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()
