from datetime import date

class Usuario:
    def __init__(self, id_usuario, nombre, email):
        self._id_usuario = id_usuario
        self._nombre = nombre
        self._email = email

    @property
    def id_usuario(self):
        return self._id_usuario

    @property
    def nombre(self):
        return self._nombre

    @property
    def email(self):
        return self._email

    def to_dict(self):
        return {
            "id_usuario": self._id_usuario,
            "nombre": self._nombre,
            "email": self._email,
            "tipo": "Usuario"
        }

class Socio(Usuario):
    MAX_PRESTAMOS = 3
    DIAS_PRESTAMO = 14

    def __init__(self, id_usuario, nombre, email):
        super().__init__(id_usuario, nombre, email)
        self._sancionado = False
        self._fecha_fin_sancion = None  #fecha en la que termina la sancion, None si no esta sancionado
        self._prestamos_activos = []  #lista con los ids de prestamos activos

    @property
    def sancionado(self):
        return self._sancionado

    @sancionado.setter
    def sancionado(self, valor):
        self._sancionado = valor

    @property
    def fecha_fin_sancion(self):
        return self._fecha_fin_sancion

    @fecha_fin_sancion.setter
    def fecha_fin_sancion(self, valor):
        self._fecha_fin_sancion = valor

    @property
    def prestamos_activos(self):
        return self._prestamos_activos

    def puede_pedir_prestamo(self):
        #si esta sancionado no puede pedir nada
        if self._sancionado:
            return False
        #tampoco si ya tiene el maximo de prestamos
        return len(self._prestamos_activos) < self.MAX_PRESTAMOS

    def to_dict(self):
        d = super().to_dict()
        d.update({
            "sancionado": self._sancionado,
            "fecha_fin_sancion": self._fecha_fin_sancion.isoformat() if self._fecha_fin_sancion else None,
            "prestamos_activos": self._prestamos_activos,
            "tipo": "Socio"
        })
        return d

class Bibliotecario(Usuario):
    def __init__(self, id_usuario, nombre, email, num_empleado):
        super().__init__(id_usuario, nombre, email)
        self._num_empleado = num_empleado

    @property
    def num_empleado(self):
        return self._num_empleado

    def to_dict(self):
        d = super().to_dict()
        d["num_empleado"] = self._num_empleado #los corchetes son otra forma de poner d.update()
        d["tipo"] = "Bibliotecario" #cambiamos el tipo de usuario de "usuario" a "bibliotecario"
        return d

class Administrador(Usuario):
    def __init__(self, id_usuario, nombre, email):
        super().__init__(id_usuario, nombre, email) #recogemos los datos del usuario
        self._activo = True #todos los admins estan activos x defecto

    def to_dict(self): #to_dict() convierte un objeto en un diccionario
        d = super().to_dict()
        d["activo"] = self._activo
        d["tipo"] = "Administrador"
        return d
