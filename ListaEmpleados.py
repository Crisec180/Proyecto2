#Ojo trabajemos con los empleados ya hechos para no estar metiendo esos datos
from Empleado import Empleado
import csv

class ListaEmpleados:
    def __init__(self):
        self.empleados = []

    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def eliminar_empleado(self, empleado):
        if empleado in self.empleados:
            self.empleados.remove(empleado)

    def obtener_empleados(self):
        return self.empleados
    
    def guardar_en_CSV(self, nombre_archivo):
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
                escritor_csv = csv.writer(archivo)
                escritor_csv.writerow(['id', 'nombre', 'apellido', 'edad', 'telefono', 'correo'])
                
                # 3. Escribir los datos de los empleados
                for empleado in self.empleados:
                    escritor_csv.writerow([empleado.id, 
                                           empleado.nombre, 
                                           empleado.apellido, 
                                           empleado.departamento, 
                                           empleado.puesto, 
                                           empleado.salario, 
                                           empleado.tipo_pago, 
                                           empleado.fecha_ingreso]) 
            print(f"Empleados guardados exitosamente en {nombre_archivo}.")
        except Exception as e:
            print(f"Error al guardar en CSV: {e}")

    #ya funcionan los dos
    def cargar_empleados_desde_CSV(self, nombre_archivo):
        try:
            self.empleados = []         #(utf-8) es para leer tíldes
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lector_csv = csv.reader(archivo)
                #salta la fila de encabezado
                next(lector_csv, None) 
                
                for fila in lector_csv:
                    if len(fila) == 8:
                        id_emp, nombre, apellido, departamento, puesto, salario_str, tipo_pago, fecha_ingreso = fila
                        try:
                            empleado = Empleado(id_emp, nombre, apellido, departamento, puesto, float(salario_str), tipo_pago, fecha_ingreso)
                            self.agregar_empleado(empleado)
                        except ValueError:
                            print(f"Advertencia: Fila omitida. Salario '{salario_str}' no es un número válido: {fila}")
                    else:
                        print(f"Advertencia: Fila omitida por formato incorrecto (se esperaban 8 columnas): {fila}")

            print(f"Empleados cargados exitosamente desde {nombre_archivo}.")

        except FileNotFoundError:
            print(f"El archivo {nombre_archivo} no fue encontrado.")
        except Exception as e:
            print(f"Error al cargar desde CSV: {e}")

    #Recursividad----------------------------------------------------
    @staticmethod
    def _merge_por_nombre(izquierda, derecha, key):
        result = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            left_val = key(izquierda[i])
            right_val = key(derecha[j])
            if isinstance(left_val, str) and isinstance(right_val, str):
                left_val = left_val.lower()
                right_val = right_val.lower()
            if left_val <= right_val:
                result.append(izquierda[i])
                i += 1
            else:
                result.append(derecha[j])
                j += 1
        if i < len(izquierda):
            result.extend(izquierda[i:])
        if j < len(derecha):
            result.extend(derecha[j:])
        return result

    @classmethod
    def _merge_sort(cls, lista, key):
        if len(lista) <= 1:
            return lista[:]
        mid = len(lista) // 2
        left_sorted = cls._merge_sort(lista[:mid], key)
        right_sorted = cls._merge_sort(lista[mid:], key)
        return cls._merge_por_nombre(left_sorted, right_sorted, key)

    def ordenar_por_nombre(self, in_place=True):
        key = lambda e: e.nombre
        sorted_list = self._merge_sort(self.empleados, key)
        if in_place:
            self.empleados = sorted_list
            return None
        return sorted_list

#-----------------------------------------------------------------