import customtkinter as ctk
from tkinter import messagebox

class ColaView:
    """Vista para la gestión de Cola (FIFO)"""
    
    def __init__(self, parent, cola_cheques, data_manager):
        self.parent = parent
        self.cola_cheques = cola_cheques
        self.data_manager = data_manager
    
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
        
        title = ctk.CTkLabel(header_frame, text="Cola: Calcular Neto Empleado", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text="Visualización de la cola de procesamiento de cheques (FIFO)", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        # Mostrar empleado seleccionado
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"✓ Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#2fa572"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar a la Cola", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        # Selector de empleado
        ctk.CTkLabel(left_panel, text="Seleccionar Empleado:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(10, 5), padx=20, anchor="w")
        
        empleados = self.data_manager.obtener_empleados()
        if empleados:
            opciones_empleados = [f"{emp.get('nombre', '')} {emp.get('apellido', '')} - {emp.get('id', '')}" for emp in empleados]
            empleado_menu = ctk.CTkOptionMenu(left_panel, values=opciones_empleados)
            empleado_menu.pack(pady=(0, 10), padx=20, fill="x")
            
            # Pre-seleccionar si hay un empleado seleccionado
            empleado_actual = self.data_manager.obtener_empleado_seleccionado()
            if empleado_actual:
                texto_actual = f"{empleado_actual.get('nombre', '')} {empleado_actual.get('apellido', '')} - {empleado_actual.get('id', '')}"
                if texto_actual in opciones_empleados:
                    empleado_menu.set(texto_actual)
        else:
            empleado_menu = ctk.CTkOptionMenu(left_panel, values=["No hay empleados"])
            empleado_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Monto Neto a Calcular:").pack(pady=(10, 5), padx=20, anchor="w")
        monto_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 1500.00")
        monto_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Tipo de Cálculo:").pack(pady=(10, 5), padx=20, anchor="w")
        tipo_menu = ctk.CTkOptionMenu(left_panel, values=["Salario Base", "Horas Extra", "Bonificación"])
        tipo_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        # Vista previa de la cola
        ctk.CTkLabel(left_panel, text="Cola Actual:", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.queue_display = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b", height=200)
        self.queue_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def enqueue():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = empleado_menu.get()
            monto = monto_entry.get()
            tipo = tipo_menu.get()
            
            if seleccion and monto and "No hay empleados" not in seleccion:
                try:
                    float(monto)  # Validar que sea número
                    # Extraer ID del empleado
                    id_emp = seleccion.split(" - ")[-1]
                    nombre_emp = seleccion.split(" - ")[0]
                    
                    cheque_info = {
                        'id': id_emp,
                        'nombre': nombre_emp,
                        'monto': monto,
                        'tipo': tipo
                    }
                    self.cola_cheques.append(cheque_info)
                    self.update_queue_display()
                    monto_entry.delete(0, 'end')
                    messagebox.showinfo("Éxito", f"Cheque agregado a la cola para {nombre_emp}")
                except ValueError:
                    messagebox.showerror("Error", "El monto debe ser un número válido")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
        
        def dequeue():
            if self.cola_cheques:
                procesado = self.cola_cheques.pop(0)
                self.update_queue_display()
                messagebox.showinfo("Procesado", f"Cheque procesado (DEQUEUE):\n{procesado['nombre']}\nMonto: ${procesado['monto']}")
            else:
                messagebox.showinfo("Cola Vacía", "No hay elementos en la cola")
        
        def clear_queue():
            self.cola_cheques.clear()
            self.update_queue_display()
            messagebox.showinfo("Cola Limpiada", "Todos los elementos fueron removidos")
        
        ctk.CTkButton(left_panel, text="➕ ENQUEUE (Agregar)", command=enqueue, fg_color="#2fa572", hover_color="#25824f").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="✅ DEQUEUE (Procesar Primero)", command=dequeue, fg_color="#3b8ed0", hover_color="#2d6fa3").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Limpiar Cola", command=clear_queue, fg_color="#6b7280", hover_color="#4b5563").pack(pady=5, padx=20, fill="x")
        
        self.update_queue_display()
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Cola (FIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text="FIFO: First In, First Out\nEl primer elemento agregado será el primero en procesarse",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.display_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_display()
    
    def update_queue_display(self):
        """Actualiza la vista previa pequeña de la cola"""
        for widget in self.queue_display.winfo_children():
            widget.destroy()
        
        if not self.cola_cheques:
            ctk.CTkLabel(self.queue_display, text="Cola vacía", text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=10)
        else:
            for idx, item in enumerate(self.cola_cheques[:5]):  # Mostrar solo los primeros 5
                texto = f"{idx+1}. {item['nombre']} - ${item['monto']}"
                color = "#2fa572" if idx == 0 else "gray"
                ctk.CTkLabel(self.queue_display, text=texto, text_color=color, font=ctk.CTkFont(size=10)).pack(anchor="w", padx=5, pady=2)
            
            if len(self.cola_cheques) > 5:
                ctk.CTkLabel(self.queue_display, text=f"... y {len(self.cola_cheques) - 5} más", text_color="gray", font=ctk.CTkFont(size=9)).pack(anchor="w", padx=5, pady=2)
        
        self.update_display()
    
    def update_display(self):
        """Actualiza la visualización principal de la cola"""
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if not self.cola_cheques:
            ctk.CTkLabel(self.display_frame, text="Cola vacía\n\nAgrega cheques para comenzar", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            for idx, item in enumerate(self.cola_cheques):
                item_frame = ctk.CTkFrame(self.display_frame, fg_color="#1a1a1a", border_width=2, border_color="#2fa572" if idx == 0 else "#3b3b3b")
                item_frame.pack(fill="x", pady=8, padx=5)
                
                # Header del cheque
                position_text = "⏩ SIGUIENTE EN PROCESAR" if idx == 0 else f"Posición #{idx + 1} en cola"
                position_color = "#2fa572" if idx == 0 else "gray"
                
                header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                
                ctk.CTkLabel(header_frame, text=position_text, text_color=position_color, font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
                
                # Información del cheque
                info_text = f"👤 {item['nombre']}\n💰 Monto: ${item['monto']}\n📋 Tipo: {item['tipo']}\n🆔 ID: {item['id']}"
                ctk.CTkLabel(item_frame, text=info_text, text_color="lightgray", justify="left", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=15, pady=(5, 15))