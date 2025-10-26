from CalculosConDICCIONARIOS import CalculaBrutoXHora
from CalculosConDICCIONARIOS import CalcularDeduccionNormal

# Diccionario de bonos por departamento
#esto se le suma al bruto por horas
BONO_DEPARTAMENTO = {
    "Ingeniería": 0.5,
    "Administración": 0.3,
    "Ventas": 0.4
}
class ObtenerNetoXHoras:
    def __init__(self):
        self.pila = Pila.Pila()

    def calcular_y_guardar(self, empleado, horas_trabajadas, tarifa_hora):
        #Validaciones
        if not isinstance(horas_trabajadas, (int, float)) or horas_trabajadas < 0:
                return {"Proceso": False, "detalle": "Horas trabajadas inválidas."}
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
                return {"Proceso": False, "detalle": "Tarifa por hora inválida."}
        try:
            # Obtener el bono según el departamento
            bono = BONO_DEPARTAMENTO.get(empleado.departamento, 0.0)

            bruto = CalculaBrutoXHora(empleado, horas_trabajadas, tarifa_hora)

            bruto_bono = round(bruto_bono * (1 + bono), 2)
            deducciones_normales = CalcularDeduccionNormal(bruto_bono)
            neto = round(bruto_bono - deducciones_normales, 2)

            resultado = {
                    "Id": getattr(empleado, "id", None),
                    "Nombre": f"{getattr(empleado, 'nombre', '')} {getattr(empleado, 'apellido', '')}".strip(),
                    "Departamento": getattr(empleado, "departamento", ""),
                    "Horas_trabajadas": horas_trabajadas,
                    "Tarifa_hora": tarifa_hora,
                    "Bono_departamento": bono,
                    "Bruto": round(bruto, 2),
                    "Bruto_con_bono": bruto_bono,
                    "Deducciones_normales": deducciones_normales,
                    "Neto": neto,
                    "Proceso": True,
                    "Detalle": ""
                }
            #APILA LOS RESULTADOS
            self.pila.push(resultado)
            return resultado
        except Exception as e:
            return print(f"Error al calcular... {e}")
    
    def procesar(self):
        return self.pila.pop()

    def mostrar_pila(self):
        self.pila.mostrar()