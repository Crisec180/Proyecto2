from CalculosConDiccionarios.CalcularDeduccionNormal import calculoDeDeducciones
from CalculosConDiccionarios.CalculaOtrasDeducciones import calculoDeDeduccionesExtras
from CalculosConDiccionarios.CalculaBrutoXHora import calculoDeSalarioBruto
from CalculosPILAS.PilasParaCalculos import pila

PORCENTAJE_PAGO = {
    "Semanal": 0.08,
    "Quincenal": 0.12
}

class calcularNetoXContrato:
    def __init__(self):
        self.pila = pila()


    def calcular_y_guardar(self, empleado, deduccion_extra=None, tipo_deduccion=None, horas_trabajadas=None):
        try:
            if empleado is None:
                return {"success": False, "detalle": "Empleado no válido", "id": None}

            try:
                salario_bruto = float(empleado.salario_base)
                if salario_bruto < 0:
                    return {"success": False, "detalle": "Salario base no puede ser negativo", "id": empleado.id}
            except (ValueError, AttributeError):
                return {"success": False, "detalle": "Salario base no válido", "id": getattr(empleado, "id", None)}

            # Validar y obtener tipo de contrato
            tipo_contrato = getattr(empleado, "tipo_contrato", "")

            if tipo_contrato not in PORCENTAJE_PAGO:
                return {"success": False, "detalle": f"Tipo de contrato no válido: {tipo_contrato}", "id": getattr(empleado, "id", None)}

            # Determinar si tenemos una tarifa por hora real o solo un salario por periodo
            tarifa = None
            tarifa_es_horaria = False
            try:
                raw_tarifa = getattr(empleado, 'tarifa_hora', None)
                if raw_tarifa is not None:
                    tarifa_tmp = float(raw_tarifa)
                    if tarifa_tmp > 0:
                        tarifa = tarifa_tmp
                        tarifa_es_horaria = True
            except (TypeError, ValueError):
                tarifa = None

            # Si no hay tarifa horaria válida, usamos salario_base COMO SALARIO (no como tarifa horaria)
            if tarifa is None:
                try:
                    salario_base_val = float(getattr(empleado, 'salario_base', 0.0))
                except (TypeError, ValueError):
                    return {"success": False, "detalle": "Salario base no válido", "id": getattr(empleado, "id", None)}
                tarifa = salario_base_val
                tarifa_es_horaria = False

            # Calcular salario bruto: si se pasan horas_trabajadas las usamos,
            # si no, usamos el período según tipo de contrato (Semanal/Quincenal)
            if horas_trabajadas is not None:
                try:
                    horas_val = float(horas_trabajadas)
                except (TypeError, ValueError):
                    return {"success": False, "detalle": "Horas trabajadas inválidas", "id": getattr(empleado, "id", None)}
                if horas_val <= 0:
                    return {"success": False, "detalle": "Horas trabajadas debe ser mayor que 0", "id": getattr(empleado, "id", None)}
                horas_periodo = horas_val
                if tarifa_es_horaria:
                    salario_bruto = round(tarifa * horas_periodo, 2)
                else:
                    # No tenemos tarifa horaria; interpretar salario_base como salario por periodo
                    # Ignoramos las horas y usamos tarifa (salario_base) directamente
                    salario_bruto = round(tarifa, 2)
            else:
                if tipo_contrato == "Quincenal":
                    horas_periodo = 80  # 8h * 10 días
                    salario_bruto = round(tarifa * horas_periodo, 2) if tarifa_es_horaria else round(tarifa, 2)
                elif tipo_contrato == "Semanal":
                    horas_periodo = 40  # 8h * 5 días
                    salario_bruto = round(tarifa * horas_periodo, 2) if tarifa_es_horaria else round(tarifa, 2)
                else:
                    # Por defecto usar salario_base tal cual
                    horas_periodo = None
                    salario_bruto = float(getattr(empleado, 'salario_base', 0.0))

            # DEBUG: información intermedia para entender valores
            try:
                print(f"Debug - tipo_contrato: {tipo_contrato}")
                print(f"Debug - raw_tarifa (empleado.tarifa_hora): {getattr(empleado, 'tarifa_hora', None)}")
                print(f"Debug - tarifa_es_horaria: {tarifa_es_horaria}")
                print(f"Debug - tarifa usada para cálculo: {tarifa}")
                print(f"Debug - salario_bruto antes de ajuste: {salario_bruto}")
                print(f"Debug - horas_periodo: {horas_periodo}")
            except Exception:
                pass

            # Calcular porcentaje de pago (bono) según tipo
            porcentaje = PORCENTAJE_PAGO[tipo_contrato]

            # El ajuste se suma al salario bruto
            ajuste = round(salario_bruto * porcentaje, 2)
            print(f"Debug - Ajuste calculado: {ajuste}")  # Debug

            # El salario ajustado es el bruto más el ajuste
            salario_ajustado = round(salario_bruto + ajuste, 2)
            print(f"Debug - Salario ajustado (bruto + ajuste): {salario_ajustado}")  # Debug

            # Deducciones normales sobre el salario ajustado
            deducciones_normales_obj = calculoDeDeducciones(salario_ajustado)
            resultado_deducciones = deducciones_normales_obj.calcular_deducciones()
            monto_deducciones_normales = round(float(resultado_deducciones.get("Total", 0.0)), 2)
            desglose_normales = resultado_deducciones.get("Desglose", {})
            
            # Deducciones extras
            if deduccion_extra and tipo_deduccion:
                deducciones_extras_obj = calculoDeDeduccionesExtras(salario_ajustado, deduccion_extra, tipo_deduccion)
                resultado_extras = deducciones_extras_obj.calcular_deduccion_extra()
                monto_extra = round(float(resultado_extras.get("Total", 0.0)), 2) if isinstance(resultado_extras, dict) else round(float(resultado_extras or 0.0), 2)
                desglose_extras = resultado_extras.get("Desglose", {}) if isinstance(resultado_extras, dict) else {}
            else:
                monto_extra = 0
                desglose_extras = {}

            # El neto es: salario bruto + ajuste - deducciones
            neto = round(salario_bruto + ajuste - monto_deducciones_normales - monto_extra, 2)

            resultado = {
                "id": empleado.id,
                "nombre": f"{empleado.nombre} {empleado.apellido}".strip(),
                "tipo_contrato": tipo_contrato,
                "calculo": {
                    "salario_bruto": round(salario_bruto, 2),
                    "porcentaje_ajuste": porcentaje,
                    "monto_ajuste": ajuste,
                    "salario_ajustado": salario_ajustado
                },
                "deducciones": {
                    "normales": desglose_normales,
                    "total_normales": monto_deducciones_normales,
                    "extras": desglose_extras,
                    "total_extras": monto_extra
                },
                "neto": neto,
                "proceso": True,
                "detalle": "Cálculo realizado exitosamente"
            }
            #APILA EL RESULTADO------------------------------------------------------
            self.pila.push(resultado)
            return resultado

        except Exception as e:
            return {
                "id": getattr(empleado, "id", None),
                "proceso": False,
                "detalle": f"Error al calcular... {e}"
            }

    #MAS PILA-------------------------------------------------------------
    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()