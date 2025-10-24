import customtkinter as ctk
from tkinter import messagebox

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
        
        subtitle = ctk.CTkLabel(header_frame, text="Gestión de cálculos con estructura de diccionario", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"✓ Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#dc2626"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar al Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
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
        
        ctk.CTkLabel(left_panel, text="Tipo de Cálculo:").pack(pady=(10, 5), padx=20, anchor="w")
        tipo_menu = ctk.CTkOptionMenu(left_panel, values=["Bruto por Horas", "Deducciones Normales", "Otras Deducciones", "Bonificaciones", "Impuestos"])
        tipo_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Valor:").pack(pady=(10, 5), padx=20, anchor="w")
        value_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 2500.00")
        value_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        def add():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = key_menu.get()
            tipo = tipo_menu.get()
            value = value_entry.get()
            
            if seleccion and value and "No hay empleados" not in seleccion:
                try:
                    float(value)
                    key = seleccion.split(" - ")[0]
                    
                    if key not in self.diccionario:
                        self.diccionario[key] = {}
                    self.diccionario[key][tipo] = value
                    self.update_dict_display()
                    
                    self.main_window.guardar_estado_completo()
                    
                    value_entry.delete(0, 'end')
                    messagebox.showinfo("Éxito", f"Cálculo agregado al diccionario para {key}")
                except ValueError:
                    messagebox.showerror("Error", "El valor debe ser un número válido")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
        
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
                        
                        self.main_window.guardar_estado_completo()
                        
                        messagebox.showinfo("Éxito", f"Cálculos eliminados para {key}")
                else:
                    messagebox.showinfo("No Encontrado", f"No hay cálculos para {key}")
        
        ctk.CTkButton(left_panel, text="➕ Agregar/Actualizar", command=add, fg_color="#dc2626", hover_color="#b91c1c").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Eliminar Empleado", command=remove, fg_color="#6b7280", hover_color="#4b5563").pack(pady=10, padx=20, fill="x")
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización del Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.dict_display = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.dict_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_dict_display()
    
    def update_dict_display(self):
        for widget in self.dict_display.winfo_children():
            widget.destroy()
        
        if not self.diccionario:
            ctk.CTkLabel(self.dict_display, text="Diccionario vacío\n\nAgrega cálculos para comenzar", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
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
                
                ctk.CTkLabel(header_frame, text=f"🔑 {key}", font=ctk.CTkFont(size=12, weight="bold"), text_color="#dc2626").pack(side="left")
                ctk.CTkLabel(header_frame, text=f"👤 {nombre_completo}", font=ctk.CTkFont(size=11), text_color="gray").pack(side="left", padx=10)
                
                for subkey, subvalue in values.items():
                    calc_frame = ctk.CTkFrame(key_frame, fg_color="#2b2b2b")
                    calc_frame.pack(fill="x", padx=15, pady=3)
                    
                    ctk.CTkLabel(calc_frame, text=f"• {subkey}:", text_color="lightgray", font=ctk.CTkFont(size=11)).pack(side="left", padx=10, pady=5)
                    ctk.CTkLabel(calc_frame, text=f"${float(subvalue):,.2f}", text_color="#2fa572", font=ctk.CTkFont(size=11, weight="bold")).pack(side="right", padx=10, pady=5)
                
                ctk.CTkLabel(key_frame, text="").pack(pady=5)