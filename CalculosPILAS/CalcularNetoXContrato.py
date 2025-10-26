from CalculosConDICCIONARIOS import CalcularDeduccionNormal
from CalculosConDICCIONARIOS import CalculaOtrasDeducciones

PORCENTAJE_PAGO = {
    "Semanal": 0.08,
    "Quincenal": 0.12
}

class CalcularNetoXContrato:
    def __init__(self):
        self.pila = Pila.Pila()

    def calcular_y_guardar(self, empleado, deduccion_extra, tipo_deduccion):
        try:
            salario_bruto = float(getattr(empleado, "salario_base", 0.0))
            if salario_bruto < 0:
                raise ValueError("Salario base no puede ser negativo.")

            porcentaje = PORCENTAJE_PAGO.get(getattr(empleado, "tipo_contrato", ""), 0.0)
            ajuste = round(salario_bruto * porcentaje, 2)

            # Deduccion normal
            deducciones_normales_obj = CalcularDeduccionNormal(salario_bruto)
            deducciones_normales = round(deducciones_normales_obj.calcular_deducciones(), 2)
            desglose_normales = deducciones_normales_obj.mostrar_deducciones()

            # Extras
            base_para_extras = salario_bruto - ajuste - deducciones_normales
            deducciones_extras_obj = CalculaOtrasDeducciones(base_para_extras, deduccion_extra, tipo_deduccion)
            resultado_extras = deducciones_extras_obj.calcular_deduccion_extra()
            monto_extra = round(resultado_extras.get("total", 0.0), 2)

            neto = round(salario_bruto - ajuste - deducciones_normales - monto_extra, 2)

            resultado = {
                "Id": getattr(empleado, "id", None),
                "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "Tipo contrato": getattr(empleado, "tipo_contrato", ""),
                "Salario bruto": round(salario_bruto, 2),
                "Porcentaje periodo": porcentaje,
                "Ajuste": ajuste,
                "Valor deducciones normales": deducciones_normales,
                "Deducciones normales": desglose_normales,
                "Otras deducciones": resultado_extras.get("desglose", {}),
                "Deducciones extra": deduccion_extra,
                "Neto": neto,
                "Proceso": resultado_extras.get("Proceso", True),
                "Detalle": resultado_extras.get("detalle", "")
            }

            self.pila.push(resultado)
            return resultado

        except Exception as e:
            return print(f"Error al calcular... {e}")

    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()
