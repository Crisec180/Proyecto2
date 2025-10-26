class CalculoDeDeducciones:
    def __init__(self, bruto):
        self.bruto = bruto

        self.deducciones = {
            "CCSS": bruto * 0.105, 
            "Banco": bruto * 0.01,   
            "Impuesto sobre la Renta": self.impuesto_sobre_la_renta()
        }
        
    def impuesto_sobre_la_renta(self):
        if self.bruto <= 922000:
            return 0.0
        elif self.bruto <= 1352000:
            return (self.bruto - 922000) * 0.10
        elif self.bruto <= 2373000:
            return (1352000 - 922000) * 0.10 + (self.bruto - 1352000) * 0.15
        elif self.bruto <= 4745000:
            return (1352000 - 922000) * 0.10 + (2373000 - 1352000) * 0.15 + (self.bruto - 2373000) * 0.20
        else:
            return ((1352000 - 922000) * 0.10 +
                    (2373000 - 1352000) * 0.15 +
                    (4745000 - 2373000) * 0.20 +
                    (self.bruto - 4745000) * 0.25)

    def calcular_deducciones(self):
        return self.bruto * 0.10
    
    def mostrar_deducciones(self):
        for nombre, valor in self.deducciones.items():
            print(f"{nombre}: {valor}")
