#Excepciones personalizadas del proyecto OpenBook
#Marcos

class MaterialNoEncontrado(Exception):
    def __init__(self, id_material):
        super().__init__(f"No se encontro ningun material con id '{id_material}'.")

class MaterialNoDisponible(Exception):
    def __init__(self, id_material):
        super().__init__(f"El material '{id_material}' no esta disponible.")

class MaterialYaExiste(Exception):
    def __init__(self, id_material):
        super().__init__(f"Ya existe un material con id '{id_material}'.")

class UsuarioNoEncontrado(Exception):
    def __init__(self, id_usuario):
        super().__init__(f"No se encontro ningun usuario con id '{id_usuario}'.")

class UsuarioSancionado(Exception):
    def __init__(self, nombre):
        super().__init__(f"El usuario '{nombre}' esta sancionado y no puede pedir prestamos.")

class LimitePrestamosAlcanzado(Exception):
    def __init__(self, nombre, maximo):
        super().__init__(f"'{nombre}' ya tiene {maximo} prestamos activos.")

class PrestamoNoEncontrado(Exception):
    def __init__(self, id_prestamo):
        super().__init__(f"No se encontro ningun prestamo con id '{id_prestamo}'.")

class PrestamoYaDevuelto(Exception):
    def __init__(self, id_prestamo):
        super().__init__(f"El prestamo '{id_prestamo}' ya fue devuelto.")

class ReservaNoEncontrada(Exception):
    def __init__(self, id_reserva):
        super().__init__(f"No se encontro ninguna reserva con id '{id_reserva}'.")
