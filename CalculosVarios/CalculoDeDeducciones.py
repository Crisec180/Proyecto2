from CalculosDeSalarioBruto import CalculosDeSalarioBruto

class CalculoDeDeducciones:
    #Posibles
    def deduccion_Horas_Extras(self, horas_extras, tarifa_hora, HorasTrabajadas, tarifaPorHora):
        calculo_salario = CalculosDeSalarioBruto()
        salario_bruto = calculo_salario.TarifaPorHora(HorasTrabajadas, tarifaPorHora)
        if horas_extras > 0:
            valor_hora_extra = tarifa_hora * 1.5
            return horas_extras * valor_hora_extra
        else:
            return 0

    def deduccion_Salud(self, salario_bruto):
        return salario_bruto * 0.08 

    def deduccion_Pension(self, salario_bruto):
        return salario_bruto * 0.05
