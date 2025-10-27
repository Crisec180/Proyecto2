import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from CalculoConCOLAS.CalculaNetoEmpleado import calculaNetoEmpleado
from GestionArchivos import GestionArchivos

class PagosView:
    """Vista para el Procesamiento de Pagos"""
    
    def __init__(self, parent, data_manager, main_window):
        self.parent = parent
        self.data_manager = data_manager
        self.main_window = main_window
        self.empleados_seleccionados = []
        self.cheques_procesados = []  # Lista para almacenar los cheques ya procesados por la cola
    
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
        
        subtitle = ctk.CTkLabel(header_frame, text="Gestión y procesamiento de pagos de nómina", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
    
    def create_filter_panel(self, parent):
        filter_frame = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        filter_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        
        ctk.CTkLabel(filter_frame, text="Filtrar por:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=20, sticky="w")
        
        self.tipo_pago_var = ctk.StringVar(value="Todos")
        tipo_menu = ctk.CTkOptionMenu(
            filter_frame, 
            values=["Todos", "Semanal", "Quincenal", "Mensual"],
            variable=self.tipo_pago_var,
            command=lambda x: self.actualizar_lista()
        )
        tipo_menu.grid(row=0, column=1, padx=10, pady=20, sticky="ew")
        
        # Botón para seleccionar todos
        ctk.CTkButton(
            filter_frame,
            text="✓ Seleccionar Todos",
            command=self.seleccionar_todos,
            fg_color="#2fa572",
            hover_color="#25824f",
            width=120
        ).grid(row=0, column=3, padx=10, pady=20)
        
        ctk.CTkButton(
            filter_frame,
            text="💵 Procesar Seleccionados",
            command=self.procesar_pagos,
            fg_color="#3b8ed0",
            hover_color="#2d6fa3",
            width=150
        ).grid(row=0, column=4, padx=10, pady=20)
    
    def create_content_panel(self, parent):
        content_frame = ctk.CTkFrame(parent, fg_color="transparent")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_columnconfigure((0, 1), weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Panel izquierdo - Lista de empleados
        left_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="Empleados Disponibles", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.empleados_frame = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b")
        self.empleados_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Panel derecho - Resumen
        right_panel = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Resumen de Pagos", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        self.resumen_frame = ctk.CTkFrame(right_panel, fg_color="#2b2b2b")
        self.resumen_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualiza la lista de cheques procesados"""
        # Limpiar frame
        for widget in self.empleados_frame.winfo_children():
            widget.destroy()
        
        # Debug: Mostrar información de las estructuras
        print(f"DEBUG: Cantidad de elementos en pila_horas: {len(self.main_window.pila_horas)}")
        print(f"DEBUG: Cantidad de elementos en pila_contratos: {len(self.main_window.pila_contratos)}")
        
        # Obtener resultados de la cola y las pilas
        self.cheques_procesados = []
        
            # Agregar resultados de pila_horas
        for resultado in self.main_window.pila_horas:
            if isinstance(resultado, dict):
                # Obtener ID del resultado, con manejo de diferentes formatos
                emp_id = resultado.get('Id') or resultado.get('id')
                if not emp_id:
                    continue  # Saltar registros sin ID
                
                # Obtener nombre, con manejo de diferentes formatos
                nombre = resultado.get('Nombre') or resultado.get('nombre')
                if not nombre or nombre == 'N/A':
                    emp_dict, _ = self.data_manager.buscar_por_id(emp_id)
                    if emp_dict:
                        nombre = f"{emp_dict.get('nombre', '')} {emp_dict.get('apellido', '')}".strip()
                
                # Obtener monto neto, con manejo de diferentes formatos
                monto = float(resultado.get('Neto', 0.0))
                if monto > 0:  # Solo agregar si el monto es positivo
                    self.cheques_procesados.append({
                        'id': emp_id,
                        'nombre': nombre,
                        'monto': monto,
                        'tipo': 'Por Horas',
                        'resultado': resultado
                    })
        
        # Agregar resultados de pila_contratos
        for resultado in self.main_window.pila_contratos:
            if isinstance(resultado, dict):
                # Obtener ID del resultado, con manejo de diferentes formatos
                emp_id = resultado.get('Id') or resultado.get('id')
                if not emp_id:
                    continue  # Saltar registros sin ID
                
                # Obtener nombre, con manejo de diferentes formatos
                nombre = resultado.get('Nombre') or resultado.get('nombre')
                if not nombre or nombre == 'N/A':
                    emp_dict, _ = self.data_manager.buscar_por_id(emp_id)
                    if emp_dict:
                        nombre = f"{emp_dict.get('nombre', '')} {emp_dict.get('apellido', '')}".strip()
                
                # Obtener monto neto, con manejo de diferentes formatos
                monto = float(resultado.get('Neto', 0.0))
                if monto > 0:  # Solo agregar si el monto es positivo
                    self.cheques_procesados.append({
                        'id': emp_id,
                        'nombre': nombre,
                        'monto': monto,
                        'tipo': 'Por Contrato',
                        'resultado': resultado
                    })        # Debug: Mostrar información de los cheques procesados
        print(f"DEBUG: Cantidad de cheques procesados: {len(self.cheques_procesados)}")
        for cheque in self.cheques_procesados:
            print(f"DEBUG: Cheque - ID: {cheque['id']}, Nombre: {cheque['nombre']}, Monto: {cheque['monto']}, Tipo: {cheque['tipo']}")
        
        if not self.cheques_procesados:
            ctk.CTkLabel(
                self.empleados_frame, 
                text="No hay cheques procesados\n\nProcesa empleados en la Cola primero",
                text_color="gray",
                font=ctk.CTkFont(size=14)
            ).pack(pady=40)
            self.actualizar_resumen()
            return
        
        # Ordenar por ID para mantener consistencia
        self.cheques_procesados.sort(key=lambda x: x['id'])
        
        # Mostrar cheques procesados
        for cheque in self.cheques_procesados:
            emp_id = cheque['id']
            nombre = cheque['nombre']
            monto = cheque['monto']
            tipo = cheque['tipo']
            resultado = cheque['resultado']
            
            emp_frame = ctk.CTkFrame(self.empleados_frame, fg_color="#1a1a1a")
            emp_frame.pack(fill="x", pady=8, padx=5)
            
            # Checkbox para selección
            var = ctk.BooleanVar(value=emp_id in self.empleados_seleccionados)
            
            def toggle_selection(emp_id=emp_id, var=var):
                if var.get():
                    if emp_id not in self.empleados_seleccionados:
                        self.empleados_seleccionados.append(emp_id)
                else:
                    if emp_id in self.empleados_seleccionados:
                        self.empleados_seleccionados.remove(emp_id)
                self.actualizar_resumen()
            
            checkbox = ctk.CTkCheckBox(
                emp_frame,
                text="",
                variable=var,
                command=toggle_selection,
                width=30
            )
            checkbox.pack(side="left", padx=10, pady=10)
            
            # Información del cheque
            info_frame = ctk.CTkFrame(emp_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Primera línea: Nombre y ID
            header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            header_frame.pack(fill="x")
            ctk.CTkLabel(header_frame, text=f"{nombre} (ID: {emp_id})", 
                        font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left")
            ctk.CTkLabel(header_frame, text=tipo, text_color="#2fa572", 
                        font=ctk.CTkFont(size=12), anchor="e").pack(side="right")
            
            # Segunda línea: Montos
            montos_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            montos_frame.pack(fill="x", pady=(5,0))
            
            bruto = resultado.get('Bruto', 0.0)
            deducciones = resultado.get('Deducciones', {}).get('total', 0.0)
            
            ctk.CTkLabel(montos_frame, text=f"Bruto: ${bruto:,.2f}", 
                        text_color="gray", anchor="w", 
                        font=ctk.CTkFont(size=12)).pack(side="left", padx=(0,15))
            
            ctk.CTkLabel(montos_frame, text=f"Deducciones: ${deducciones:,.2f}", 
                        text_color="gray", anchor="w",
                        font=ctk.CTkFont(size=12)).pack(side="left", padx=(0,15))
            
            ctk.CTkLabel(montos_frame, text=f"Neto: ${monto:,.2f}", 
                        text_color="#3b8ed0", anchor="w",
                        font=ctk.CTkFont(size=12, weight="bold")).pack(side="left")
            
            # Si hay detalles del procesamiento
            if detalle := resultado.get('Detalle'):
                ctk.CTkLabel(info_frame, text=detalle, text_color="gray",
                            font=ctk.CTkFont(size=11), anchor="w").pack(fill="x", pady=(5,0))
        
        self.actualizar_resumen()
    
    def actualizar_resumen(self):
        """Actualiza el resumen de cheques procesados"""
        # Limpiar frame
        for widget in self.resumen_frame.winfo_children():
            widget.destroy()
        
        # Calcular totales
        cantidad_seleccionados = len(self.empleados_seleccionados)
        total_bruto = 0.0
        total_deducciones = 0.0
        total_neto = 0.0
        
        # Calcular totales de los seleccionados
        for cheque in self.cheques_procesados:
            if cheque['id'] in self.empleados_seleccionados:
                resultado = cheque['resultado']
                total_bruto += float(resultado.get('Bruto', 0.0))
                total_deducciones += float(resultado.get('Deducciones', {}).get('total', 0.0))
                total_neto += float(resultado.get('Neto', 0.0))
        
        # Mostrar estadísticas
        stats_data = [
            ("Cheques Seleccionados", str(cantidad_seleccionados), "#3b8ed0"),
            ("Total Bruto", f"${total_bruto:,.2f}", "#16a34a"),
            ("Total Deducciones", f"${total_deducciones:,.2f}", "#dc2626"),
            ("Total Neto a Pagar", f"${total_neto:,.2f}", "#2fa572"),
            ("Total Cheques", str(len(self.cheques_procesados)), "gray")
        ]
        
        for label, value, color in stats_data:
            stat_frame = ctk.CTkFrame(self.resumen_frame, fg_color="#1a1a1a")
            stat_frame.pack(fill="x", pady=10, padx=10)
            
            ctk.CTkLabel(stat_frame, text=label, text_color="gray", 
                        font=ctk.CTkFont(size=12)).pack(pady=(15, 2), padx=15, anchor="w")
            ctk.CTkLabel(stat_frame, text=value, text_color=color, 
                        font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(2, 15), padx=15, anchor="w")
        
        # Lista de cheques seleccionados
        if self.empleados_seleccionados:
            ctk.CTkLabel(
                self.resumen_frame,
                text="Cheques a Imprimir:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="lightgray"
            ).pack(pady=(20, 10), padx=10, anchor="w")
            
            lista_frame = ctk.CTkScrollableFrame(self.resumen_frame, fg_color="#1a1a1a", height=200)
            lista_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            
            for cheque in self.cheques_procesados:
                if cheque['id'] in self.empleados_seleccionados:
                    resultado = cheque['resultado']
                    nombre = cheque['nombre']
                    tipo = cheque['tipo']
                    neto = float(cheque['monto'])
                    bruto = float(resultado.get('Bruto', 0.0))
                    deducciones = float(resultado.get('Deducciones', {}).get('total', 0.0))
                    
                    item_frame = ctk.CTkFrame(lista_frame, fg_color="#2b2b2b")
                    item_frame.pack(fill="x", pady=5, padx=5)
                    
                    # Nombre y tipo
                    header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
                    header_frame.pack(fill="x", padx=10, pady=(10,5))
                    ctk.CTkLabel(header_frame, text=f"• {nombre}", 
                               text_color="white", anchor="w",
                               font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
                    ctk.CTkLabel(header_frame, text=tipo,
                               text_color="#2fa572", anchor="e",
                               font=ctk.CTkFont(size=10)).pack(side="right")
                    
                    # Montos
                    montos_text = f"Bruto: ${bruto:,.2f} | Deducciones: ${deducciones:,.2f} | Neto: ${neto:,.2f}"
                    ctk.CTkLabel(item_frame, text=montos_text,
                               text_color="gray", anchor="w",
                               font=ctk.CTkFont(size=10)).pack(fill="x", padx=10, pady=(0,10))
    
    def seleccionar_todos(self):
        """Selecciona todos los empleados"""
        empleados = self.data_manager.obtener_empleados()
        self.empleados_seleccionados = [emp.get('id', '') for emp in empleados]
        self.actualizar_lista()
        messagebox.showinfo("Selección", f"Se seleccionaron {len(self.empleados_seleccionados)} empleados")
    
    def procesar_pagos(self):
        """Guarda los cheques seleccionados en la lista de impresión"""
        if not self.empleados_seleccionados:
            messagebox.showwarning("Advertencia", "No hay cheques seleccionados para procesar")
            return
        
        cheques_a_imprimir = []
        total_neto = 0.0
        detalles = "Cheques a imprimir:\n\n"
        
        # Recolectar cheques seleccionados
        for cheque in self.cheques_procesados:
            if cheque['id'] in self.empleados_seleccionados:
                resultado = cheque['resultado']
                monto = float(cheque['monto'])
                total_neto += monto
                
                # Crear tupla de cheque para lista_impresion.csv
                cheque_tuple = (
                    cheque['id'],
                    cheque['nombre'],
                    monto,
                    f"Nómina - {cheque['tipo']}",
                    datetime.now().strftime('%Y-%m-%d')
                )
                cheques_a_imprimir.append(cheque_tuple)
                
                # Agregar al mensaje de detalles
                detalles += f"• {cheque['nombre']}\n"
                detalles += f"  Tipo: {cheque['tipo']}\n"
                detalles += f"  Monto: ${monto:,.2f}\n\n"
        
        detalles += f"━━━━━━━━━━━━━━━\nTotal Neto: ${total_neto:,.2f}"
        
        # Confirmar procesamiento
        cantidad = len(cheques_a_imprimir)
        respuesta = messagebox.askyesno(
            "Confirmar Impresión",
            f"¿Guardar {cantidad} cheques para impresión?\n\nTotal Neto: ${total_neto:,.2f}"
        )
        
        if respuesta:
            # Agregar a la lista de impresión
            self.main_window.lista_impresion.extend(cheques_a_imprimir)
            
            # Guardar todos los datos
            try:
                GestionArchivos.guardar_todos_los_datos(
                    self.main_window.cola_cheques,
                    self.main_window.pila_horas,
                    self.main_window.pila_contratos,
                    self.main_window.diccionario_calculos,
                    self.main_window.lista_impresion
                )
                
                messagebox.showinfo(
                    "Cheques Guardados",
                    f"✓ Se guardaron {cantidad} cheques para impresión\n\n{detalles}"
                )
                
                # Limpiar selección
                self.empleados_seleccionados.clear()
                self.actualizar_lista()
                
            except Exception as e:
                messagebox.showerror(
                    "Error al Guardar",
                    f"Ocurrió un error al guardar los cheques:\n{str(e)}"
                )