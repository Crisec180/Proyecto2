from collections import deque
from CalculosPILAS.CalcularNetoXContrato import calcularNetoXContrato
from CalculosPILAS.ObtenerNetoXHoras import obtenerNetoXHoras
class calculaNetoEmpleado:
    def __init__(self, empleados, horas_extras, tipo_cheque):
        self.empleados = empleados
        if horas_extras < 0:
            raise ValueError("horas_extras no puede ser negativo.")
        else:
            self.horas_extras = float(horas_extras)
        self.tipo_cheque = tipo_cheque
        #COLA ----------------------------------------------------------------------------
        self.cola_empleados = deque(list(empleados))
        self.cola_resultado = deque()

#esta clase manda a las otras hacer los calculos

#COLA PARA GUARDAR LOS RESULTADOS--------------------------------------------------------
    def encolar(self, resultado):
        self.cola_resultado.append(resultado)

    def desencolar(self):
        if not self.esta_vacia():
            return self.cola_resultado.popleft()
        return None
    
    def esta_vacia(self):
        cant = 0
        for _ in self.cola_resultado:
            cant += 1
        return cant == 0

#-----------------------------------------------------------------------------------------
    #def calcula_neto(self, empleado: Empleado)
    def obtener_neto_por_horas_extras(self, empleado):
        tarifa_hora = getattr(empleado, "salario_base", 0.0)
        #Esta manda a la otra clase hacer el calculo
        # DEBUG: mostrar valores usados para calcular por horas
        try:
            print(f"DEBUG obtener_neto_por_horas_extras - empleado.id={getattr(empleado,'id',None)}, salario_base={getattr(empleado,'salario_base',None)}, tarifa_hora_attr={getattr(empleado,'tarifa_hora',None)}, horas_extras={self.horas_extras}")
        except Exception:
            pass

        calculador = obtenerNetoXHoras()
        resultado = calculador.calcular_y_guardar(empleado, self.horas_extras, tarifa_hora)

        try:
            print(f"DEBUG obtener_neto_por_horas_extras - resultado: {resultado}")
        except Exception:
            pass

        return resultado

    def obtener_neto_por_contrato(self, empleado):
        #Aqui igual
        deduccion_extra = getattr(empleado, "deduccion_extra", "")
        tipo_deduccion = getattr(empleado, "tipo_deduccion", "")
        # DEBUG: mostrar valores antes de calcular contrato
        try:
            print(f"DEBUG obtener_neto_por_contrato - empleado.id={getattr(empleado,'id',None)}, salario_base={getattr(empleado,'salario_base',None)}, tarifa_hora={getattr(empleado,'tarifa_hora',None)}, tipo_contrato={getattr(empleado,'tipo_contrato',None)}, deduccion_extra={deduccion_extra}, tipo_deduccion={tipo_deduccion}")
        except Exception:
            pass

        calculador = calcularNetoXContrato()
        resultado_contrato = calculador.calcular_y_guardar(empleado, deduccion_extra, tipo_deduccion)

        try:
            print(f"DEBUG obtener_neto_por_contrato - resultado_contrato: {resultado_contrato}")
        except Exception:
            pass

        return resultado_contrato
    
    def calcula_neto_para_empleado(self, empleado):
        if empleado is None:
            raise ValueError("No hay empleado.")
        
        tipo_contrato = getattr(empleado, "tipo_contrato", "").strip()
        
        try:
            if tipo_contrato == "Semanal":
                resultado = self.obtener_neto_por_horas_extras(empleado)
            elif tipo_contrato == "Quincenal":
                resultado = self.obtener_neto_por_contrato(empleado)
            else:
                return {
                    "id": getattr(empleado, "id", None),
                    "nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                    "salario_bruto": 0.0,
                    "deducciones": {
                        "normales": {},
                        "total_normales": 0.0,
                        "extras": {},
                        "total_extras": 0.0
                    },
                    "neto": 0.0,
                    "proceso": False,
                    "detalle": f"Tipo de contrato no reconocido: '{tipo_contrato}'"
                }
        except Exception as e:
            return {
                "Id": getattr(empleado, "id", None),
                "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "Bruto": 0.0,
                "Deducciones": {"total": 0.0},
                "Otras Deducciones": {"total": 0.0},
                "Neto": 0.0,
                "Proceso": False,
                "Detalle": f"Error al calcular.... {e}"
            }
    
        resultado.setdefault("Id", getattr(empleado, "id", None))
        resultado.setdefault("Nombre", f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip())
        resultado.setdefault("Bruto", float(resultado.get("Bruto", 0.0)))
        resultado.setdefault("Deducciones", resultado.get("Deducciones", {"total": 0.0}))
        resultado.setdefault("Otras Deducciones", resultado.get("Otras Deducciones", {"total": 0.0}))
        resultado.setdefault("Neto", float(resultado.get("Neto", 0.0)))
        resultado.setdefault("Proceso", bool(resultado.get("Proceso", True)))
        resultado.setdefault("Detalle", resultado.get("Detalle", ""))
        return resultado

    def combinar_y_encolar(self, resultado_horas, resultado_contrato, empleado, horas_extras=0, tipo_cheque=""):
        """
        Combina dos resultados (horas y contrato) ya calculados, suma horas extras y ajuste por tipo_cheque,
        crea un resultado unificado y lo encola en self.cola_resultado.
        """
        try:
            # DEBUG: mostrar los resultados de entrada a la combinación
            try:
                print(f"DEBUG combinar_y_encolar - resultado_horas={resultado_horas}")
                print(f"DEBUG combinar_y_encolar - resultado_contrato={resultado_contrato}")
            except Exception:
                pass
            # Normalizar inputs
            rh = resultado_horas or {}
            rc = resultado_contrato or {}

            # Extraer valores con robustez ante distintos esquemas
            bruto_horas = float(rh.get('bruto', rh.get('Bruto', 0.0) or 0.0))
            neto_horas = float(rh.get('neto', rh.get('Neto', 0.0) or 0.0))
            deduc_horas = float(rh.get('deducciones normales', rh.get('deducciones', {}).get('total_normales', rh.get('Deducciones', {}).get('total', 0.0) or 0.0) or 0.0))

            # Para contrato el bruto está dentro de 'calculo' o en claves antiguas
            bruto_contrato = float(rc.get('calculo', {}).get('salario_bruto', rc.get('salario_bruto', rc.get('Bruto', 0.0) or 0.0) or 0.0))
            neto_contrato = float(rc.get('neto', rc.get('Neto', 0.0) or 0.0))
            deduc_contrato = float(rc.get('deducciones', {}).get('total_normales', rc.get('Deducciones', {}).get('total', rc.get('deducciones_normales', 0.0) or 0.0) or 0.0))

            # Sumar bruto/deducciones/neto base
            bruto_total = round(bruto_horas + bruto_contrato, 2)
            deduc_total = round(deduc_horas + deduc_contrato, 2)
            neto_total = round(neto_horas + neto_contrato, 2)

            detalle_parts = []

            # Si hay horas extras, calcular su impacto usando la clase de horas
            if horas_extras and horas_extras > 0:
                try:
                    tarifa = float(getattr(empleado, 'salario_base', getattr(empleado, 'tarifa_hora', 0.0) or 0.0))
                    calc_horas = obtenerNetoXHoras()
                    res_h_extra = calc_horas.calcular_y_guardar(empleado, horas_extras, tarifa)
                    if isinstance(res_h_extra, dict) and res_h_extra.get('proceso', True):
                        bruto_extra = float(res_h_extra.get('bruto', 0.0))
                        neto_extra = float(res_h_extra.get('neto', 0.0))
                        deduc_extra = float(res_h_extra.get('deducciones normales', 0.0))
                        bruto_total = round(bruto_total + bruto_extra, 2)
                        deduc_total = round(deduc_total + deduc_extra, 2)
                        neto_total = round(neto_total + neto_extra, 2)
                        detalle_parts.append(f"Horas extras: {horas_extras}")
                except Exception:
                    detalle_parts.append("Horas extras: error al calcular")

            # Ajuste por tipo de cheque (pequeño monto fijo)
            TIPO_CHEQUE = {
                "pago de salario": 0,
                "caja chica": 20000,
                "otros gastos": 15000
            }
            tipo_norm = str(tipo_cheque or '').strip().lower()
            ajuste_cheque = float(TIPO_CHEQUE.get(tipo_norm, 0.0))
            if ajuste_cheque:
                neto_total = round(neto_total + ajuste_cheque, 2)
                detalle_parts.append(f"Ajuste {tipo_norm}: +{int(ajuste_cheque)}")

            resultado = {
                "Id": getattr(empleado, 'id', None),
                "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "Bruto": bruto_total,
                "Deducciones": {"total": deduc_total},
                "Otras_Deducciones": {"total": 0.0},
                "Neto": neto_total,
                "Proceso": True,
                "Detalle": '; '.join(detalle_parts)
            }

            # DEBUG: valores finales calculados
            try:
                print(f"DEBUG combinar_y_encolar - bruto_total={bruto_total}, deduc_total={deduc_total}, neto_total={neto_total}, detalle_parts={detalle_parts}")
            except Exception:
                pass

            # Encolar el resultado unificado
            self.encolar(resultado)
            return resultado

        except Exception as e:
            res = {
                "Id": getattr(empleado, 'id', None),
                "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                "Bruto": 0.0,
                "Deducciones": {"total": 0.0},
                "Otras_Deducciones": {"total": 0.0},
                "Neto": 0.0,
                "Proceso": False,
                "Detalle": f"Error al combinar: {e}"
            }
            self.encolar(res)
            return res

 
    def procesar_todos_empleados(self):
        resultados = []
        for empleado in self.empleados:
            res = self.calcula_neto_para_empleado(empleado)
            #SE MANDA A LA COLA----------------------------------------------------------
            self.encolar(res)
            resultados.append(res)
        return resultados

        

       