class Persona:
    def __init__(self, nombre, edad, cedula, correo):
        self.nombre = nombre
        self.edad = edad
        self.cedula = cedula
        self.correo = correo
        
    def __str__(self):
        return f"Nombre: {self.nombre}, Edad: {self.edad}, Cédula: {self.cedula}, Correo: {self.correo}"