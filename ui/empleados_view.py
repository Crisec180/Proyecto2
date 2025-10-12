import customtkinter as ctk
from tkinter import messagebox

class EmpleadosView:
    """Vista para la gestión de empleados con Merge Sort y Binary Search"""
    
    def __init__(self, parent, data_manager):
        self.parent = parent
        self.data_manager = data_manager
    
    def render(self):
        """Renderiza la vista de empleados"""
        self.create_header()
        self.create_search_and_sort_controls()
        self.create_table()
    
    def create_header(self):
        """Crea el encabezado de la vista"""
        header_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Gestión de Empleados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Visualización de todos los empleados cargados",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle_label.pack(anchor="w")
    
    def create_search_and_sort_controls(self):
        """Crea los controles de búsqueda y ordenamiento"""
        # Frame de búsqueda
        search_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", pady=20)
        search_frame.grid_columnconfigure(1, weight=1)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar empleado (Nombre/Apellido/ID)...",
            height=40
        )
        self.search_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        
        # Frame de botones de ordenamiento
        sort_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        sort_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        sort_frame.grid_columnconfigure(4, weight=1)
        
        ctk.CTkLabel(sort_frame, text="Ordenar por:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=(0, 10)
        )
        
        sort_buttons = [
            ("Nombre", 'nombre'),
            ("Apellido", 'apellido'),
            ("ID", 'id')
        ]
        
        for i, (text, campo) in enumerate(sort_buttons):
            ctk.CTkButton(
                sort_frame,
                text=text,
                command=lambda c=campo: self.ordenar(c),
                width=100,
                fg_color="#2fa572",
                hover_color="#25824f",
                font=ctk.CTkFont(size=12)
            ).grid(row=0, column=i+1, padx=5)
        
        ctk.CTkButton(
            sort_frame,
            text="🔍 Buscar (Binary Search)",
            command=self.buscar,
            width=150,
            fg_color="#3b8ed0",
            hover_color="#2d6fa3",
            font=ctk.CTkFont(size=12)
        ).grid(row=0, column=4, padx=5, sticky="e")
    
    def create_table(self):
        """Crea la tabla de empleados"""
        table_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        table_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 20))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        scrollable = ctk.CTkScrollableFrame(table_frame, fg_color="#2b2b2b")
        scrollable.grid(row=0, column=0, sticky="nsew")
        scrollable.grid_columnconfigure(0, weight=1)
        
        empleados = self.data_manager.obtener_empleados()
        
        if empleados:
            headers = list(empleados[0].keys())
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    scrollable,
                    text=header.upper(),
                    font=ctk.CTkFont(weight="bold"),
                    fg_color="#1a1a1a",
                    corner_radius=5
                )
                label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            for row_idx, empleado in enumerate(empleados, 1):
                for col_idx, value in enumerate(empleado.values()):
                    label = ctk.CTkLabel(
                        scrollable,
                        text=str(value),
                        fg_color="#2b2b2b" if row_idx % 2 == 0 else "#1a1a1a"
                    )
                    label.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="ew")
        else:
            no_data = ctk.CTkLabel(
                scrollable,
                text="No hay empleados cargados. Por favor, carga un archivo CSV.",
                text_color="gray"
            )
            no_data.pack(pady=50)
    
    def ordenar(self, campo):
        """Ordena empleados por el campo especificado usando Merge Sort"""
        exito, mensaje = self.data_manager.ordenar_por_campo(campo)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.render()
        else:
            messagebox.showwarning("Advertencia", mensaje)
    
    def buscar(self):
        """Busca un empleado usando Binary Search"""
        valor_busqueda = self.search_entry.get()
        empleado, error = self.data_manager.buscar_por_nombre(valor_busqueda)
        
        if error:
            messagebox.showwarning("Advertencia", error)
        else:
            resultado = f"Empleado encontrado:\n\n"
            for key, value in empleado.items():
                resultado += f"{key.upper()}: {value}\n"
            messagebox.showinfo("Resultado de Búsqueda", resultado)