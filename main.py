import customtkinter as ctk
from tkinter import filedialog, messagebox
import csv

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PayrollSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Nómina - Visualización de Estructuras de Datos")
        self.geometry("1400x850")
        
        # Variables de datos simulados
        self.empleados = []
        self.cola_cheques = []
        self.pila_horas = []
        self.pila_contratos = []
        self.diccionario_calculos = {}
        self.lista_impresion = []
        self.caja_chica_balance = 5000.00
        self.movimientos_caja = []
        
        # Crear el layout principal
        self.create_layout()
        
    def create_layout(self):
        # Frame principal con dos columnas
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar izquierdo
        self.create_sidebar()
        
        # Frame principal derecho
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Mostrar vista inicial
        self.show_dashboard()
        
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        # Logo/Título
        logo_label = ctk.CTkLabel(
            sidebar, 
            text="💼 Sistema de Nómina", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#3b8ed0"
        )
        logo_label.pack(pady=30, padx=20)
        
        # Botón cargar CSV
        self.load_csv_btn = ctk.CTkButton(
            sidebar,
            text="📂 Cargar CSV",
            command=self.load_csv,
            fg_color="#2b2b2b",
            hover_color="#3b3b3b"
        )
        self.load_csv_btn.pack(pady=10, padx=20, fill="x")
        
        # Separador
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#3b3b3b")
        separator.pack(pady=20, padx=20, fill="x")
        
        # Botones de navegación
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("👥 Empleados", self.show_empleados),
            ("📋 Cola: Calcular Neto", self.show_cola_neto),
            ("📚 Pila: Neto por Horas", self.show_pila_horas),
            ("📚 Pila: Neto Contrato", self.show_pila_contratos),
            ("📖 Diccionario: Cálculos", self.show_diccionario),
            ("📄 Lista: Imprimir Cheques", self.show_lista_cheques),
            ("💰 Caja Chica", self.show_caja_chica),
            ("💵 Procesar Pagos", self.show_procesar_pagos)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color="#2b2b2b",
                anchor="w",
                height=40
            )
            btn.pack(pady=5, padx=20, fill="x")
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def create_header(self, title, subtitle=""):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(anchor="w")
        
        if subtitle:
            subtitle_label = ctk.CTkLabel(
                header_frame,
                text=subtitle,
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            subtitle_label.pack(anchor="w")
    
    def load_csv(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    self.empleados = list(csv_reader)
                
                messagebox.showinfo("Éxito", f"Se cargaron {len(self.empleados)} empleados correctamente")
                self.show_dashboard()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
    
    def show_dashboard(self):
        self.clear_main_frame()
        self.create_header("Dashboard", "Resumen general del sistema")
        
        # Contenedor de tarjetas
        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.grid(row=1, column=0, sticky="nsew")
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Tarjetas de estadísticas
        stats = [
            ("👥 Empleados", str(len(self.empleados)), "#3b8ed0"),
            ("📋 Cola Cheques", str(len(self.cola_cheques)), "#2fa572"),
            ("📚 Pila Activa", str(len(self.pila_horas)), "#d97706"),
            ("📖 Diccionario", str(len(self.diccionario_calculos)), "#dc2626")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = self.create_stat_card(cards_frame, label, value, color)
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        
        # Área de visualización
        viz_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a")
        viz_frame.grid(row=2, column=0, sticky="nsew", pady=20)
        viz_frame.grid_rowconfigure(0, weight=1)
        
        info_label = ctk.CTkLabel(
            viz_frame,
            text="Bienvenido al Sistema de Nómina\n\nSelecciona una opción del menú para visualizar las estructuras de datos",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        info_label.pack(expand=True, pady=50)
    
    def create_stat_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        title_label.pack(pady=(20, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(5, 20))
        
        return card
    
    def show_empleados(self):
        self.clear_main_frame()
        self.create_header("Gestión de Empleados", "Visualización de todos los empleados cargados")
        
        # Frame de contenido
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a1a")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Barra de búsqueda
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar empleado...",
            height=40,
            width=400
        )
        search_entry.pack(side="left", padx=(0, 10))
        
        add_btn = ctk.CTkButton(
            search_frame,
            text="+ Agregar Empleado",
            height=40,
            fg_color="#2fa572",
            hover_color="#25824f"
        )
        add_btn.pack(side="left")
        
        # Tabla de empleados
        table_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        table_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # ScrollableFrame para la tabla
        scrollable = ctk.CTkScrollableFrame(table_frame, fg_color="#2b2b2b")
        scrollable.pack(fill="both", expand=True)
        
        if self.empleados:
            # Encabezados
            headers = list(self.empleados[0].keys())
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    scrollable,
                    text=header,
                    font=ctk.CTkFont(weight="bold"),
                    fg_color="#1a1a1a",
                    corner_radius=5
                )
                label.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            
            # Datos
            for row_idx, empleado in enumerate(self.empleados, 1):
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
    
    def show_cola_neto(self):
        self.clear_main_frame()
        self.create_header("Cola: Calcular Neto Empleado", "Visualización de la cola de procesamiento de cheques")
        
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo - Controles
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar a la Cola", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="ID Empleado:").pack(pady=(10, 5), padx=20, anchor="w")
        id_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: EMP001")
        id_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Monto:").pack(pady=(10, 5), padx=20, anchor="w")
        monto_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 1500.00")
        monto_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        # Panel derecho - Visualización de la cola
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Cola (FIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        queue_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        queue_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def update_queue_display():
            for widget in queue_frame.winfo_children():
                widget.destroy()
            
            if not self.cola_cheques:
                ctk.CTkLabel(queue_frame, text="Cola vacía", text_color="gray").pack(pady=20)
            else:
                for idx, item in enumerate(self.cola_cheques):
                    item_frame = ctk.CTkFrame(queue_frame, fg_color="#1a1a1a")
                    item_frame.pack(fill="x", pady=5, padx=5)
                    
                    position = "← SIGUIENTE" if idx == 0 else f"Posición {idx}"
                    color = "#2fa572" if idx == 0 else "gray"
                    
                    ctk.CTkLabel(
                        item_frame,
                        text=f"{position}: {item}",
                        text_color=color
                    ).pack(side="left", padx=10, pady=10)
        
        def enqueue_item():
            id_emp = id_entry.get()
            monto = monto_entry.get()
            if id_emp and monto:
                self.cola_cheques.append(f"{id_emp}: ${monto}")
                update_queue_display()
                id_entry.delete(0, 'end')
                monto_entry.delete(0, 'end')
        
        def dequeue_item():
            if self.cola_cheques:
                self.cola_cheques.pop(0)
                update_queue_display()
        
        ctk.CTkButton(
            left_panel,
            text="➕ Agregar a Cola (ENQUEUE)",
            command=enqueue_item,
            fg_color="#2fa572",
            hover_color="#25824f"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            left_panel,
            text="✅ Procesar Primero (DEQUEUE)",
            command=dequeue_item,
            fg_color="#3b8ed0",
            hover_color="#2d6fa3"
        ).pack(pady=10, padx=20, fill="x")
        
        update_queue_display()
    
    def show_pila_horas(self):
        self.clear_main_frame()
        self.create_header("Pila: Obtener Neto por Horas", "Visualización de la pila para cálculo de neto por horas")
        self.create_stack_view("horas", self.pila_horas, "Horas trabajadas")
    
    def show_pila_contratos(self):
        self.clear_main_frame()
        self.create_header("Pila: Calcular Neto por Contrato", "Visualización de la pila para cálculo de neto por contrato")
        self.create_stack_view("contratos", self.pila_contratos, "Contratos")
    
    def create_stack_view(self, tipo, pila, label_text):
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text=f"Agregar a la Pila", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="ID Empleado:").pack(pady=(10, 5), padx=20, anchor="w")
        id_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: EMP001")
        id_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text=f"{label_text}:").pack(pady=(10, 5), padx=20, anchor="w")
        data_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 160")
        data_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        # Panel derecho
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Pila (LIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        stack_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        stack_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def update_stack_display():
            for widget in stack_frame.winfo_children():
                widget.destroy()
            
            if not pila:
                ctk.CTkLabel(stack_frame, text="Pila vacía", text_color="gray").pack(pady=20)
            else:
                for idx, item in enumerate(reversed(pila)):
                    item_frame = ctk.CTkFrame(stack_frame, fg_color="#1a1a1a")
                    item_frame.pack(fill="x", pady=5, padx=5)
                    
                    position = "← TOPE" if idx == 0 else f"Nivel {len(pila) - idx}"
                    color = "#d97706" if idx == 0 else "gray"
                    
                    ctk.CTkLabel(
                        item_frame,
                        text=f"{position}: {item}",
                        text_color=color
                    ).pack(side="left", padx=10, pady=10)
        
        def push_item():
            id_emp = id_entry.get()
            data = data_entry.get()
            if id_emp and data:
                pila.append(f"{id_emp}: {data}")
                update_stack_display()
                id_entry.delete(0, 'end')
                data_entry.delete(0, 'end')
        
        def pop_item():
            if pila:
                pila.pop()
                update_stack_display()
        
        ctk.CTkButton(
            left_panel,
            text="⬆️ Agregar a Pila (PUSH)",
            command=push_item,
            fg_color="#d97706",
            hover_color="#b45309"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            left_panel,
            text="⬇️ Sacar de Pila (POP)",
            command=pop_item,
            fg_color="#dc2626",
            hover_color="#b91c1c"
        ).pack(pady=10, padx=20, fill="x")
        
        update_stack_display()
    
    def show_diccionario(self):
        self.clear_main_frame()
        self.create_header("Diccionario: Cálculos Varios", "Gestión de cálculos con estructura de diccionario")
        
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Agregar al Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        ctk.CTkLabel(left_panel, text="Clave (ID):").pack(pady=(10, 5), padx=20, anchor="w")
        key_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: EMP001")
        key_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Tipo de Cálculo:").pack(pady=(10, 5), padx=20, anchor="w")
        tipo_menu = ctk.CTkOptionMenu(
            left_panel,
            values=["Bruto por Horas", "Deducciones Normales", "Otras Deducciones"]
        )
        tipo_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Valor:").pack(pady=(10, 5), padx=20, anchor="w")
        value_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 2500.00")
        value_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        # Panel derecho
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización del Diccionario", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        dict_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        dict_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def update_dict_display():
            for widget in dict_frame.winfo_children():
                widget.destroy()
            
            if not self.diccionario_calculos:
                ctk.CTkLabel(dict_frame, text="Diccionario vacío", text_color="gray").pack(pady=20)
            else:
                for key, values in self.diccionario_calculos.items():
                    key_frame = ctk.CTkFrame(dict_frame, fg_color="#1a1a1a", border_width=2, border_color="#dc2626")
                    key_frame.pack(fill="x", pady=10, padx=5)
                    
                    ctk.CTkLabel(
                        key_frame,
                        text=f"🔑 {key}",
                        font=ctk.CTkFont(weight="bold"),
                        text_color="#dc2626"
                    ).pack(anchor="w", padx=10, pady=(10, 5))
                    
                    for subkey, subvalue in values.items():
                        ctk.CTkLabel(
                            key_frame,
                            text=f"  • {subkey}: {subvalue}",
                            text_color="gray"
                        ).pack(anchor="w", padx=20, pady=2)
                    
                    ctk.CTkLabel(key_frame, text="").pack(pady=5)
        
        def add_to_dict():
            key = key_entry.get()
            tipo = tipo_menu.get()
            value = value_entry.get()
            if key and value:
                if key not in self.diccionario_calculos:
                    self.diccionario_calculos[key] = {}
                self.diccionario_calculos[key][tipo] = value
                update_dict_display()
                key_entry.delete(0, 'end')
                value_entry.delete(0, 'end')
        
        def remove_from_dict():
            key = key_entry.get()
            if key in self.diccionario_calculos:
                del self.diccionario_calculos[key]
                update_dict_display()
                key_entry.delete(0, 'end')
        
        ctk.CTkButton(
            left_panel,
            text="➕ Agregar/Actualizar",
            command=add_to_dict,
            fg_color="#dc2626",
            hover_color="#b91c1c"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            left_panel,
            text="🗑️ Eliminar Clave",
            command=remove_from_dict,
            fg_color="#6b7280",
            hover_color="#4b5563"
        ).pack(pady=10, padx=20, fill="x")
        
        update_dict_display()
    
    def show_lista_cheques(self):
        self.clear_main_frame()
        self.create_header("Lista/Tupla: Imprimir Cheques", "Gestión de impresión de cheques")
        
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
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
        
        # Panel derecho
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Lista de Cheques", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        list_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        def update_list_display():
            for widget in list_frame.winfo_children():
                widget.destroy()
            
            if not self.lista_impresion:
                ctk.CTkLabel(list_frame, text="No hay cheques en la lista", text_color="gray").pack(pady=20)
            else:
                for idx, (id_emp, nombre, monto) in enumerate(self.lista_impresion, 1):
                    cheque_frame = ctk.CTkFrame(list_frame, fg_color="#1a1a1a", border_width=2, border_color="#2fa572")
                    cheque_frame.pack(fill="x", pady=10, padx=5)
                    
                    ctk.CTkLabel(
                        cheque_frame,
                        text=f"📄 Cheque #{idx}",
                        font=ctk.CTkFont(weight="bold"),
                        text_color="#2fa572"
                    ).pack(anchor="w", padx=15, pady=(15, 5))
                    
                    info_text = f"ID: {id_emp}\nNombre: {nombre}\nMonto: ${monto}"
                    ctk.CTkLabel(
                        cheque_frame,
                        text=info_text,
                        text_color="lightgray",
                        justify="left"
                    ).pack(anchor="w", padx=15, pady=(5, 15))
        
        def add_to_list():
            id_emp = id_entry.get()
            nombre = nombre_entry.get()
            monto = monto_entry.get()
            if id_emp and nombre and monto:
                self.lista_impresion.append((id_emp, nombre, monto))
                update_list_display()
                id_entry.delete(0, 'end')
                nombre_entry.delete(0, 'end')
                monto_entry.delete(0, 'end')
        
        def clear_list():
            self.lista_impresion.clear()
            update_list_display()
        
        ctk.CTkButton(
            left_panel,
            text="➕ Agregar a Lista",
            command=add_to_list,
            fg_color="#2fa572",
            hover_color="#25824f"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            left_panel,
            text="🖨️ Imprimir Todos",
            fg_color="#3b8ed0",
            hover_color="#2d6fa3"
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            left_panel,
            text="🗑️ Limpiar Lista",
            command=clear_list,
            fg_color="#6b7280",
            hover_color="#4b5563"
        ).pack(pady=10, padx=20, fill="x")
        
        update_list_display()
    
    def show_caja_chica(self):
        self.clear_main_frame()
        self.create_header("Gestión de Caja Chica", "Administración de viáticos y gastos menores")
        
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo - Balance y Recarga
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Balance actual
        balance_frame = ctk.CTkFrame(left_panel, fg_color="#2b2b2b")
        balance_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            balance_frame,
            text="Balance Actual",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(pady=(15, 5))
        
        balance_label = ctk.CTkLabel(
            balance_frame,
            text=f"${self.caja_chica_balance:,.2f}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#2fa572"
        )
        balance_label.pack(pady=(5, 15))
        
        # Departamentos
        ctk.CTkLabel(
            left_panel,
            text="Seleccionar Departamento",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(20, 10), padx=20, anchor="w")
        
        dept_menu = ctk.CTkOptionMenu(
            left_panel,
            values=["Administración", "Ingeniería", "Recursos Humanos", "Ventas"]
        )
        dept_menu.pack(pady=(0, 20), padx=20, fill="x")
        
        # Recargar caja
        ctk.CTkLabel(left_panel, text="Monto a Recargar:").pack(pady=(10, 5), padx=20, anchor="w")
        recarga_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 1000.00")
        recarga_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        def recargar_caja():
            try:
                monto = float(recarga_entry.get())
                self.caja_chica_balance += monto
                balance_label.configure(text=f"${self.caja_chica_balance:,.2f}")
                self.movimientos_caja.append(f"Recarga: +${monto:.2f}")
                update_historial()
                recarga_entry.delete(0, 'end')
                messagebox.showinfo("Éxito", f"Se recargaron ${monto:.2f} a la caja chica")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")
        
        ctk.CTkButton(
            left_panel,
            text="💰 Recargar Caja Chica",
            command=recargar_caja,
            fg_color="#2fa572",
            hover_color="#25824f",
            height=40
        ).pack(pady=10, padx=20, fill="x")
        
        # Panel derecho - Registro de Viáticos
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            right_panel,
            text="Registrar Pago de Viáticos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20, padx=20, anchor="w")
        
        form_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(form_frame, text="ID Empleado:").pack(pady=(20, 5), padx=20, anchor="w")
        emp_id_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: EMP001")
        emp_id_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(form_frame, text="Concepto:").pack(pady=(10, 5), padx=20, anchor="w")
        concepto_menu = ctk.CTkOptionMenu(
            form_frame,
            values=["Horas Extra", "Transporte", "Alimentación", "Otros Gastos"]
        )
        concepto_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(form_frame, text="Monto:").pack(pady=(10, 5), padx=20, anchor="w")
        monto_viatico_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: 250.00")
        monto_viatico_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(form_frame, text="Descripción:").pack(pady=(10, 5), padx=20, anchor="w")
        desc_text = ctk.CTkTextbox(form_frame, height=100)
        desc_text.pack(pady=(0, 10), padx=20, fill="x")
        
        def registrar_viatico():
            try:
                emp_id = emp_id_entry.get()
                concepto = concepto_menu.get()
                monto = float(monto_viatico_entry.get())
                
                if emp_id and monto > 0:
                    if monto <= self.caja_chica_balance:
                        self.caja_chica_balance -= monto
                        balance_label.configure(text=f"${self.caja_chica_balance:,.2f}")
                        self.movimientos_caja.append(f"{emp_id} - {concepto}: -${monto:.2f}")
                        update_historial()
                        emp_id_entry.delete(0, 'end')
                        monto_viatico_entry.delete(0, 'end')
                        desc_text.delete("1.0", "end")
                        messagebox.showinfo("Éxito", f"Viático registrado: ${monto:.2f}")
                    else:
                        messagebox.showerror("Error", "Saldo insuficiente en caja chica")
                else:
                    messagebox.showwarning("Advertencia", "Complete todos los campos")
            except ValueError:
                messagebox.showerror("Error", "Ingrese un monto válido")
        
        ctk.CTkButton(
            form_frame,
            text="✅ Registrar Viático",
            command=registrar_viatico,
            fg_color="#3b8ed0",
            hover_color="#2d6fa3",
            height=40
        ).pack(pady=20, padx=20, fill="x")
        
        # Historial
        ctk.CTkLabel(
            form_frame,
            text="Últimos Movimientos",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 10), padx=20, anchor="w")
        
        historial_frame = ctk.CTkScrollableFrame(form_frame, height=150, fg_color="#1a1a1a")
        historial_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        def update_historial():
            for widget in historial_frame.winfo_children():
                widget.destroy()
            
            if not self.movimientos_caja:
                ctk.CTkLabel(historial_frame, text="No hay movimientos", text_color="gray").pack(pady=10)
            else:
                for mov in reversed(self.movimientos_caja[-10:]):
                    mov_frame = ctk.CTkFrame(historial_frame, fg_color="#2b2b2b")
                    mov_frame.pack(fill="x", pady=5)
                    
                    ctk.CTkLabel(
                        mov_frame,
                        text=mov,
                        text_color="lightgray"
                    ).pack(side="left", padx=10, pady=8)
        
        update_historial()
    
    def show_procesar_pagos(self):
        self.clear_main_frame()
        self.create_header("Procesamiento de Pagos", "Gestión de pagos semanales, quincenales y mensuales")
        
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Panel superior - Filtros
        filter_frame = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        filter_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        ctk.CTkLabel(filter_frame, text="Tipo de Pago:").grid(row=0, column=0, padx=10, pady=20, sticky="w")
        tipo_pago = ctk.CTkOptionMenu(
            filter_frame,
            values=["Todos", "Semanal", "Quincenal", "Mensual"]
        )
        tipo_pago.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        ctk.CTkLabel(filter_frame, text="Departamento:").grid(row=0, column=2, padx=10, pady=20, sticky="w")
        dept_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["Todos", "Administración", "Ingeniería", "Ventas", "RRHH"]
        )
        dept_filter.grid(row=0, column=3, padx=10, pady=20, sticky="ew")
        
        # Panel de empleados y pagos
        main_content = ctk.CTkFrame(content_frame, fg_color="transparent")
        main_content.grid(row=1, column=0, sticky="nsew")
        main_content.grid_columnconfigure((0, 1), weight=1)
        main_content.grid_rowconfigure(0, weight=1)
        
        # Lista de empleados pendientes
        left_panel = ctk.CTkFrame(main_content, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(
            left_panel,
            text="Empleados Pendientes de Pago",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20, padx=20, anchor="w")
        
        empleados_frame = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b")
        empleados_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Empleados de ejemplo
        empleados_pendientes = [
            ("EMP001", "Juan Pérez", "Quincenal", "$2,500.00"),
            ("EMP002", "María García", "Semanal", "$800.00"),
            ("EMP003", "Carlos López", "Mensual", "$4,200.00"),
            ("EMP004", "Ana Martínez", "Quincenal", "$2,800.00"),
            ("EMP005", "Luis Rodríguez", "Semanal", "$750.00")
        ]
        
        for emp_id, nombre, tipo, monto in empleados_pendientes:
            emp_frame = ctk.CTkFrame(empleados_frame, fg_color="#1a1a1a")
            emp_frame.pack(fill="x", pady=8, padx=5)
            
            info_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            ctk.CTkLabel(
                info_frame,
                text=f"{nombre} ({emp_id})",
                font=ctk.CTkFont(weight="bold"),
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{tipo} - {monto}",
                text_color="gray",
                anchor="w"
            ).pack(fill="x")
            
            btn_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            btn_frame.pack(side="right", padx=10)
            
            ctk.CTkButton(
                btn_frame,
                text="✓",
                width=40,
                fg_color="#2fa572",
                hover_color="#25824f"
            ).pack(side="left", padx=5)
            
            ctk.CTkButton(
                btn_frame,
                text="👁",
                width=40,
                fg_color="#3b8ed0",
                hover_color="#2d6fa3"
            ).pack(side="left", padx=5)
        
        # Panel derecho - Resumen y acciones
        right_panel = ctk.CTkFrame(main_content, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(
            right_panel,
            text="Resumen de Pagos",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=20, padx=20, anchor="w")
        
        # Tarjetas de resumen
        summary_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        stats_data = [
            ("Total a Pagar", "$11,050.00", "#2fa572"),
            ("Empleados", "5", "#3b8ed0"),
            ("Promedio", "$2,210.00", "#d97706")
        ]
        
        for label, value, color in stats_data:
            stat_frame = ctk.CTkFrame(summary_frame, fg_color="#2b2b2b")
            stat_frame.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                stat_frame,
                text=label,
                text_color="gray",
                font=ctk.CTkFont(size=12)
            ).pack(pady=(10, 2), padx=15, anchor="w")
            
            ctk.CTkLabel(
                stat_frame,
                text=value,
                text_color=color,
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=(2, 10), padx=15, anchor="w")
        
        # Botones de acción
        action_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b")
        action_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            action_frame,
            text="Acciones Disponibles",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, anchor="w")
        
        ctk.CTkButton(
            action_frame,
            text="💳 Procesar Todos los Pagos",
            fg_color="#2fa572",
            hover_color="#25824f",
            height=50,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            action_frame,
            text="📊 Generar Reporte",
            fg_color="#3b8ed0",
            hover_color="#2d6fa3",
            height=40
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            action_frame,
            text="📧 Enviar Notificaciones",
            fg_color="#d97706",
            hover_color="#b45309",
            height=40
        ).pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(
            action_frame,
            text="💾 Exportar Lista",
            fg_color="#6b7280",
            hover_color="#4b5563",
            height=40
        ).pack(pady=10, padx=20, fill="x")
        
        # Información adicional
        info_frame = ctk.CTkFrame(action_frame, fg_color="#1a1a1a", border_width=2, border_color="#3b8ed0")
        info_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            info_frame,
            text="ℹ️ Información",
            font=ctk.CTkFont(weight="bold"),
            text_color="#3b8ed0"
        ).pack(pady=(10, 5), padx=15, anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text="Los pagos se procesarán según el\ntipo de nómina configurado para\ncada empleado en el CSV.",
            text_color="gray",
            justify="left"
        ).pack(pady=(5, 10), padx=15, anchor="w")

if __name__ == "__main__":
    app = PayrollSystem()
    app.mainloop()