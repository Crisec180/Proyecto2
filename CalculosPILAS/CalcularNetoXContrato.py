class CalcularNetoXContrato:
    def __init__(self, bruto, deducciones):
        self.bruto = bruto
        self.deducciones = deducciones

    def calcular_neto(self):
        return self.bruto - self.deducciones