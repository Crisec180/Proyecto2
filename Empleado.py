class Empleado:
    def __init__(self, id, nombre, apellido, edad, telefono, correo):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.telefono = telefono
        self.correo = correo

    def __str__(self):
        return f"{self.id} - {self.nombre} {self.apellido}, {self.edad} años, Telefono: {self.telefono}, Email: {self.correo}"
