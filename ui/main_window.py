import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.data_manager import DataManager
from ui.dashboard_view import DashboardView
from ui.empleados_view import EmpleadosView
from ui.cola_view import ColaView
from ui.pila_view import PilaView
from ui.diccionario_view import DiccionarioView
from ui.lista_view import ListaView
from ui.caja_chica_view import CajaChicaView
from ui.pagos_view import PagosView

class PayrollSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema de Nómina - Visualización de Estructuras de Datos")
        self.geometry("1400x850")
        
        # Inicializar gestores de datos
        self.data_manager = DataManager()
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
        """Crea el layout principal con sidebar y frame principal"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.create_sidebar()
        
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.show_dashboard()
        
    def create_sidebar(self):
        """Crea el sidebar con botones de navegación"""
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#1a1a1a")
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        
        logo_label = ctk.CTkLabel(
            sidebar, 
            text="💼 Sistema de Nómina", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#3b8ed0"
        )
        logo_label.pack(pady=30, padx=20)
        
        self.load_csv_btn = ctk.CTkButton(
            sidebar,
            text="📂 Cargar CSV",
            command=self.load_csv,
            fg_color="#2b2b2b",
            hover_color="#3b3b3b"
        )
        self.load_csv_btn.pack(pady=10, padx=20, fill="x")
        
        separator = ctk.CTkFrame(sidebar, height=2, fg_color="#3b3b3b")
        separator.pack(pady=20, padx=20, fill="x")
        
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
        """Limpia todos los widgets del frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def load_csv(self):
        """Carga un archivo CSV"""
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            exito, mensaje = self.data_manager.cargar_csv(filename)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.show_dashboard()
            else:
                messagebox.showerror("Error", mensaje)
    
    def show_dashboard(self):
        """Muestra la vista del Dashboard"""
        self.clear_main_frame()
        view = DashboardView(self.main_frame, self.data_manager, 
                           len(self.cola_cheques), len(self.pila_horas), 
                           len(self.diccionario_calculos))
        view.render()
    
    def show_empleados(self):
        """Muestra la vista de Gestión de Empleados"""
        self.clear_main_frame()
        view = EmpleadosView(self.main_frame, self.data_manager)
        view.render()
    
    def show_cola_neto(self):
        """Muestra la vista de Cola"""
        self.clear_main_frame()
        view = ColaView(self.main_frame, self.cola_cheques)
        view.render()
    
    def show_pila_horas(self):
        """Muestra la vista de Pila de Horas"""
        self.clear_main_frame()
        view = PilaView(self.main_frame, self.pila_horas, "Neto por Horas", "Horas trabajadas")
        view.render()
    
    def show_pila_contratos(self):
        """Muestra la vista de Pila de Contratos"""
        self.clear_main_frame()
        view = PilaView(self.main_frame, self.pila_contratos, "Neto Contrato", "Contratos")
        view.render()
    
    def show_diccionario(self):
        """Muestra la vista de Diccionario"""
        self.clear_main_frame()
        view = DiccionarioView(self.main_frame, self.diccionario_calculos)
        view.render()
    
    def show_lista_cheques(self):
        """Muestra la vista de Lista de Cheques"""
        self.clear_main_frame()
        view = ListaView(self.main_frame, self.lista_impresion)
        view.render()
    
    def show_caja_chica(self):
        """Muestra la vista de Caja Chica"""
        self.clear_main_frame()
        view = CajaChicaView(self.main_frame, self.caja_chica_balance, self.movimientos_caja)
        view.render()
    
    def show_procesar_pagos(self):
        """Muestra la vista de Procesamiento de Pagos"""
        self.clear_main_frame()
        view = PagosView(self.main_frame)
        view.render()