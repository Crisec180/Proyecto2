import customtkinter as ctk

class PilaView:
    """Vista para la gestión de Pila (LIFO)"""
    
    def __init__(self, parent, pila, titulo, label_text):
        self.parent = parent
        self.pila = pila
        self.titulo = titulo
        self.label_text = label_text
    
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
        
        subtitle = ctk.CTkLabel(header_frame, text=f"Visualización de la pila para cálculo de {self.titulo.lower()}", font=ctk.CTkFont(size=14), text_color="gray")
        subtitle.pack(anchor="w")
    
    def create_left_panel(self, parent):
        left_panel = ctk.CTkFrame(parent, fg_color="#1a1a1a")
        left_panel.grid(row=0, column=0, sticky="ew", pady=(0, 20))