import customtkinter as ctk
from tkinter import messagebox
from CalculosPILAS.ObtenerNetoXHoras import obtenerNetoXHoras
from CalculosPILAS.CalcularNetoXContrato import calcularNetoXContrato
from Empleado import Empleado
from GestionArchivos import GestionArchivos

class PilaView:
    
    def __init__(self, parent, pila, titulo, label_text, data_manager, main_window):
        self.parent = parent
        self.pila = pila
        self.titulo = titulo
        self.label_text = label_text
        self.data_manager = data_manager
        self.main_window = main_window
        
        self.es_pila_horas = "Horas" in titulo
    
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
        
        clase_usada = "obtenerNetoXHoras" if self.es_pila_horas else "calcularNetoXContrato"
        
        title = ctk.CTkLabel(header_frame, text=f"Pila: {self.titulo}", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text=f"Visualización de la pila (LIFO) - Usa {clase_usada}", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#d97706"
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
        
        ctk.CTkLabel(left_panel, text="PUSH - Agregar a la Pila", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="Seleccionar Empleado:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        
        empleados = self.data_manager.obtener_empleados()
        if empleados:
            opciones_empleados = [f"{emp.get('nombre', '')} {emp.get('apellido', '')} - {emp.get('id', '')}" for emp in empleados]
            empleado_menu = ctk.CTkOptionMenu(left_panel, values=opciones_empleados)
            empleado_menu.pack(pady=(0, 10), padx=20, fill="x")
            
            empleado_actual = self.data_manager.obtener_empleado_seleccionado()
            if empleado_actual:
                texto_actual = f"{empleado_actual.get('nombre', '')} {empleado_actual.get('apellido', '')} - {empleado_actual.get('id', '')}"
                if texto_actual in opciones_empleados:
                    empleado_menu.set(texto_actual)
        else:
            empleado_menu = ctk.CTkOptionMenu(left_panel, values=["No hay empleados"])
            empleado_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        if self.es_pila_horas:
            ctk.CTkLabel(left_panel, text="Horas Trabajadas:").pack(pady=(10, 5), padx=20, anchor="w")
            valor_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 45 (horas)")
            valor_entry.pack(pady=(0, 10), padx=20, fill="x")
            
            ctk.CTkLabel(left_panel, text="Tarifa por Hora:").pack(pady=(10, 5), padx=20, anchor="w")
            tarifa_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 5000 (colones)")
            tarifa_entry.pack(pady=(0, 10), padx=20, fill="x")
        else:
            ctk.CTkLabel(left_panel, text="Deducción Extra:").pack(pady=(10, 5), padx=20, anchor="w")
            deduccion_menu = ctk.CTkOptionMenu(left_panel, values=[
                "Seguro privado", "Fondo de Pensiones", "Donacion Opcional",
                "Prestamo privado", "Ahorro", "Embargo", "Pensión alimentaria"
            ])
            deduccion_menu.pack(pady=(0, 10), padx=20, fill="x")
            
            ctk.CTkLabel(left_panel, text="Tipo de Deducción:").pack(pady=(10, 5), padx=20, anchor="w")
            tipo_deduccion_menu = ctk.CTkOptionMenu(left_panel, values=["Voluntaria", "Contrato", "Judicial"])
            tipo_deduccion_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Pila Actual (LIFO):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.stack_display = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b", height=150)
        self.stack_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def push():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return

            seleccion = empleado_menu.get()

            if not seleccion or "No hay empleados" in seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un empleado válido")
                return

            id_emp = seleccion.split(" - ")[-1]
            emp_dict, error = self.data_manager.buscar_por_id(id_emp)

            if error:
                messagebox.showerror("Error", error)
                return

            empleado_obj = self.crear_objeto_empleado(emp_dict)

            try:
                if self.es_pila_horas:
                    horas_str = valor_entry.get()
                    tarifa_str = tarifa_entry.get()

                    if not horas_str or not tarifa_str:
                        messagebox.showwarning("Advertencia", "Completa todos los campos")
                        return

                    horas = float(horas_str)
                    tarifa = float(tarifa_str)

                    if horas < 0 or tarifa <= 0:
                        messagebox.showerror("Error", "Los valores deben ser positivos")
                        return

                    empleado_obj.tarifa_hora = tarifa

                    calculador = obtenerNetoXHoras()
                    resultado = calculador.calcular_y_guardar(empleado_obj, horas, tarifa)

                    # ⭐ CORRECCIÓN: Agregar el resultado a la pila de la vista
                    self.pila.append(resultado)

                    # Actualizar diccionario
                    if empleado_obj.id not in self.main_window.diccionario_calculos:
                        self.main_window.diccionario_calculos[empleado_obj.id] = {}

                    self.main_window.diccionario_calculos[empleado_obj.id]['Bruto por Horas'] = resultado.get('bruto', 0)
                    self.main_window.diccionario_calculos[empleado_obj.id]['Deducciones Normales'] = resultado.get('deducciones normales', 0)

                    valor_entry.delete(0, 'end')
                    tarifa_entry.delete(0, 'end')

                    mensaje_extra = f"Horas: {horas}\nTarifa: ${tarifa:,.2f}"

                else:
                    deduccion_extra = deduccion_menu.get()
                    tipo_deduccion = tipo_deduccion_menu.get()

                    empleado_obj.deduccion_extra = deduccion_extra
                    empleado_obj.tipo_deduccion = tipo_deduccion

                    calculador = calcularNetoXContrato()
                    resultado = calculador.calcular_y_guardar(empleado_obj, deduccion_extra, tipo_deduccion)

                    self.pila.append(resultado)

                    # Actualizar diccionario
                    if empleado_obj.id not in self.main_window.diccionario_calculos:
                        self.main_window.diccionario_calculos[empleado_obj.id] = {}

                    self.main_window.diccionario_calculos[empleado_obj.id]['Deducciones Normales'] = resultado.get('valor deducciones normales', 0)
                    self.main_window.diccionario_calculos[empleado_obj.id]['Otras Deducciones'] = resultado.get('deducciones extra', '')

                    mensaje_extra = f"Deducción: {deduccion_extra}\nTipo: {tipo_deduccion}"

                if not resultado.get('proceso', True):
                    messagebox.showerror("Error", resultado.get('detalle', 'Error desconocido'))
                    return

                self.update_stack_display()

                try:
                    GestionArchivos.guardar_todos_los_datos(
                        self.main_window.cola_cheques,
                        self.main_window.pila_horas,
                        self.main_window.pila_contratos,
                        self.main_window.diccionario_calculos,
                        self.main_window.lista_impresion
                    )
                except Exception as e:
                    print(f"Error al guardar datos: {e}")

                mensaje = f"PUSH - Elemento agregado al tope de la pila\n\n"
                mensaje += f"{empleado_obj.nombre} {empleado_obj.apellido}\n"
                mensaje += mensaje_extra + "\n"
                mensaje += f"Neto calculado: ${resultado.get('neto', 0):,.2f}\n\n"
                mensaje += "La pila internamente usó DICCIONARIOS para:\n"
                if self.es_pila_horas:
                    mensaje += "  • Calcular Bruto por Horas\n"
                    mensaje += "  • Calcular Deducciones Normales"
                else:
                    mensaje += "  • Calcular Deducciones Normales\n"
                    mensaje += "  • Calcular Otras Deducciones"

                messagebox.showinfo("PUSH Exitoso", mensaje)

            except ValueError as ve:
                messagebox.showerror("Error", f"Valor inválido: {str(ve)}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al procesar: {str(e)}")
        
        def pop():
            if not self.pila:
                messagebox.showinfo("Pila Vacía", "No hay elementos en la pila para procesar")
                return

            try:
                # ⭐ CORRECCIÓN: Remover del final de la lista (LIFO)
                procesado = self.pila.pop()  # Esto ya remueve el último elemento

                if procesado:
                    self.update_stack_display()

                    try:
                        GestionArchivos.guardar_todos_los_datos(
                            self.main_window.cola_cheques,
                            self.main_window.pila_horas,
                            self.main_window.pila_contratos,
                            self.main_window.diccionario_calculos,
                            self.main_window.lista_impresion
                        )
                    except Exception as e:
                        print(f"Error al guardar datos: {e}")

                    nombre = procesado.get('nombre', 'Desconocido')
                    neto = procesado.get('neto', 0)

                    messagebox.showinfo("POP Exitoso", 
                        f"POP - Elemento removido del tope\n\n"
                        f"{nombre}\n"
                        f"Neto: ${neto:,.2f}")
                else:
                    messagebox.showinfo("Pila Vacía", "No hay elementos para procesar")

            except Exception as e:
                messagebox.showerror("Error", f"Error al hacer POP: {str(e)}")
        
        def peek():
            if not self.pila:
                messagebox.showinfo("Pila Vacía", "No hay elementos en la pila")
                return

            # ⭐ CORRECCIÓN: Obtener el último elemento sin removerlo
            ultimo = self.pila[-1]
            nombre = ultimo.get('nombre', 'Desconocido')
            neto = ultimo.get('neto', 0)

            info = f"PEEK - Elemento en el tope:\n\n"
            info += f"{nombre}\n"
            info += f"Neto: ${neto:,.2f}\n\n"

            if self.es_pila_horas:
                info += f"Horas: {ultimo.get('horas trabajadas', 0)}\n"
                info += f"Tarifa: ${ultimo.get('tarifa hora', 0):,.2f}"
            else:
                info += f"Contrato: {ultimo.get('tipo contrato', 'N/A')}\n"
                info += f"Salario Base: ${ultimo.get('salario bruto', 0):,.2f}"

            messagebox.showinfo("PEEK", info)
        
        def clear_stack():
            if not self.pila:
                messagebox.showinfo("Pila Vacía", "La pila ya está vacía")
                return
            
            cantidad = len(self.pila)
            respuesta = messagebox.askyesno("Confirmar", f"¿Limpiar {cantidad} elementos de la pila?")
            
            if respuesta:
                self.pila.clear()
                self.update_stack_display()
                
                try:
                    GestionArchivos.guardar_todos_los_datos(
                        self.main_window.cola_cheques,
                        self.main_window.pila_horas,
                        self.main_window.pila_contratos,
                        self.main_window.diccionario_calculos,
                        self.main_window.lista_impresion
                    )
                except Exception as e:
                    print(f"Error al guardar datos: {e}")
                
                messagebox.showinfo("Pila Limpiada", f"Se removieron {cantidad} elementos")
        
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(btn_frame, text="⬆PUSH (Agregar al tope)", command=push, 
                     fg_color="#d97706", hover_color="#b45309", height=40).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="⬇POP (Remover del tope)", command=pop, 
                     fg_color="#3b8ed0", hover_color="#2d6fa3", height=40).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="PEEK (Ver tope)", command=peek, 
                     fg_color="#2fa572", hover_color="#25824f", height=35).pack(fill="x", pady=5)
        ctk.CTkButton(btn_frame, text="Limpiar Pila", command=clear_stack, 
                     fg_color="#6b7280", hover_color="#4b5563", height=35).pack(fill="x", pady=5)
        
        info_frame = ctk.CTkFrame(left_panel, fg_color="#2b2b2b", border_width=2, border_color="#d97706")
        info_frame.pack(pady=10, padx=20, fill="x")
        
        clase_info = "obtenerNetoXHoras" if self.es_pila_horas else "calcularNetoXContrato"
        diccionarios_info = "Bruto por Horas, Deducciones" if self.es_pila_horas else "Deducciones Normales, Otras Deducciones"
        
        info_text = f"ℹEstructura: Pila (LIFO)\nClase: {clase_info}\nUsa Diccionarios: {diccionarios_info}"
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=9), 
                    text_color="gray", justify="left").pack(padx=10, pady=10)
        
        self.update_stack_display()
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Pila (LIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        clase_usada = "obtenerNetoXHoras" if self.es_pila_horas else "calcularNetoXContrato"
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text=f"LIFO: Last In, First Out\nEl último elemento agregado será el primero en procesarse\n✓ Usa: {clase_usada}",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.display_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_display()
    
    def update_stack_display(self):
        for widget in self.stack_display.winfo_children():
            widget.destroy()
        
        if not self.pila:
            ctk.CTkLabel(self.stack_display, text="Pila vacía", text_color="gray", 
                        font=ctk.CTkFont(size=11)).pack(pady=10)
        else:
            for idx, item in enumerate(reversed(self.pila[-5:])):
                pos = len(self.pila) - idx
                nombre = item.get('nombre', 'N/A')
                neto = item.get('neto', 0)
                texto = f"[{pos}] {nombre} - ${neto:,.2f}"
                color = "#d97706" if idx == 0 else "gray"
                peso = "bold" if idx == 0 else "normal"
                ctk.CTkLabel(self.stack_display, text=texto, text_color=color, 
                           font=ctk.CTkFont(size=10, weight=peso)).pack(anchor="w", padx=5, pady=2)
            
            if len(self.pila) > 5:
                ctk.CTkLabel(self.stack_display, text=f"... {len(self.pila) - 5} elementos abajo", 
                           text_color="gray", font=ctk.CTkFont(size=9)).pack(anchor="w", padx=5, pady=2)
        if hasattr(self, 'display_frame'):
            self.update_display()
    
    def update_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if not self.pila:
            ctk.CTkLabel(self.display_frame, text="Pila vacía\n\nAgrega elementos para comenzar", 
                        text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            for idx, item in enumerate(reversed(self.pila)):
                pos_real = len(self.pila) - idx
                
                item_frame = ctk.CTkFrame(self.display_frame, fg_color="#1a1a1a", 
                                         border_width=2, border_color="#d97706" if idx == 0 else "#3b3b3b")
                item_frame.pack(fill="x", pady=8, padx=5)
                
                position_text = "TOPE DE LA PILA" if idx == 0 else f"Posición #{pos_real}"
                position_color = "#d97706" if idx == 0 else "gray"
                
                header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                
                ctk.CTkLabel(header_frame, text=position_text, text_color=position_color, 
                           font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
                
                info_text = f"{item.get('nombre', 'N/A')}\n"
                info_text += f"ID: {item.get('id', 'N/A')}\n"
                
                if self.es_pila_horas:
                    info_text += f"Horas: {item.get('horas trabajadas', 0)}\n"
                    info_text += f"Tarifa/hora: ${item.get('tarifa hora', 0):,.2f}\n"
                    info_text += f"Bruto: ${item.get('bruto', 0):,.2f}\n"
                    info_text += f"Bono: {item.get('bono departamento', 0)*100}%\n"
                    info_text += f"Bruto + Bono: ${item.get('bruto con bono', 0):,.2f}\n"
                else:
                    info_text += f"Contrato: {item.get('tipo contrato', 'N/A')}\n"
                    info_text += f"Salario Base: ${item.get('salario bruto', 0):,.2f}\n"
                    info_text += f"Ajuste: ${item.get('ajuste', 0):,.2f}\n"
                
                info_text += f"Deducciones: ${item.get('valor deducciones normales', item.get('deducciones normales', 0)):,.2f}\n"
                info_text += f"Neto Final: ${item.get('neto', 0):,.2f}"
                
                ctk.CTkLabel(item_frame, text=info_text, text_color="lightgray", 
                           justify="left", font=ctk.CTkFont(size=10)).pack(anchor="w", padx=15, pady=(5, 15))