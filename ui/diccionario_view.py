import customtkinter as ctk

class DiccionarioView:
    """Vista para la gestión de Diccionario"""
    
    def __init__(self, parent, diccionario):
        self.parent = parent
        self.diccionario = diccionario
    
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
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar al Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="Clave (ID):").pack(pady=(10, 5), padx=20, anchor="w")
        key_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: EMP001")
        key_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Tipo de Cálculo:").pack(pady=(10, 5), padx=20, anchor="w")
        tipo_menu = ctk.CTkOptionMenu(left_panel, values=["Bruto por Horas", "Deducciones Normales", "Otras Deducciones"])
        tipo_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Valor:").pack(pady=(10, 5), padx=20, anchor="w")
        value_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 2500.00")
        value_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        def add():
            key = key_entry.get()
            tipo = tipo_menu.get()
            value = value_entry.get()
            if key and value:
                if key not in self.diccionario:
                    self.diccionario[key] = {}
                self.diccionario[key][tipo] = value
                self.update_dict_display()
                key_entry.delete(0, 'end')
                value_entry.delete(0, 'end')
        
        def remove():
            key = key_entry.get()
            if key in self.diccionario:
                del self.diccionario[key]
                self.update_dict_display()
                key_entry.delete(0, 'end')
        
        ctk.CTkButton(left_panel, text="➕ Agregar/Actualizar", command=add, fg_color="#dc2626", hover_color="#b91c1c").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Eliminar Clave", command=remove, fg_color="#6b7280", hover_color="#4b5563").pack(pady=10, padx=20, fill="x")
    
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
            ctk.CTkLabel(self.dict_display, text="Diccionario vacío", text_color="gray").pack(pady=20)
        else:
            for key, values in self.diccionario.items():
                key_frame = ctk.CTkFrame(self.dict_display, fg_color="#1a1a1a", border_width=2, border_color="#dc2626")
                key_frame.pack(fill="x", pady=10, padx=5)
                
                ctk.CTkLabel(key_frame, text=f"🔑 {key}", font=ctk.CTkFont(weight="bold"), text_color="#dc2626").pack(anchor="w", padx=10, pady=(10, 5))
                
                for subkey, subvalue in values.items():
                    ctk.CTkLabel(key_frame, text=f"  • {subkey}: {subvalue}", text_color="gray").pack(anchor="w", padx=20, pady=2)
                
                ctk.CTkLabel(key_frame, text="").pack(pady=5,row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar a la Cola", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="ID Empleado:").pack(pady=(10, 5), padx=20, anchor="w")
        id_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: EMP001")
        id_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Monto:").pack(pady=(10, 5), padx=20, anchor="w")
        monto_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 1500.00")
        monto_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        self.queue_display = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b")
        self.queue_display.pack(fill="both", expand=True, padx=20, pady=10)
        
        def enqueue():
            id_emp = id_entry.get()
            monto = monto_entry.get()
            if id_emp and monto:
                self.cola_cheques.append(f"{id_emp}: ${monto}")
                self.update_queue_display()
                id_entry.delete(0, 'end')
                monto_entry.delete(0, 'end')
        
        def dequeue():
            if self.cola_cheques:
                self.cola_cheques.pop(0)
                self.update_queue_display()
        
        ctk.CTkButton(left_panel, text="➕ ENQUEUE", command=enqueue, fg_color="#2fa572", hover_color="#25824f").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="✅ DEQUEUE", command=dequeue, fg_color="#3b8ed0", hover_color="#2d6fa3").pack(pady=10, padx=20, fill="x")
        
        self.update_queue_display()
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Cola (FIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.display_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def update_queue_display(self):
        for widget in self.queue_display.winfo_children():
            widget.destroy()
        
        if not self.cola_cheques:
            ctk.CTkLabel(self.queue_display, text="Cola vacía", text_color="gray").pack(pady=20)
        else:
            for idx, item in enumerate(self.cola_cheques):
                item_frame = ctk.CTkFrame(self.queue_display, fg_color="#1a1a1a")
                item_frame.pack(fill="x", pady=5, padx=5)
                
                position = "← SIGUIENTE" if idx == 0 else f"Posición {idx}"
                color = "#2fa572" if idx == 0 else "gray"
                
                ctk.CTkLabel(item_frame, text=f"{position}: {item}", text_color=color).pack(side="left", padx=10, pady=10)