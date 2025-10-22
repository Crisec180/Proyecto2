

class CalculoDeSalarioBruto:
    def __init__(self, empleado, horas_trabajadas, valor_hora):
        self.empleado = empleado
        self.horas_trabajadas = horas_trabajadas
        self.valor_hora = valor_hora
    

    def diccPrecioHora(self):
            if self.horas_trabajadas <= 40:
                return {"Valor1": 4.50}
            
            elif 40 < self.horas_trabajadas <= 80:
                return {"Valor2": 5.00}
            
            elif self.horas_trabajadas > 80:
                return {"Valor3": 6.00}

    def calcular_bruto_x_hora(self, diccPrecioHora):
        if self.horas_trabajadas <= 40:
            valor_hora = diccPrecioHora["Valor1"]
        elif 40 < self.horas_trabajadas <= 80:
            valor_hora = diccPrecioHora["Valor2"]
        elif self.horas_trabajadas > 80:
            valor_hora = diccPrecioHora["Valor3"]
        else:
            raise ValueError("Opción no válida para el valor por hora.")

        salario_bruto = self.horas_trabajadas * valor_hora
        return salario_bruto