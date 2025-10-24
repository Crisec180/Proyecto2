import customtkinter as ctk
from tkinter import messagebox

class PilaView:
    
    def __init__(self, parent, pila, titulo, label_text, data_manager, main_window):
        self.parent = parent
        self.pila = pila
        self.titulo = titulo
        self.label_text = label_text
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
        
        title = ctk.CTkLabel(header_frame, text=f"Pila: {self.titulo}", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header_frame, text=f"Visualización de la pila para cálculo de {self.titulo.lower()} (LIFO)", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"✓ Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#d97706"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar a la Pila", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
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
        
        ctk.CTkLabel(left_panel, text=f"{self.label_text}:").pack(pady=(10, 5), padx=20, anchor="w")
        valor_entry = ctk.CTkEntry(left_panel, placeholder_text=f"Ej: {self.get_placeholder()}")
        valor_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Descripción:").pack(pady=(10, 5), padx=20, anchor="w")
        descripcion_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: Horas normales, Horas extra...")
        descripcion_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Pila Actual (LIFO):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.stack_display = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b", height=200)
        self.stack_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def push():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = empleado_menu.get()
            valor = valor_entry.get()
            descripcion = descripcion_entry.get()
            
            if seleccion and valor and "No hay empleados" not in seleccion:
                try:
                    float(valor)
                    id_emp = seleccion.split(" - ")[-1]
                    nombre_emp = seleccion.split(" - ")[0]
                    
                    item_info = {
                        'id': id_emp,
                        'nombre': nombre_emp,
                        'valor': valor,
                        'descripcion': descripcion if descripcion else self.label_text
                    }
                    self.pila.append(item_info)
                    self.update_stack_display()
                    
                    self.main_window.guardar_estado_completo()
                    
                    valor_entry.delete(0, 'end')
                    descripcion_entry.delete(0, 'end')
                    messagebox.showinfo("Éxito", f"Elemento agregado a la pila (PUSH) para {nombre_emp}")
                except ValueError:
                    messagebox.showerror("Error", "El valor debe ser un número válido")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos obligatorios")
        
        def pop():
            if self.pila:
                procesado = self.pila.pop()
                self.update_stack_display()
                
                self.main_window.guardar_estado_completo()
                
                messagebox.showinfo("Procesado", f"Elemento procesado (POP):\n{procesado['nombre']}\nValor: {procesado['valor']}")
            else:
                messagebox.showinfo("Pila Vacía", "No hay elementos en la pila")
        
        def peek():
            if self.pila:
                ultimo = self.pila[-1]
                messagebox.showinfo("PEEK", f"Elemento en el tope:\n{ultimo['nombre']}\nValor: {ultimo['valor']}\nDescripción: {ultimo['descripcion']}")
            else:
                messagebox.showinfo("Pila Vacía", "No hay elementos en la pila")
        
        def clear_stack():
            self.pila.clear()
            self.update_stack_display()
            
            self.main_window.guardar_estado_completo()
            
            messagebox.showinfo("Pila Limpiada", "Todos los elementos fueron removidos")
        
        ctk.CTkButton(left_panel, text="⬆️ PUSH (Agregar al tope)", command=push, fg_color="#d97706", hover_color="#b45309").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="⬇️ POP (Remover del tope)", command=pop, fg_color="#3b8ed0", hover_color="#2d6fa3").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="👁️ PEEK (Ver tope)", command=peek, fg_color="#2fa572", hover_color="#25824f").pack(pady=5, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Limpiar Pila", command=clear_stack, fg_color="#6b7280", hover_color="#4b5563").pack(pady=5, padx=20, fill="x")
        
        self.update_stack_display()
    
    def get_placeholder(self):
        if "Horas" in self.titulo:
            return "40"
        else:
            return "1000.00"
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Pila (LIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text="LIFO: Last In, First Out\nEl último elemento agregado será el primero en procesarse",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="left"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.display_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_display()
    
    def update_stack_display(self):
        for widget in self.stack_display.winfo_children():
            widget.destroy()
        
        if not self.pila:
            ctk.CTkLabel(self.stack_display, text="Pila vacía", text_color="gray", font=ctk.CTkFont(size=11)).pack(pady=10)
        else:
            for idx, item in enumerate(reversed(self.pila[-5:])):
                pos = len(self.pila) - idx
                texto = f"[{pos}] {item['nombre']} - {item['valor']}"
                color = "#d97706" if idx == 0 else "gray"
                peso = "bold" if idx == 0 else "normal"
                ctk.CTkLabel(self.stack_display, text=texto, text_color=color, font=ctk.CTkFont(size=10, weight=peso)).pack(anchor="w", padx=5, pady=2)
            
            if len(self.pila) > 5:
                ctk.CTkLabel(self.stack_display, text=f"... {len(self.pila) - 5} elementos abajo", text_color="gray", font=ctk.CTkFont(size=9)).pack(anchor="w", padx=5, pady=2)
        
        self.update_display()
    
    def update_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
        
        if not self.pila:
            ctk.CTkLabel(self.display_frame, text="Pila vacía\n\nAgrega elementos para comenzar", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
        else:
            for idx, item in enumerate(reversed(self.pila)):
                pos_real = len(self.pila) - idx
                
                item_frame = ctk.CTkFrame(self.display_frame, fg_color="#1a1a1a", border_width=2, border_color="#d97706" if idx == 0 else "#3b3b3b")
                item_frame.pack(fill="x", pady=8, padx=5)
                
                position_text = "🔝 TOPE DE LA PILA" if idx == 0 else f"Posición #{pos_real}"
                position_color = "#d97706" if idx == 0 else "gray"
                
                header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                header_frame.pack(fill="x", padx=10, pady=(10, 5))
                
                ctk.CTkLabel(header_frame, text=position_text, text_color=position_color, font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
                
                info_text = f"👤 {item['nombre']}\n📊 Valor: {item['valor']}\n📝 {item['descripcion']}\n🆔 ID: {item['id']}"
                ctk.CTkLabel(item_frame, text=info_text, text_color="lightgray", justify="left", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=15, pady=(5, 15))