import csv
from Ordenamiento import merge_sort
from Busqueda_binaria import binary_search

class DataManager:
    """Gestiona la carga y manipulación de datos de empleados"""
    
    def __init__(self):
        self.empleados = []
        self.empleados_ordenados = []
    
    def cargar_csv(self, archivo):
        """Carga empleados desde un archivo CSV"""
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                self.empleados = list(csv_reader)
            return True, f"Se cargaron {len(self.empleados)} empleados correctamente"
        except Exception as e:
            return False, f"Error al cargar el archivo: {str(e)}"
    
    def ordenar_por_campo(self, campo):
        """Ordena empleados por un campo específico usando Merge Sort"""
        if not self.empleados:
            return False, "No hay empleados cargados"
        
        try:
            self.empleados_ordenados = merge_sort(self.empleados, key=lambda emp: emp[campo])
            return True, f"Empleados ordenados por {campo} usando Merge Sort O(n log n)"
        except Exception as e:
            return False, f"Error al ordenar: {str(e)}"
    
    def buscar_por_nombre(self, valor_busqueda):
        """Busca un empleado por nombre usando Binary Search"""
        if not self.empleados_ordenados:
            return None, "Primero ordena los empleados"
        
        valor_busqueda = valor_busqueda.strip().lower()
        if not valor_busqueda:
            return None, "Ingresa un valor para buscar"
        
        # Crear lista de nombres en minúsculas para la búsqueda
        nombres = [emp['nombre'].lower() for emp in self.empleados_ordenados]
        
        # Usar binary search
        indice = binary_search(nombres, valor_busqueda)
        
        if indice != -1:
            return self.empleados_ordenados[indice], None
        else:
            return None, f"No se encontró empleado con nombre: {valor_busqueda}"
    
    def obtener_empleados(self):
        """Retorna los empleados ordenados si existen, sino los originales"""
        return self.empleados_ordenados if self.empleados_ordenados else self.empleados
    
    def obtener_cantidad_empleados(self):
        """Retorna la cantidad total de empleados"""
        return len(self.empleados)