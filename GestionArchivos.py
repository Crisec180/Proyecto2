import csv
import os
import json
from datetime import datetime
from collections import deque

class GestionArchivos:
    Cola_Cheques_csv = "cola_cheques.csv"
    Pila_Horas_csv = "pila_horas.csv"
    Pila_Contratos_csv = "pila_contratos.csv"
    Diccionario_Calculos_csv = "diccionario_calculos.csv"
    Lista_Impresion_csv = "lista_impresion.csv"
    
    @staticmethod
    def existe_archivo(nombre_archivo):
        return os.path.exists(nombre_archivo)
    
    @staticmethod
    def guardar_cola_cheques(cola_cheques, nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = GestionArchivos.Cola_Cheques_csv
        
        if not cola_cheques:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id_empleado', 'nombre', 'apellido', 'departamento', 'puesto',
                    'salario', 'tipo_pago', 'horas_extras', 'tipo_cheque', 
                    'estado', 'fecha_creacion'
                ])
            return True, f"Archivo creado (cola vacía)"
        
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id_empleado', 'nombre', 'apellido', 'departamento', 'puesto',
                    'salario', 'tipo_pago', 'horas_extras', 'tipo_cheque', 
                    'estado', 'fecha_creacion'
                ])
                
                for item in cola_cheques:
                    empleado = item.get('empleado')
                    
                    if isinstance(empleado, str):
                        id_emp = empleado
                        nombre = ''
                        apellido = ''
                        departamento = ''
                        puesto = ''
                        salario = 0
                        tipo_pago = ''
                    elif isinstance(empleado, dict):
                        id_emp = empleado.get('id', '')
                        nombre = empleado.get('nombre', '')
                        apellido = empleado.get('apellido', '')
                        departamento = empleado.get('departamento', '')
                        puesto = empleado.get('puesto', '')
                        salario = empleado.get('salario_base', empleado.get('salario', 0))
                        tipo_pago = empleado.get('tipo_contrato', empleado.get('tipo_pago', ''))
                    else: 
                        id_emp = getattr(empleado, 'id', '')
                        nombre = getattr(empleado, 'nombre', '')
                        apellido = getattr(empleado, 'apellido', '')
                        departamento = getattr(empleado, 'departamento', '')
                        puesto = getattr(empleado, 'puesto', '')
                        salario = getattr(empleado, 'salario_base', getattr(empleado, 'salario', 0))
                        tipo_pago = getattr(empleado, 'tipo_contrato', getattr(empleado, 'tipo_pago', ''))
                    
                    writer.writerow([
                        id_emp,
                        nombre,
                        apellido,
                        departamento,
                        puesto,
                        salario,
                        tipo_pago,
                        item.get('horas_extras', 0),
                        item.get('tipo_cheque', ''),
                        item.get('estado', 'En espera'),
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ])
            
            return True, f"Cola guardada: {len(cola_cheques)} elementos"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def guardar_pila(pila, nombre_archivo):
        if not pila:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'nombre', 'datos_json', 'fecha_guardado'])
            return True, f"Archivo creado (pila vacía)"
        
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'nombre', 'datos_json', 'fecha_guardado'])
                
                for item in pila:
                    id_emp = item.get('id', '')
                    nombre = item.get('nombre', 'N/A')
                    datos_json = json.dumps(item, ensure_ascii=False)
                    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    writer.writerow([id_emp, nombre, datos_json, fecha])
            
            return True, f"Pila guardada: {len(pila)} elementos"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def guardar_diccionario(diccionario, nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = GestionArchivos.Diccionario_Calculos_csv
        
        if not diccionario:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id_empleado', 'tipo_calculo', 'datos_json', 'fecha_guardado'])
            return True, f"Archivo creado (diccionario vacío)"
        
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['id_empleado', 'tipo_calculo', 'datos_json', 'fecha_guardado'])
                
                for id_empleado, calculos in diccionario.items():
                    if isinstance(calculos, dict):
                        for tipo_calculo, datos in calculos.items():
                            datos_json = json.dumps(datos, ensure_ascii=False)
                            fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            writer.writerow([id_empleado, tipo_calculo, datos_json, fecha])
                    else:
                        datos_json = json.dumps(calculos, ensure_ascii=False)
                        fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        writer.writerow([id_empleado, 'valor_directo', datos_json, fecha])
            
            return True, f"Diccionario guardado: {len(diccionario)} claves"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def guardar_lista_impresion(lista, nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = GestionArchivos.Lista_Impresion_csv
        
        if not lista:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id_empleado', 'nombre_completo', 'monto', 'concepto', 
                    'fecha_cheque', 'fecha_guardado'
                ])
            return True, f"Archivo creado (lista vacía)"
        
        try:
            with open(nombre_archivo, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'id_empleado', 'nombre_completo', 'monto', 'concepto', 
                    'fecha_cheque', 'fecha_guardado'
                ])
                
                for cheque in lista:
                    if isinstance(cheque, tuple) and len(cheque) >= 5:
                        id_emp, nombre, monto, concepto, fecha = cheque
                    elif isinstance(cheque, dict):
                        id_emp = cheque.get('id_empleado', '')
                        nombre = cheque.get('nombre', '')
                        monto = cheque.get('monto', 0)
                        concepto = cheque.get('concepto', '')
                        fecha = cheque.get('fecha', '')
                    else:
                        continue
                    
                    writer.writerow([
                        id_emp,
                        nombre,
                        monto,
                        concepto,
                        fecha,
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ])
            
            return True, f"Lista guardada: {len(lista)} elementos"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def cargar_cola_cheques(nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = GestionArchivos.Cola_Cheques_csv
        
        if not os.path.exists(nombre_archivo):
            return []
        
        try:
            cola = []
            with open(nombre_archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    empleado_dict = {
                        'id': row['id_empleado'],
                        'nombre': row['nombre'],
                        'apellido': row['apellido'],
                        'departamento': row['departamento'],
                        'puesto': row['puesto'],
                        'salario': float(row['salario']) if row['salario'] else 0,
                        'tipo_pago': row['tipo_pago'],
                        'salario_base': float(row['salario']) if row['salario'] else 0,
                        'tipo_contrato': row['tipo_pago']
                    }
                    
                    item = {
                        'empleado': empleado_dict,
                        'empleado_dict': empleado_dict,
                        'horas_extras': float(row['horas_extras']) if row['horas_extras'] else 0,
                        'tipo_cheque': row['tipo_cheque'],
                        'estado': row['estado'],
                        'resultado': None
                    }
                    
                    cola.append(item)
            
            return cola
        except Exception as e:
            print(f"Error al cargar cola: {e}")
            return []
    
    @staticmethod
    def cargar_pila(nombre_archivo):
        if not os.path.exists(nombre_archivo):
            return []
        
        try:
            pila = []
            with open(nombre_archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    datos = json.loads(row['datos_json'])
                    pila.append(datos)
            
            return pila
        except Exception as e:
            print(f"Error al cargar pila: {e}")
            return []
    
    @staticmethod
    def cargar_diccionario(nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = GestionArchivos.Diccionario_Calculos_csv
        
        if not os.path.exists(nombre_archivo):
            return {}
        
        try:
            diccionario = {}
            with open(nombre_archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    id_empleado = row['id_empleado']
                    tipo_calculo = row['tipo_calculo']
                    datos = json.loads(row['datos_json'])
                    
                    if id_empleado not in diccionario:
                        diccionario[id_empleado] = {}
                    
                    if tipo_calculo == 'valor_directo':
                        diccionario[id_empleado] = datos
                    else:
                        diccionario[id_empleado][tipo_calculo] = datos
            
            return diccionario
        except Exception as e:
            print(f"Error al cargar diccionario: {e}")
            return {}
    
    @staticmethod
    def cargar_lista_impresion(nombre_archivo=None):
        if nombre_archivo is None:
            nombre_archivo = GestionArchivos.Lista_Impresion_csv
        
        if not os.path.exists(nombre_archivo):
            return []
        
        try:
            lista = []
            with open(nombre_archivo, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    cheque = (
                        row['id_empleado'],
                        row['nombre_completo'],
                        row['monto'],
                        row['concepto'],
                        row['fecha_cheque']
                    )
                    lista.append(cheque)
            
            return lista
        except Exception as e:
            print(f"Error al cargar lista: {e}")
            return []
    
    @staticmethod
    def guardar_todos_los_datos(cola_cheques, pila_horas, pila_contratos, 
                                 diccionario_calculos, lista_impresion):
        resultados = []
        
        exito, mensaje = GestionArchivos.guardar_cola_cheques(cola_cheques)
        resultados.append((exito, mensaje))
        
        exito, mensaje = GestionArchivos.guardar_pila(
            pila_horas, 
            GestionArchivos.Pila_Horas_csv
        )
        resultados.append((exito, mensaje))
        
        exito, mensaje = GestionArchivos.guardar_pila(
            pila_contratos, 
            GestionArchivos.Pila_Contratos_csv
        )
        resultados.append((exito, mensaje))
        
        exito, mensaje = GestionArchivos.guardar_diccionario(diccionario_calculos)
        resultados.append((exito, mensaje))
        
        exito, mensaje = GestionArchivos.guardar_lista_impresion(lista_impresion)
        resultados.append((exito, mensaje))
        
        return resultados
    
    @staticmethod
    def cargar_todos_los_datos():
        cola = GestionArchivos.cargar_cola_cheques()
        pila_horas = GestionArchivos.cargar_pila(GestionArchivos.Pila_Horas_csv)
        pila_contratos = GestionArchivos.cargar_pila(GestionArchivos.Pila_Contratos_csv)
        diccionario = GestionArchivos.cargar_diccionario()
        lista_impresion = GestionArchivos.cargar_lista_impresion()
        
        cola_deque = deque(cola)
        
        return cola_deque, pila_horas, pila_contratos, diccionario, lista_impresion
    
    @staticmethod
    def limpiar_todos_los_archivos():
        archivos = [
            GestionArchivos.Cola_Cheques_csv,
            GestionArchivos.Pila_Horas_csv,
            GestionArchivos.Pila_Contratos_csv,
            GestionArchivos.Diccionario_Calculos_csv,
            GestionArchivos.Lista_Impresion_csv
        ]
        
        eliminados = 0
        for archivo in archivos:
            if os.path.exists(archivo):
                try:
                    os.remove(archivo)
                    eliminados += 1
                except Exception as e:
                    print(f"Error al eliminar {archivo}: {e}")
        
        return eliminados
    
    @staticmethod
    def obtener_estadisticas():
        stats = {
            'cola_cheques': 0,
            'pila_horas': 0,
            'pila_contratos': 0,
            'diccionario': 0,
            'lista_impresion': 0
        }
        
        archivos_info = [
            (GestionArchivos.Cola_Cheques_csv, 'cola_cheques'),
            (GestionArchivos.Pila_Horas_csv, 'pila_horas'),
            (GestionArchivos.Pila_Contratos_csv, 'pila_contratos'),
            (GestionArchivos.Diccionario_Calculos_csv, 'diccionario'),
            (GestionArchivos.Lista_Impresion_csv, 'lista_impresion')
        ]
        
        for archivo, clave in archivos_info:
            if os.path.exists(archivo):
                try:
                    with open(archivo, 'r', encoding='utf-8') as f:
                        stats[clave] = sum(1 for _ in f) - 1
                except:
                    pass
        
        return stats