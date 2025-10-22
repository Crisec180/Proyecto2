

class CalculoDeSalarioBruto:
    def __init__(self, empleado, horas_trabajadas, valor_hora):
        self.empleado = empleado
        self.horas_trabajadas = horas_trabajadas
        self.valor_hora = valor_hora
    

    def diccPrecioHora(self):
          {
              "precio1": 5.50,
              "precio2": 7.00,
              "precio3": 8.50
          }
    def calcular_bruto_x_hora(self):
         tarifa = self.diccPrecioHora()
         if self.horas_trabajadas <= 40:
             valor_hora = tarifa["precio1"]
         elif 40 < self.horas_trabajadas <= 80:
             valor_hora = tarifa["precio2"]
         elif self.horas_trabajadas > 80:
             valor_hora = tarifa["precio3"]
         else:
             raise ValueError("Opción no válida para el valor por hora.")

         salario_bruto = self.horas_trabajadas * valor_hora
         return salario_bruto