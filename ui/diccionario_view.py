import customtkinter as ctk
from tkinter import messagebox
from CalculosConDiccionarios.CalculaBrutoXHora import calculoDeSalarioBruto
from CalculosConDiccionarios.CalcularDeduccionNormal import calculoDeDeducciones
from CalculosConDiccionarios.CalculaOtrasDeducciones import calculoDeDeduccionesExtras
from Empleado import Empleado
from GestionArchivos import GestionArchivos

class DiccionarioView:
    
    def __init__(self, parent, diccionario, data_manager, main_window):
        self.parent = parent
        self.diccionario = diccionario
        self.data_manager = data_manager
        self.main_window = main_window
    
    def render(self):
        self.create_header()
        
        content_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        self.create_left_panel(content_frame)
        self.create_right_panel(content_frame)
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(header_frame, text="Diccionario: Cálculos Varios", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text="Usa: CalculaBrutoXHora, CalcularDeduccionNormal, CalculaOtrasDeducciones", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#dc2626"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def crear_objeto_empleado(self, emp_dict):
        """Convierte diccionario de empleado a objeto Empleado"""
        return Empleado(
            id=emp_dict.get('id', ''),
            nombre=emp_dict.get('nombre', ''),
            apellido=emp_dict.get('apellido', ''),
            departamento=emp_dict.get('departamento', 'General'),
            puesto=emp_dict.get('puesto', 'Empleado'),
            salario_base=float(emp_dict.get('salario_base', 0)),
            tipo_contrato=emp_dict.get('tipo_contrato', 'Mensual')
        )
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Calcular y Agregar al Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="Empleado (Clave):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        
        empleados = self.data_manager.obtener_empleados()
        if empleados:
            opciones_empleados = [f"{emp.get('id', '')} - {emp.get('nombre', '')} {emp.get('apellido', '')}" for emp in empleados]
            key_menu = ctk.CTkOptionMenu(left_panel, values=opciones_empleados)
            key_menu.pack(pady=(0, 10), padx=20, fill="x")
            
            empleado_actual = self.data_manager.obtener_empleado_seleccionado()
            if empleado_actual:
                texto_actual = f"{empleado_actual.get('id', '')} - {empleado_actual.get('nombre', '')} {empleado_actual.get('apellido', '')}"
                if texto_actual in opciones_empleados:
                    key_menu.set(texto_actual)
        else:
            key_menu = ctk.CTkOptionMenu(left_panel, values=["No hay empleados"])
            key_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Tipo de Cálculo:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        tipo_menu = ctk.CTkOptionMenu(left_panel, values=[
            "Bruto por Horas",
            "Deducciones Normales",
            "Otras Deducciones"
        ])
        tipo_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        self.campos_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        self.campos_frame.pack(fill="x", padx=20, pady=10)
        
        def actualizar_campos(*args):
            for widget in self.campos_frame.winfo_children():
                widget.destroy()
            
            tipo = tipo_menu.get()
            
            if tipo == "Bruto por Horas":
                ctk.CTkLabel(self.campos_frame, text="Horas Trabajadas:").pack(pady=(5, 2), anchor="w")
                self.input1 = ctk.CTkEntry(self.campos_frame, placeholder_text="Ej: 45")
                self.input1.pack(fill="x", pady=(0, 10))
                
                ctk.CTkLabel(self.campos_frame, text="Tarifa por Hora:").pack(pady=(5, 2), anchor="w")
                self.input2 = ctk.CTkEntry(self.campos_frame, placeholder_text="Ej: 5000")
                self.input2.pack(fill="x", pady=(0, 10))
                
            elif tipo == "Deducciones Normales":
                ctk.CTkLabel(self.campos_frame, text="Salario Bruto:").pack(pady=(5, 2), anchor="w")
                self.input1 = ctk.CTkEntry(self.campos_frame, placeholder_text="Ej: 500000")
                self.input1.pack(fill="x", pady=(0, 10))
                
            elif tipo == "Otras Deducciones":
                ctk.CTkLabel(self.campos_frame, text="Salario Bruto:").pack(pady=(5, 2), anchor="w")
                self.input1 = ctk.CTkEntry(self.campos_frame, placeholder_text="Ej: 500000")
                self.input1.pack(fill="x", pady=(0, 10))
                
                ctk.CTkLabel(self.campos_frame, text="Tipo de Deducción:").pack(pady=(5, 2), anchor="w")
                self.input2 = ctk.CTkOptionMenu(self.campos_frame, values=["Voluntaria", "Contrato", "Judicial"])
                self.input2.pack(fill="x", pady=(0, 10))
                
                ctk.CTkLabel(self.campos_frame, text="Deducción Específica:").pack(pady=(5, 2), anchor="w")
                self.input3 = ctk.CTkOptionMenu(self.campos_frame, values=[
                    "Seguro privado", "Fondo de Pensiones", "Donacion Opcional",
                    "Prestamo privado", "Ahorro", "Embargo", "Pensión alimentaria"
                ])
                self.input3.pack(fill="x", pady=(0, 10))
        
        tipo_menu.configure(command=actualizar_campos)
        actualizar_campos() 
        
        def calcular_y_agregar():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = key_menu.get()
            tipo = tipo_menu.get()
            
            if not seleccion or "No hay empleados" in seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un empleado válido")
                return
            
            key = seleccion.split(" - ")[0]
            emp_dict, error = self.data_manager.buscar_por_id(key)
            
            if error:
                messagebox.showerror("Error", error)
                return
            
            empleado_obj = self.crear_objeto_empleado(emp_dict)
            
            try:
                if tipo == "Bruto por Horas":
                    horas_str = self.input1.get()
                    tarifa_str = self.input2.get()
                    
                    if not horas_str or not tarifa_str:
                        messagebox.showwarning("Advertencia", "Completa todos los campos")
                        return
                    
                    horas = float(horas_str)
                    tarifa = float(tarifa_str)
                    
                    empleado_obj.tarifa_hora = tarifa
                    
                    calculador = calculoDeSalarioBruto(empleado_obj, horas)
                    resultado = calculador.calcular_bruto_x_hora()
                    
                    if key not in self.diccionario:
                        self.diccionario[key] = {}
                    
                    self.diccionario[key]['Bruto por Horas'] = resultado
                    
                    mensaje = f"Cálculo: Bruto por Horas\n\n"
                    mensaje += f"Horas: {resultado['Horas_trabajadas']}\n"
                    mensaje += f"Tarifa Base: ${resultado['Tarifa_base']:,.2f}\n"
                    mensaje += f"Tarifa Final: ${resultado['Tarifa_final']:,.2f}\n"
                    mensaje += f"{resultado['Ajuste']}\n"
                    mensaje += f"Bruto Total: ${resultado['Bruto']:,.2f}\n\n"
                    mensaje += "Guardado en Diccionario (estructura dict)"
                    
                elif tipo == "Deducciones Normales":
                    bruto_str = self.input1.get()
                    
                    if not bruto_str:
                        messagebox.showwarning("Advertencia", "Ingresa el salario bruto")
                        return
                    
                    bruto = float(bruto_str)
                    
                    calculador = calculoDeDeducciones(bruto)
                    resultado = calculador.calcular_deducciones()
                    
                    if not resultado['Proceso']:
                        messagebox.showerror("Error", resultado['Detalle'])
                        return
                    
                    if key not in self.diccionario:
                        self.diccionario[key] = {}
                    
                    self.diccionario[key]['Deducciones Normales'] = resultado
                    
                    mensaje = f"Cálculo: Deducciones Normales\n\n"
                    mensaje += f"Bruto: ${bruto:,.2f}\n\n"
                    mensaje += "Desglose:\n"
                    for nombre, valor in resultado['Desglose'].items():
                        mensaje += f"  • {nombre}: ${valor:,.2f}\n"
                    mensaje += f"\nTotal Deducciones: ${resultado['Total']:,.2f}\n\n"
                    mensaje += "Guardado en Diccionario (estructura dict)"
                    
                elif tipo == "Otras Deducciones":
                    bruto_str = self.input1.get()
                    tipo_deduccion = self.input2.get()
                    deduccion_especifica = self.input3.get()
                    
                    if not bruto_str:
                        messagebox.showwarning("Advertencia", "Ingresa el salario bruto")
                        return
                    
                    bruto = float(bruto_str)
                    
                    calculador = calculoDeDeduccionesExtras(bruto, deduccion_especifica, tipo_deduccion)
                    resultado = calculador.calcular_deduccion_extra()
                    
                    if not resultado['Proceso']:
                        messagebox.showerror("Error", resultado['Detalle'])
                        return
                    
                    if key not in self.diccionario:
                        self.diccionario[key] = {}
                    
                    self.diccionario[key]['Otras Deducciones'] = resultado
                    
                    mensaje = f"Cálculo: Otras Deducciones\n\n"
                    mensaje += f"Bruto: ${bruto:,.2f}\n"
                    mensaje += f"Tipo: {tipo_deduccion}\n"
                    mensaje += f"Deducción: {deduccion_especifica}\n\n"
                    mensaje += f"Monto: ${resultado['Total']:,.2f}\n\n"
                    mensaje += "Guardado en Diccionario (estructura dict)"
                
                self.update_dict_display()
                
                try:
                    GestionArchivos.guardar_todos_los_datos(
                        self.main_window.cola_cheques,
                        self.main_window.pila_horas,
                        self.main_window.pila_contratos,
                        self.diccionario,
                        self.main_window.lista_impresion
                    )
                except Exception as e:
                    print(f"Error al guardar datos: {e}")
                
                messagebox.showinfo("Cálculo Exitoso", mensaje)
                
            except ValueError as ve:
                messagebox.showerror("Error", f"Valor inválido: {str(ve)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al calcular: {str(e)}")
        
        def remove():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados.")
                return
            
            seleccion = key_menu.get()
            if seleccion and "No hay empleados" not in seleccion:
                key = seleccion.split(" - ")[0]
                if key in self.diccionario:
                    respuesta = messagebox.askyesno("Confirmar", f"¿Eliminar todos los cálculos de {key}?")
                    if respuesta:
                        del self.diccionario[key]
                        self.update_dict_display()
                        
                        try:
                            GestionArchivos.guardar_todos_los_datos(
                                self.main_window.cola_cheques,
                                self.main_window.pila_horas,
                                self.main_window.pila_contratos,
                                self.diccionario,
                                self.main_window.lista_impresion
                            )
                        except Exception as e:
                            print(f"Error al guardar datos: {e}")
                        
                        messagebox.showinfo("Éxito", f"Cálculos eliminados para {key}")
                else:
                    messagebox.showinfo("No Encontrado", f"No hay cálculos para {key}")
        
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(btn_frame, text="Calcular y Guardar", command=calcular_y_agregar, 
                     fg_color="#dc2626", hover_color="#b91c1c", height=40).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="Eliminar Empleado", command=remove, 
                     fg_color="#6b7280", hover_color="#4b5563", height=35).pack(fill="x", pady=5)
        
        info_frame = ctk.CTkFrame(left_panel, fg_color="#2b2b2b", border_width=2, border_color="#dc2626")
        info_frame.pack(pady=10, padx=20, fill="x")
        
        info_text = "ℹEstructura: Diccionario (dict)\nClases usadas:\n  • calculoDeSalarioBruto\n  • calculoDeDeducciones\n  • calculoDeDeduccionesExtras"
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=9), 
                    text_color="gray", justify="left").pack(padx=10, pady=10)
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización del Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text="Diccionario Python (dict)\nClave-Valor para almacenar cálculos por empleado\nAcceso O(1) - Muy eficiente",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.dict_display = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.dict_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_dict_display()
    
    def update_dict_display(self):
        for widget in self.dict_display.winfo_children():
            widget.destroy()
        
        if not self.diccionario:
            ctk.CTkLabel(self.dict_display, text="Diccionario vacío\n\nRealiza cálculos para comenzar", 
                        text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            for key, values in self.diccionario.items():
                empleado, _ = self.data_manager.buscar_por_id(key)
                if empleado:
                    nombre_completo = f"{empleado.get('nombre', '')} {empleado.get('apellido', '')}"
                else:
                    nombre_completo = "Empleado Desconocido"
                
                key_frame = ctk.CTkFrame(self.dict_display, fg_color="#1a1a1a", border_width=2, border_color="#dc2626")
                key_frame.pack(fill="x", pady=10, padx=5)
                
                header_frame = ctk.CTkFrame(key_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                
                ctk.CTkLabel(header_frame, text=f"{key}", font=ctk.CTkFont(size=12, weight="bold"), 
                           text_color="#dc2626").pack(side="left")
                ctk.CTkLabel(header_frame, text=f"{nombre_completo}", font=ctk.CTkFont(size=11), 
                           text_color="gray").pack(side="left", padx=10)
                
                for tipo_calculo, datos in values.items():
                    calc_frame = ctk.CTkFrame(key_frame, fg_color="#2b2b2b")
                    calc_frame.pack(fill="x", padx=15, pady=5)
                    
                    ctk.CTkLabel(calc_frame, text=f"{tipo_calculo}", text_color="#dc2626", 
                               font=ctk.CTkFont(size=11, weight="bold")).pack(anchor="w", padx=10, pady=(5, 2))
                    
                    if isinstance(datos, dict):
                        if tipo_calculo == "Bruto por Horas":
                            info = f"  Horas: {datos.get('Horas_trabajadas', 0)}\n"
                            info += f"  Tarifa Base: ${datos.get('Tarifa_base', 0):,.2f}\n"
                            info += f"  {datos.get('Ajuste', '')}\n"
                            info += f"  Bruto: ${datos.get('Bruto', 0):,.2f}"
                        elif tipo_calculo == "Deducciones Normales":
                            info = f"  Total: ${datos.get('Total', 0):,.2f}\n"
                            if 'Desglose' in datos:
                                for nombre, valor in datos['Desglose'].items():
                                    info += f"  • {nombre}: ${valor:,.2f}\n"
                        elif tipo_calculo == "Otras Deducciones":
                            info = f"  Total: ${datos.get('Total', 0):,.2f}\n"
                            if 'Desglose' in datos:
                                for nombre, valor in datos['Desglose'].items():
                                    info += f"  • {nombre}: ${valor:,.2f}\n"
                        else:
                            info = f"  Valor: {datos}"
                        
                        ctk.CTkLabel(calc_frame, text=info, text_color="lightgray", 
                                   justify="left", font=ctk.CTkFont(size=10)).pack(anchor="w", padx=20, pady=(2, 5))
                    else:
                        ctk.CTkLabel(calc_frame, text=f"  ${float(datos):,.2f}", text_color="#2fa572", 
                                   font=ctk.CTkFont(size=11, weight="bold")).pack(side="right", padx=10, pady=5)
                
                ctk.CTkLabel(key_frame, text="").pack(pady=5)