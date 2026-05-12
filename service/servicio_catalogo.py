from model.usuario import Socio
from model.material import Libro, Revista, RecursoDigital

class ServicioCatalogo:
    def __init__(self, repositorio_materiales, repositorio_usuarios):
        self._repositorio_materiales = repositorio_materiales
        self._repositorio_usuarios = repositorio_usuarios

    #---GESTIÓN DE MATERIALES---

    def alta_material(self, material):
        """Agrega un nuevo material al catálogo"""
        self._repositorio_materiales.agregar(material)

    def baja_material(self, id_material):
        """Elimina un material si no esta prestado, sino lanza excepción"""
        material = self._repositorio_materiales.obtener(id_material)
        if not material.disponible:
            raise Exception(f"No se puede eliminar: El material con ID {id_material} está prestado.")
        self._repositorio_materiales.eliminar(id_material)

    def buscar_materiales(self, texto):
        """Busca en titulo y autor sin distinguir mayúsculas/minúsculas"""
        texto_busqueda = texto.lower()
        todos = self._repositorio_materiales.listar_todos()
        resultados = [
            m for m in todos
            if texto_busqueda in m.titulo.lower() or texto_busqueda in m.autor.lower()
        ]
        return resultados

    #---GESTIÓN DE USUARIOS---
    def registrar_usuario(self, usuario):
        """Registra un nuevo usuario"""
        self._repositorio_usuarios.agregar(usuario)

    def dar_baja_usuario(self, id_usuario):
        """Elimina un usuario si no tiene préstamos activos, sino lanza excepción"""
        usuario = self._repositorio_usuarios.obtener(id_usuario)
        if isinstance(usuario, Socio) and len(usuario.prestamos_activos) > 0:
            raise Exception(f"No se puede eliminar: el usuario {id_usuario} tiene prestamos activos.")
        self._repositorio_usuarios.eliminar(id_usuario)

    #---INFORMES---
    def listar_todos(self):
        """Devuelve una lista de todos los materiales en el catálogo"""
        return self._repositorio_materiales.listar_todos()

    def listar_disponibles(self):
        """Devuelve solo los materiales disponibles"""
        return self._repositorio_materiales.listar_disponibles()

    def listar_usuarios(self):
        """Devuelve todos los usuarios"""
        return self._repositorio_usuarios.listar_todos()

    def listar_usuarios_sancionados(self):
        """Devuelve una lista de socios sancionados"""
        usuarios = self._repositorio_usuarios.listar_todos()
        return [u for u in usuarios if isinstance(u, Socio) and u.sancionado]

    def obtener_usuario(self, id_usuario):
        """Devuelve un usuario por su ID"""
        return self._repositorio_usuarios.obtener(id_usuario)
