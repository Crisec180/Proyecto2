class CalculoDeDeducciones:
    def __init__(self, bruto, deduccion_extra, tipo_deduccion):
        self.bruto = bruto
        self.deduccion_extra = deduccion_extra
        self.tipo_deduccion = tipo_deduccion

        self.deducciones_voluntarias = {
            "Seguro privado": bruto * 0.03,
            "Fondo de Pensiones": bruto * 0.05,
            "Donacion Opcional": 10000,
        }
        self.deducciones_contrato = {
            "Prestamo privado": bruto * 0.05,
            "Ahorro": bruto * 0.02,
        }
        self.deducciones_judiciales = {
            "Embargo": bruto * 0.15,
            "Pensión alimentaria": bruto * 0.35,
        }

    def tipo_seleccionada(self):
        if self.tipo_deduccion == "Voluntaria":
            return self.deducciones_voluntarias
        elif self.tipo_deduccion == "Contrato":
            return self.deducciones_contrato
        elif self.tipo_deduccion == "Judicial":
            return self.deducciones_judiciales
        else:
            return {}

    def seleccionar_deduccion(self):
        tipo = self.tipo_seleccionada()
        return tipo.get(self.deduccion_extra, None)

    def nombre_deduccion(self):
        return self.deduccion_extra

    def calcular_neto(self):
        monto = self.seleccionar_deduccion()
        if monto is None:
            return f"Deducción '{self.deduccion_extra}' no encontrada"
        return self.bruto - monto