

class CalculoDeSalarioBruto:
    def __init__(self, horas_trabajadas, valor_hora):
        self.horas_trabajadas = horas_trabajadas
        self.valor_hora = valor_hora

    def calcular_bruto(self):
        return self.horas_trabajadas * self.valor_hora
    

    def diccPrecioHora(self):
        return {
            "Valor1": 4.50,
            "Valor2": 5.00,
            "Valor3": 6.00
        }

    def diccionario_bruto(self):
        bruto = self.calcular_bruto()
        return {
            "horas_trabajadas": self.horas_trabajadas,
            "valor_hora": self.valor_hora,
            "salario_bruto": bruto
        }