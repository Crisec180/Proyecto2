# ===== lista_view.py =====
import customtkinter as ctk

class ListaView:
    """Vista para la gestión de Lista de Cheques"""
    
    def __init__(self, parent, lista_impresion):
        self.parent = parent
        self.lista_impresion = lista_impresion
    
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
        
        title = ctk.CTkLabel(header_frame, text="Lista/Tupla: Imprimir Cheques", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar Cheque a Lista", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="ID Empleado:").pack(pady=(10, 5), padx=20, anchor="w")
        id_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: EMP001")
        id_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Nombre:").pack(pady=(10, 5), padx=20, anchor="w")
        nombre_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: Juan Pérez")
        nombre_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Monto:").pack(pady=(10, 5), padx=20, anchor="w")
        monto_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 3500.00")
        monto_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        def add():
            id_emp = id_entry.get()
            nombre = nombre_entry.get()
            monto = monto_entry.get()
            if id_emp and nombre and monto:
                self.lista_impresion.append((id_emp, nombre, monto))
                self.update_list_display()
                id_entry.delete(0, 'end')
                nombre_entry.delete(0, 'end')
                monto_entry.delete(0, 'end')
        
        def clear():
            self.lista_impresion.clear()
            self.update_list_display()
        
        ctk.CTkButton(left_panel, text="➕ Agregar a Lista", command=add, fg_color="#2fa572", hover_color="#25824f").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🖨️ Imprimir Todos", fg_color="#3b8ed0", hover_color="#2d6fa3").pack(pady=10, padx=20, fill="x")
        ctk.CTkButton(left_panel, text="🗑️ Limpiar Lista", command=clear, fg_color="#6b7280", hover_color="#4b5563").pack(pady=10, padx=20, fill="x")
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Lista de Cheques", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.list_display = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.list_display.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_list_display()
    
    def update_list_display(self):
        for widget in self.list_display.winfo_children():
            widget.destroy()
        
        if not self.lista_impresion:
            ctk.CTkLabel(self.list_display, text="No hay cheques en la lista", text_color="gray").pack(pady=20)
        else:
            for idx, (id_emp, nombre, monto) in enumerate(self.lista_impresion, 1):
                cheque_frame = ctk.CTkFrame(self.list_display, fg_color="#1a1a1a", border_width=2, border_color="#2fa572")
                cheque_frame.pack(fill="x", pady=10, padx=5)
                
                ctk.CTkLabel(cheque_frame, text=f"📄 Cheque #{idx}", font=ctk.CTkFont(weight="bold"), text_color="#2fa572").pack(anchor="w", padx=15, pady=(15, 5))
                
                info_text = f"ID: {id_emp}\nNombre: {nombre}\nMonto: ${monto}"
                ctk.CTkLabel(cheque_frame, text=info_text, text_color="lightgray", justify="left").pack(anchor="w", padx=15, pady=(5, 15))