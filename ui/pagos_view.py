import customtkinter as ctk

class PagosView:
    """Vista para el Procesamiento de Pagos"""
    
    def __init__(self, parent):
        self.parent = parent
    
    def render(self):
        self.create_header()
        
        content_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        self.create_filter_panel(content_frame)
        self.create_content_panel(content_frame)
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(header_frame, text="Procesamiento de Pagos", font=ctk.CTkFont(size=28, weight="bold"))
        title.pack(anchor="w")
    
    def create_filter_panel(self, parent):
        filter_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        filter_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        ctk.CTkLabel(filter_frame, text="Tipo de Pago:").grid(row=0, column=0, padx=10, pady=20, sticky="w")
        ctk.CTkOptionMenu(filter_frame, values=["Todos", "Semanal", "Quincenal", "Mensual"]).grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        ctk.CTkLabel(filter_frame, text="Departamento:").grid(row=0, column=2, padx=10, pady=20, sticky="w")
        ctk.CTkOptionMenu(filter_frame, values=["Todos", "Administración", "Ingeniería", "Ventas"]).grid(row=0, column=3, padx=10, pady=20, sticky="ew")
    
    def create_content_panel(self, parent):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Empleados Pendientes", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        empleados_frame = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b")
        empleados_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        empleados = [("EMP001", "Juan Pérez", "Quincenal", "$2,500"), ("EMP002", "María García", "Semanal", "$800")]
        
        for emp_id, nombre, tipo, monto in empleados:
            emp_frame = ctk.CTkFrame(empleados_frame, fg_color="#1a1a1a")
            emp_frame.pack(fill="x", pady=8, padx=5)
            
            info_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(info_frame, text=f"{nombre} ({emp_id})", font=ctk.CTkFont(weight="bold"), anchor="w").pack(fill="x")
            ctk.CTkLabel(info_frame, text=f"{tipo} - {monto}", text_color="gray", anchor="w").pack(fill="x")
        
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Resumen de Pagos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        summary_data = [("Total a Pagar", "$3,300.00", "#2fa572"), ("Empleados", "2", "#3b8ed0")]
        
        for label, value, color in summary_data:
            stat_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b")
            stat_frame.pack(fill="x", pady=5, padx=20)
            
            ctk.CTkLabel(stat_frame, text=label, text_color="gray", font=ctk.CTkFont(size=12)).pack(pady=(10, 2), padx=15, anchor="w")
            ctk.CTkLabel(stat_frame, text=value, text_color=color, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(2, 10), padx=15, anchor="w")