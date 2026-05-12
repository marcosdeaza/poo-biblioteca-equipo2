from datetime import date, timedelta
from model.prestamo import Prestamo, Reserva
from model.usuario import Socio

class ServicioPrestamos:
    def __init__(self, repo_usuarios, repo_materiales, repo_prestamos):
        self._repo_usuarios = repo_usuarios
        self._repo_materiales = repo_materiales
        self._repo_prestamos = repo_prestamos

    def prestar(self, id_usuario, id_material):
        """Realiza un préstamo si el material está disponible y el usuario no está sancionado"""
        usuario = self._repo_usuarios.obtener(id_usuario)
        material = self._repo_materiales.obtener(id_material)

        #Validaciones
        if not isinstance(usuario, Socio):
            raise Exception(f"El usuario con ID {id_usuario} no es un socio y no puede pedir préstamos.")
        if not material.disponible:
            raise Exception(f"El material con ID {id_material} no está disponible para préstamo.")
        if not usuario.puede_pedir_prestamo():
            raise Exception(f"El usuario con ID {id_usuario} no puede realizar préstamos debido a sanciones o límite de préstamos activos.")

        nuevo_id = f"P{len(self._repo_prestamos.listar_todos()) + 1:04d}"  # Genera un ID único para el préstamo

        nuevo_prestamo = Prestamo(nuevo_id, id_usuario, id_material)  #la fecha limite se calcula dentro del constructor

        material.disponible = False  # Marcar el material como no disponible
        usuario.prestamos_activos.append(nuevo_id)

        self._repo_prestamos.agregar(nuevo_prestamo)
        return nuevo_prestamo  # Devolver el préstamo creado


    def devolver(self, id_prestamo):
        """Gestiona la devolución de un material, actualizando el estado del préstamo y del material"""
        prestamo = self._repo_prestamos.obtener(id_prestamo)
        if prestamo.devuelto:
            raise Exception("Este prestamo ya fue devuelto")

        material = self._repo_materiales.obtener(prestamo.id_material)
        usuario = self._repo_usuarios.obtener(prestamo.id_usuario)

        prestamo.devolver()  # Marca el préstamo como devuelto
        material.disponible = True  # Marca el material como disponible
        usuario.prestamos_activos.remove(id_prestamo)  # Elimina el préstamo de los activos del usuario

        #si hay retraso sancionamos al socio
        dias = prestamo.dias_retraso()
        if dias > 0 and isinstance(usuario, Socio):
            usuario.sancionado = True
            usuario.fecha_fin_sancion = date.today() + timedelta(days=dias)

        #comprobamos si hay reservas para este material y avisamos
        reservas = self._repo_prestamos.listar_reservas_material(prestamo.id_material)
        if reservas:
            print(f"\nAviso: hay {len(reservas)} reserva(s) activa(s) para este material.")

        return dias

    def reservar(self, id_usuario, id_material):
        """Crea una reserva para un material que no está disponible"""
        material = self._repo_materiales.obtener(id_material)
        if material.disponible:
            raise Exception(f"El material con ID {id_material} está disponible, no se puede reservar.")

        nuevo_id = f"V{len(self._repo_prestamos.listar_reservas()) + 1:04d}"  # Genera un ID único para la reserva
        reserva = Reserva(nuevo_id, id_usuario, id_material)  #la fecha se asigna internamente

        self._repo_prestamos.agregar_reserva(reserva)
        return reserva

    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva activa"""
        reserva = self._repo_prestamos.obtener_reserva(id_reserva)
        reserva.activa = False  # Marca la reserva como inactiva

    def listar_vencidos(self):
        """Devuelve los prestamos que han superado su fecha limite"""
        return self._repo_prestamos.listar_vencidos()

    def cancelar_prestamo(self, id_prestamo):
        """Anula un prestamo activo sin aplicar sancion (correccion administrativa)"""
        prestamo = self._repo_prestamos.obtener(id_prestamo)
        if prestamo.devuelto:
            raise Exception("Este prestamo ya fue devuelto, no se puede cancelar.")
        material = self._repo_materiales.obtener(prestamo.id_material)
        usuario = self._repo_usuarios.obtener(prestamo.id_usuario)
        material.disponible = True
        if id_prestamo in usuario.prestamos_activos:
            usuario.prestamos_activos.remove(id_prestamo)
        self._repo_prestamos.eliminar(id_prestamo)

    def listar_activos(self):
        """Devuelve todos los prestamos que aun no han sido devueltos"""
        return self._repo_prestamos.listar_activos()

    def listar_reservas(self):
        """Devuelve todas las reservas activas"""
        return self._repo_prestamos.listar_reservas()
