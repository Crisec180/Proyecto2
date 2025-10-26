from Empresa import Empresa

class Empleado:
    def __init__(self, id, nombre, apellido, salario_base, tipo_contrato, departamento="", deduccion_extra=None, tipo_deduccion=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.salario_base = salario_base
        self.tipo_contrato = tipo_contrato
        self.departamento = departamento
        self.deduccion_extra = deduccion_extra
        self.tipo_deduccion = tipo_deduccion

def main():
    empresa = Empresa("ACME")
    e1 = Empleado(1, "Ana", "Gomez", 5000.0, "Horas", departamento="Ingeniería")
    e2 = Empleado(2, "Carlos", "Perez", 800000.0, "Quincenal", deduccion_extra="Fondo de Pensiones", tipo_deduccion="Voluntaria")
    empresa.empleados.extend([e1, e2])

    # Procesar todos (horas_extras para empleados por horas)
    resultados = empresa.calcular_neto_empleados(horas_extras=40, tipo_cheque="pago de salario")
    for r in resultados:
        print(r)

    # Procesar un cheque individual
    print(empresa.procesa_cheque(2, horas_extras=0, tipo_cheque="caja_chica"))

if __name__ == "__main__":
    main()
