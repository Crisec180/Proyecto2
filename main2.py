from ListaEmpleados import ListaEmpleados

#ver si carga los empleados
lista = ListaEmpleados()
lista.cargar_empleados_desde_CSV('empleados.csv')

empleados = lista.obtener_empleados()

for emp in empleados:
    print(emp)  