class CalculoDeSalarioBruto:
    def __init__(self, horas_trabajadas, valor_hora):
        self.horas_trabajadas = horas_trabajadas
        self.valor_hora = valor_hora

    def calcular_bruto(self):
        return self.horas_trabajadas * self.valor_hora