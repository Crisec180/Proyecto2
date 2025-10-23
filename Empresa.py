#La clase que recibe todo los datos de chequeo y empleados
from CalculoConCOLAS import CalculaNetoEmpleado
from ListaEmpleados import ListaEmpleados


class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.empleados = []

    TIPO_CHEQUE = {"Pago de salario", "Caja chica", "Otros Gastos"}

#aqui hay que cargar los .csv

    def obtener_empleado(self, id):
        for empleado in self.empleados:
            if empleado.id == id:
                return empleado
        return None

    def guardar_registros_CSV(self, archivo):
        print("guardar")


    #salario con reducciones
    def calcular_neto_empleados(self, horas_extras, tipo_cheque):
        if not isinstance(horas_extras, (int, float)) or horas_extras < 0:
            raise ValueError("horas_extras debe ser numérico no negativo.")
        if not isinstance(self.empleados, list):
            raise TypeError("self.empleados debe ser una lista de empleados.")

        calculaNeto = CalculaNetoEmpleado(list(self.empleados), horas_extras, tipo_cheque)

        resultados = []
        for empleado in list(self.empleados):
        # delegar a CalculaNetoEmpleado
            res = calculaNeto.calcula_neto_para_empleado(empleado)

        # aplicar ajuste por tipo de cheque
            ajuste = 0.0
            if tipo_cheque == "caja_chica":
                ajuste = 20000.0
            elif tipo_cheque == "otros_gastos":
                ajuste = 15000.0
            res["neto"] = round(float(res.get("neto", 0.0)) + ajuste, 2)
            #para mostrar
            if ajuste:
                res["detalle"] = (res.get("detalle", "") + f"; ajuste {tipo_cheque} +{int(ajuste)}").lstrip("; ")

            calculaNeto.encolar(res)
            resultados.append(res)
        return resultados


    def procesa_cheque(self, empleado_id, horas_extras, tipo_cheque):
        if not isinstance(horas_extras, (int, float)) or horas_extras < 0:
            raise ValueError("horas_extras debe ser numérico no negativo.")

        empleado = self.obtener_empleado(empleado_id)
        if empleado is None:
            return {"success": False, "detalle": f"Empleado con ID {empleado_id} no encontrado."}

        calculaNeto = CalculaNetoEmpleado([empleado], horas_extras, tipo_cheque)
        res = calculaNeto.calcula_neto_para_empleado(empleado)

        ajuste = 0.0
        if tipo_cheque == "caja_chica":
            ajuste = 20000.0
        elif tipo_cheque == "otros_gasto":
            ajuste = 15000.0

        res["neto"] = round(float(res.get("neto", 0.0)) + ajuste, 2)
        if ajuste:
            res["detalle"] = (res.get("detalle", "") + f"; ajuste {tipo_cheque} +{int(ajuste)}").lstrip("; ")

        calculaNeto.encolar(res)
        return calculaNeto.desencolar()

    
    

