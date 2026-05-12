import json
import os
from datetime import date
#Importamos las clases de Marc
from model.usuario import Socio, Bibliotecario, Administrador

class RepositorioUsuarios:
    def __init__(self):
        #Inicializamos la lista de usuarios y el nombre del archivo JSON
        self._usuarios = []
        self._archivo = "datos/usuarios.json"

    def agregar(self, usuario):
        """Agrega un usuario a la lista si su ID no existe"""
        for u in self._usuarios:
            #Se accede al atributo privado _id_usuario para comparar con el ID del nuevo usuario
            if u.id_usuario == usuario.id_usuario:
                raise Exception(f"El ID {usuario.id_usuario} ya está registrado.")
        self._usuarios.append(usuario)

    def obtener(self, id_usuario):
        """Busca por ID o lanza excepción según contrato"""
        for usuario in self._usuarios:
            if usuario.id_usuario == id_usuario:
                return usuario
        raise Exception(f"Usuario con ID {id_usuario} no encontrado.")

    def eliminar(self, id_usuario):
        """Elimina por ID o lanza excepción si no existe"""
        usuario = self.obtener(id_usuario)  # Esto lanzará excepción si no se encuentra
        self._usuarios.remove(usuario)

    def listar_todos(self):
        """Devuelve la lista completa de usuarios"""
        return self._usuarios

    def guardar(self):
        """Guarda los usuarios en un archivo JSON"""
        os.makedirs(os.path.dirname(self._archivo), exist_ok=True)
        with open(self._archivo, 'w', encoding='utf-8') as f:
            data = [u.to_dict() for u in self._usuarios]
            json.dump(data, f, ensure_ascii=False, indent=4)

    def cargar(self):
        """Lee JSON y reconstruye los objetos de usuario"""
        try:
            with open(self._archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            for d in datos:
                #Extraemos el tipo de usuario para saber qué clase instanciar
                tipo = d.pop("tipo")

                if tipo == "Socio":
                    #sacamos los campos extra antes de llamar al constructor
                    fecha = d.pop("fecha_fin_sancion", None)
                    prestamos = d.pop("prestamos_activos", [])
                    sancionado = d.pop("sancionado", False)
                    u = Socio(**d)  #ahora d solo tiene id_usuario, nombre, email
                    u.sancionado = sancionado
                    u.fecha_fin_sancion = date.fromisoformat(fecha) if fecha else None
                    u._prestamos_activos = prestamos
                elif tipo == "Bibliotecario":
                    u = Bibliotecario(**d)
                elif tipo == "Administrador":
                    d.pop("activo", None)  #quitamos activo porque el constructor no lo recibe
                    u = Administrador(**d)
                else:
                    continue
                self._usuarios.append(u)

        except FileNotFoundError:
            # Si el archivo no existe, iniciamos con una lista vacía
            self._usuarios = []
