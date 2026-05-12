from datetime import date, timedelta #importamos date para saber la fecha del prestamo y timedelta para calcular la fecha limite

class Prestamo:
    def __init__(self, id_prestamo, id_usuario, id_material, dias_prestamo=14):
        self._id_prestamo = id_prestamo
        self._id_usuario = id_usuario
        self._id_material = id_material
        self._fecha_prestamo = date.today()
        self._fecha_limite = date.today() + timedelta(days=dias_prestamo)
        self._fecha_devolucion = None  #None significa que todavia no se ha devuelto
        self._devuelto = False

    @property
    def id_prestamo(self):
        return self._id_prestamo

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_material(self):
        return self._id_material

    @property
    def fecha_limite(self):
        return self._fecha_limite

    @property
    def devuelto(self):
        return self._devuelto

    def esta_vencido(self):
        #si ya esta devuelto no puede estar vencido
        if self._devuelto:
            return False
        return date.today() > self._fecha_limite

    def dias_retraso(self):
        #si no hay retraso devolvemos 0
        if not self.esta_vencido() and not self._devuelto:
            return 0
        referencia = self._fecha_devolucion if self._devuelto else date.today()
        if referencia <= self._fecha_limite:
            return 0
        return (referencia - self._fecha_limite).days

    def devolver(self):
        self._devuelto = True
        self._fecha_devolucion = date.today()

    def to_dict(self):
        return {
            "id_prestamo": self._id_prestamo,
            "id_usuario": self._id_usuario,
            "id_material": self._id_material,
            "fecha_prestamo": str(self._fecha_prestamo),
            "fecha_limite": str(self._fecha_limite),
            "fecha_devolucion": str(self._fecha_devolucion) if self._fecha_devolucion else None,
            "devuelto": self._devuelto
        }

    def __str__(self):
        estado = "Devuelto" if self._devuelto else ("VENCIDO" if self.esta_vencido() else "Activo")
        return f"[{self._id_prestamo}] Usuario {self._id_usuario} | Material {self._id_material} | Limite: {self._fecha_limite} | {estado}"


class Reserva:
    def __init__(self, id_reserva, id_usuario, id_material): #fecha_reserva se asigna automaticamente
        self._id_reserva = id_reserva
        self._id_usuario = id_usuario
        self._id_material = id_material
        self._fecha_reserva = date.today() # guardamos la fecha en la que se hizo la reserva
        self._activa = True
        self._fecha_disponible = None  #fecha en la que el material estara disponible, la pone el bibliotecario

    @property
    def id_reserva(self):
        return self._id_reserva

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def id_material(self):
        return self._id_material

    @property
    def activa(self):
        return self._activa

    @activa.setter
    def activa(self, valor):
        self._activa = valor

    @property
    def fecha_disponible(self):
        return self._fecha_disponible

    @fecha_disponible.setter
    def fecha_disponible(self, valor):
        self._fecha_disponible = valor

    def esta_caducada(self):
        # metodo para verificar si han pasado más de 3 días, por ejemplo
        delta = date.today() - self._fecha_reserva #restamos la fecha actual a la de reserva para ver cuantos dias han pasado.
        return delta.days > 3

    def to_dict(self):
        return {
            "id_reserva": self._id_reserva,
            "id_usuario": self._id_usuario,
            "id_material": self._id_material,
            "fecha_reserva": self._fecha_reserva.isoformat(), #convierte una fecha en string
            "activa": self._activa,
            "fecha_disponible": self._fecha_disponible.isoformat() if self._fecha_disponible else None
        }
