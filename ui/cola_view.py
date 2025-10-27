import customtkinter as ctk
from tkinter import messagebox
from CalculoConCOLAS.CalculaNetoEmpleado import calculaNetoEmpleado
from Empleado import Empleado
from GestionArchivos import GestionArchivos

class ColaView:
    
    def __init__(self, parent, cola_cheques, data_manager, main_window):
        self.parent = parent
        self.cola_cheques = cola_cheques
        self.data_manager = data_manager
        self.main_window = main_window
        self.calculador_cola = None
    
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
        
        subtitle = ctk.CTkLabel(header_frame, text="Visualización de la cola de procesamiento (FIFO) - Usa CalculaNetoEmpleado", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
        
        empleado = self.data_manager.obtener_empleado_seleccionado()
        if empleado:
            info = ctk.CTkLabel(
                header_frame,
                text=f"Trabajando con: {empleado.get('nombre', '')} {empleado.get('apellido', '')} (ID: {empleado.get('id', '')})",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#2fa572"
            )
            info.pack(anchor="w", pady=(5, 0))
    
    def crear_objeto_empleado(self, emp_dict):
        """Convierte diccionario de empleado a objeto Empleado"""
        return Empleado(
            id=emp_dict.get('id', ''),
            nombre=emp_dict.get('nombre', ''),
            apellido=emp_dict.get('apellido', ''),
            departamento=emp_dict.get('departamento', 'General'),
            puesto=emp_dict.get('puesto', 'Empleado'),
            salario_base=float(emp_dict.get('salario_base', 0)),
            tipo_contrato=emp_dict.get('tipo_contrato', 'Mensual')
        )
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ctk.CTkLabel(left_panel, text="ENQUEUE - Agregar a la Cola", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=20)
        
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
        
        ctk.CTkLabel(left_panel, text="Horas Extras:", font=ctk.CTkFont(size=12)).pack(pady=(10, 5), padx=20, anchor="w")
        horas_entry = ctk.CTkEntry(left_panel, placeholder_text="Ej: 10 (horas)")
        horas_entry.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Tipo de Cheque:", font=ctk.CTkFont(size=12)).pack(pady=(10, 5), padx=20, anchor="w")
        tipo_menu = ctk.CTkOptionMenu(left_panel, values=["Pago de salario", "Caja chica", "Otros Gastos"])
        tipo_menu.pack(pady=(0, 10), padx=20, fill="x")
        
        ctk.CTkLabel(left_panel, text="Cola Actual (FIFO):", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        # reducir altura del área de lista para dejar más espacio a los botones
        self.queue_display = ctk.CTkScrollableFrame(left_panel, fg_color="#2b2b2b", height=120)
        self.queue_display.pack(fill="both", expand=True, padx=20, pady=8)
        
        def enqueue():
            if not empleados:
                messagebox.showwarning("Advertencia", "No hay empleados cargados. Carga un archivo CSV primero.")
                return
            
            seleccion = empleado_menu.get()
            horas_extras_str = horas_entry.get()
            tipo_cheque = tipo_menu.get()
            
            if not seleccion or "No hay empleados" in seleccion:
                messagebox.showwarning("Advertencia", "Selecciona un empleado válido")
                return
            
            try:
                horas_extras = float(horas_extras_str) if horas_extras_str else 0
                if horas_extras < 0:
                    messagebox.showerror("Error", "Las horas extras no pueden ser negativas")
                    return
            except ValueError:
                messagebox.showerror("Error", "Ingresa un número válido de horas")
                return
            
            id_emp = seleccion.split(" - ")[-1]
            emp_dict, error = self.data_manager.buscar_por_id(id_emp)
            
            if error:
                messagebox.showerror("Error", error)
                return
            
            empleado_obj = self.crear_objeto_empleado(emp_dict)
            
            item_cola = {
                'empleado': empleado_obj,
                'empleado_dict': emp_dict,
                'horas_extras': horas_extras,
                'tipo_cheque': tipo_cheque,
                'estado': 'En espera',
                'resultado': None
            }
            
            self.cola_cheques.append(item_cola)
            self.update_queue_display()
            
            try:
                GestionArchivos.guardar_todos_los_datos(
                    self.cola_cheques,
                    self.main_window.pila_horas,
                    self.main_window.pila_contratos,
                    self.main_window.diccionario_calculos,
                    self.main_window.lista_impresion
                )
            except Exception as e:
                print(f"Error al guardar datos: {e}")
            
            horas_entry.delete(0, 'end')
            messagebox.showinfo("Éxito ENQUEUE", 
                f"Empleado agregado a la cola (ENQUEUE)\n\n"
                f"{empleado_obj.nombre} {empleado_obj.apellido}\n"
                f"Horas extras: {horas_extras}\n"
                f"Tipo: {tipo_cheque}\n"
                f"Posición en cola: #{len(self.cola_cheques)}")
        
        def dequeue():
            if not self.cola_cheques:
                messagebox.showinfo("Cola Vacía", "No hay elementos en la cola para procesar")
                return
            
            item = self.cola_cheques.pop(0)
            emp_field = item['empleado']
            horas_extras = item['horas_extras']
            tipo_cheque = item['tipo_cheque']

            # Normalizar empleado_obj: puede ser dict, id (str) o objeto Empleado
            empleado_obj = None
            emp_id = None
            if isinstance(emp_field, dict):
                emp_id = emp_field.get('id') or emp_field.get('id_empleado')
                empleado_obj = self.crear_objeto_empleado(emp_field)
            elif isinstance(emp_field, str):
                emp_id = emp_field
                emp_dict, err = self.data_manager.buscar_por_id(emp_id)
                if emp_dict:
                    empleado_obj = self.crear_objeto_empleado(emp_dict)
            else:
                # Asumir objeto Empleado
                empleado_obj = emp_field
                emp_id = getattr(empleado_obj, 'id', None)
            
            try:
                # DEBUG: mostrar item que se va a procesar
                try:
                    print(f"DEBUG dequeue - procesando item: empleado_id={emp_id}, horas_extras={horas_extras}, tipo_cheque={tipo_cheque}")
                except Exception:
                    pass

                # Intentar obtener resultados previos desde las pilas (si existen)
                resultado_horas = None
                resultado_contrato = None

                emp_id = getattr(empleado_obj, 'id', None)
                # Buscar último resultado correspondiente en pila_horas
                for r in reversed(self.main_window.pila_horas):
                    try:
                        if r.get('id', r.get('Id')) == emp_id:
                            resultado_horas = r
                            break
                    except Exception:
                        continue

                # Buscar último resultado correspondiente en pila_contratos
                for r in reversed(self.main_window.pila_contratos):
                    try:
                        # contrato puede tener 'id' o 'Id' y estructura distinta
                        if r.get('id', r.get('Id')) == emp_id:
                            resultado_contrato = r
                            break
                    except Exception:
                        continue

                calculador = calculaNetoEmpleado([empleado_obj], horas_extras, tipo_cheque)
                # Llamar al nuevo método que combina los dos resultados y aplica horas extras/tipo de cheque
                resultado = calculador.combinar_y_encolar(resultado_horas, resultado_contrato, empleado_obj, horas_extras, tipo_cheque)

                # Guardar el resultado en la pila correspondiente para visualización
                if "horas" in empleado_obj.tipo_contrato.lower():
                    self.main_window.pila_horas.append(resultado)
                else:
                    self.main_window.pila_contratos.append(resultado)
                
                emp_id = empleado_obj.id
                if emp_id not in self.main_window.diccionario_calculos:
                    self.main_window.diccionario_calculos[emp_id] = {}
                
                self.main_window.diccionario_calculos[emp_id]['ultimo_calculo'] = resultado.get('Neto', 0)
                self.main_window.diccionario_calculos[emp_id]['fecha_proceso'] = 'Hoy'
                
                self.update_queue_display()
                
                try:
                    GestionArchivos.guardar_todos_los_datos(
                        self.cola_cheques,
                        self.main_window.pila_horas,
                        self.main_window.pila_contratos,
                        self.main_window.diccionario_calculos,
                        self.main_window.lista_impresion
                    )
                except Exception as e:
                    print(f"Error al guardar datos: {e}")
                
                mensaje = f"DEQUEUE - Empleado procesado exitosamente\n\n"
                mensaje += f"{empleado_obj.nombre} {empleado_obj.apellido}\n"
                mensaje += f"Neto calculado: ${resultado.get('Neto', 0):,.2f}\n"
                mensaje += f"Bruto: ${resultado.get('Bruto', 0):,.2f}\n"
                mensaje += f"Deducciones: ${resultado.get('Deducciones', {}).get('total', 0):,.2f}\n\n"
                mensaje += f"Resultado guardado en {'Pila Horas' if 'horas' in empleado_obj.tipo_contrato.lower() else 'Pila Contratos'}\n"
                mensaje += f"Resultado guardado en Diccionario"
                
                messagebox.showinfo("DEQUEUE Exitoso", mensaje)
                
            except Exception as e:
                messagebox.showerror("Error al Procesar", f"Error durante DEQUEUE:\n{str(e)}")
                self.cola_cheques.insert(0, item)
                self.update_queue_display()
        
        def clear_queue():
            if not self.cola_cheques:
                messagebox.showinfo("Cola Vacía", "La cola ya está vacía")
                return
            
            cantidad = len(self.cola_cheques)
            respuesta = messagebox.askyesno("Confirmar", f"¿Limpiar {cantidad} elementos de la cola?")
            
            if respuesta:
                self.cola_cheques.clear()
                self.update_queue_display()
                
                try:
                    GestionArchivos.guardar_todos_los_datos(
                        self.cola_cheques,
                        self.main_window.pila_horas,
                        self.main_window.pila_contratos,
                        self.main_window.diccionario_calculos,
                        self.main_window.lista_impresion
                    )
                except Exception as e:
                    print(f"Error al guardar datos: {e}")
                
                messagebox.showinfo("Cola Limpiada", f"Se removieron {cantidad} elementos")
        
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        btn_frame.pack(pady=10, padx=20, fill="x")
        
        # ENQUEUE - botón prominente y más grande
        enqueue_btn = ctk.CTkButton(
            btn_frame,
            text="➕ ENQUEUE (Agregar Empleado)",
            command=enqueue,
            fg_color="#16a34a",
            hover_color="#0ea55a",
            height=40,  # Aumentado de 60 a 80
            font=ctk.CTkFont(size=16, weight="bold"),  # Aumentado de 14 a 16
            text_color="white",
            corner_radius=8,
            border_width=2
        )
        enqueue_btn.pack(fill="x", pady=(12, 10))

        # Botón de DEQUEUE
        dequeue_btn = ctk.CTkButton(
            btn_frame,
            text="▶️ DEQUEUE (Procesar Primero)",
            command=dequeue,
            fg_color="#2563eb",
            hover_color="#1e40af",
            height=80,  # Aumentado de 44 a 50
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
            corner_radius=8
        )
        dequeue_btn.pack(fill="x", pady=8)

        # Frame para botones de borrado
        delete_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
        delete_frame.pack(fill="x", pady=4)
        delete_frame.grid_columnconfigure((0, 1), weight=1)

        # Botón de borrar elemento
        ctk.CTkButton(
            delete_frame,
            text="🗑️ Borrar Elemento",
            command=lambda: messagebox.showinfo("En desarrollo", "Función de borrar elemento individual próximamente disponible"),
            fg_color="#dc2626",
            hover_color="#b91c1c",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
            corner_radius=6
        ).grid(row=0, column=0, padx=2, sticky="ew")

        # Botón de limpiar cola
        ctk.CTkButton(
            delete_frame,
            text="🧹 Limpiar Cola",
            command=clear_queue,
            fg_color="#6b7280",
            hover_color="#4b5563",
            height=45,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white",
            corner_radius=6
        ).grid(row=0, column=1, padx=2, sticky="ew")

        def clear_all_queues():
            # Limpiar las estructuras globales (cola y pilas) en la ventana principal
            respuesta = messagebox.askyesno("Confirmar", "¿Limpiar COLA y PILAS (horas y contratos)? Esto eliminará todos los elementos.")
            if not respuesta:
                return
            try:
                # Limpiar las estructuras en main_window
                self.main_window.cola_cheques.clear()
                self.main_window.pila_horas.clear()
                self.main_window.pila_contratos.clear()
                # Actualizar displays locales
                self.update_queue_display()
                try:
                    GestionArchivos.guardar_todos_los_datos(
                        self.main_window.cola_cheques,
                        self.main_window.pila_horas,
                        self.main_window.pila_contratos,
                        self.main_window.diccionario_calculos,
                        self.main_window.lista_impresion
                    )
                except Exception as e:
                    print(f"Error al guardar datos después de limpiar: {e}")
                messagebox.showinfo("Colas limpiadas", "Se limpiaron Cola, Pila Horas y Pila Contratos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo limpiar las colas: {e}")

        ctk.CTkButton(btn_frame, text="Borrar Todas las Colas", command=clear_all_queues,
                     fg_color="#dc2626", hover_color="#b91c1c", height=40).pack(fill="x", pady=5)
        
        info_frame = ctk.CTkFrame(left_panel, fg_color="#2b2b2b", border_width=2, border_color="#2fa572")
        info_frame.pack(pady=10, padx=20, fill="x")
        
        info_text = "ℹEstructura: Cola (deque)\nProcesa: Calcular Neto Empleado\nFlujo: FIFO (First In, First Out)"
        ctk.CTkLabel(info_frame, text=info_text, font=ctk.CTkFont(size=10), 
                    text_color="gray", justify="left").pack(padx=10, pady=10)
        
        self.update_queue_display()
    
    def create_right_panel(self, parent):
        right_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        ctk.CTkLabel(right_panel, text="Visualización de Cola (FIFO)", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=20)
        
        info_label = ctk.CTkLabel(
            right_panel, 
            text="FIFO: First In, First Out\nEl primer elemento agregado será el primero en procesarse\n✓ Usa: CalculaNetoEmpleado (con deque)",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            justify="center"
        )
        info_label.pack(pady=(0, 10), padx=20)
        
        self.display_frame = ctk.CTkScrollableFrame(right_panel, fg_color="#2b2b2b")
        self.display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.update_display()
    
    def update_queue_display(self):
        for widget in self.queue_display.winfo_children():
            widget.destroy()
    
        if not self.cola_cheques:
            ctk.CTkLabel(self.queue_display, text="Cola vacía", text_color="gray", 
                      font=ctk.CTkFont(size=11)).pack(pady=10)
        else:
            for idx, item in enumerate(self.cola_cheques[:5]):
                emp = item['empleado']
            
                if isinstance(emp, str):
                    emp_dict, _ = self.data_manager.buscar_por_id(emp)
                    if emp_dict:
                        nombre = f"{emp_dict.get('nombre', '')} {emp_dict.get('apellido', '')}"
                    else:
                        nombre = emp
                elif isinstance(emp, dict):
                    nombre = f"{emp.get('nombre', '')} {emp.get('apellido', '')}"
                else:
                    nombre = f"{emp.nombre} {emp.apellido}"
            
                texto = f"{idx+1}. {nombre} - {item['horas_extras']}h - {item['tipo_cheque']}"
                color = "#2fa572" if idx == 0 else "gray"
                peso = "bold" if idx == 0 else "normal"
                ctk.CTkLabel(self.queue_display, text=texto, text_color=color, 
                        font=ctk.CTkFont(size=10, weight=peso)).pack(anchor="w", padx=5, pady=2)
        
            if len(self.cola_cheques) > 5:
                ctk.CTkLabel(self.queue_display, text=f"... y {len(self.cola_cheques) - 5} más", 
                        text_color="gray", font=ctk.CTkFont(size=9)).pack(anchor="w", padx=5, pady=2)
    
        if hasattr(self, 'display_frame'):
            self.update_display()
    
    def update_display(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()
    
        if not self.cola_cheques:
            ctk.CTkLabel(self.display_frame, text="Cola vacía\n\nAgrega empleados para comenzar", 
                        text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=40)
            return

        for idx, item in enumerate(self.cola_cheques):
            emp = item['empleado']
        
            if isinstance(emp, str):
                emp_dict, _ = self.data_manager.buscar_por_id(emp)
                if emp_dict:
                    emp_nombre = emp_dict.get('nombre', 'N/A')
                    emp_apellido = emp_dict.get('apellido', '')
                    emp_id = emp_dict.get('id', emp)
                    emp_puesto = emp_dict.get('puesto', 'N/A')
                    emp_departamento = emp_dict.get('departamento', 'N/A')
                    emp_salario = emp_dict.get('salario_base', 0)
                    emp_contrato = emp_dict.get('tipo_contrato', 'N/A')
                else:
                    emp_nombre = emp
                    emp_apellido = ''
                    emp_id = emp
                    emp_puesto = 'N/A'
                    emp_departamento = 'N/A'
                    emp_salario = 0
                    emp_contrato = 'N/A'
            elif isinstance(emp, dict):
                emp_nombre = emp.get('nombre', 'N/A')
                emp_apellido = emp.get('apellido', '')
                emp_id = emp.get('id', 'N/A')
                emp_puesto = emp.get('puesto', 'N/A')
                emp_departamento = emp.get('departamento', 'N/A')
                emp_salario = emp.get('salario_base', 0)
                emp_contrato = emp.get('tipo_contrato', 'N/A')
            else:
                # Objeto Empleado
                emp_nombre = emp.nombre
                emp_apellido = emp.apellido
                emp_id = emp.id
                emp_puesto = emp.puesto
                emp_departamento = emp.departamento
                emp_salario = emp.salario_base
                emp_contrato = emp.tipo_contrato
        
            item_frame = ctk.CTkFrame(self.display_frame, fg_color="#1a1a1a", 
                                     border_width=2, border_color="#2fa572" if idx == 0 else "#3b3b3b")
            item_frame.pack(fill="x", pady=8, padx=5)
        
            position_text = "SIGUIENTE EN PROCESAR (DEQUEUE)" if idx == 0 else f"Posición #{idx + 1} en cola"
            position_color = "#2fa572" if idx == 0 else "gray"
        
            header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
            ctk.CTkLabel(header_frame, text=position_text, text_color=position_color, 
                    font=ctk.CTkFont(size=11, weight="bold")).pack(side="left")
        
            info_text = f"{emp_nombre} {emp_apellido}\n"
            info_text += f"ID: {emp_id}\n"
            info_text += f"Puesto: {emp_puesto}\n"
            info_text += f"Departamento: {emp_departamento}\n"
            info_text += f"Salario Base: ${emp_salario:,.2f}\n"
            info_text += f"Contrato: {emp_contrato}\n"
            info_text += f"Horas Extras: {item['horas_extras']}h\n"
            info_text += f"Tipo Cheque: {item['tipo_cheque']}"
        
            ctk.CTkLabel(item_frame, text=info_text, text_color="lightgray", 
                        justify="left", font=ctk.CTkFont(size=10)).pack(anchor="w", padx=15, pady=(5, 15))