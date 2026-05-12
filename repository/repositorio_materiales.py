import json
import os
from model.material import Libro, Revista, RecursoDigital #falta poner la clase general, que es model

class RepositorioMateriales: #donde se guardaran los materiales cargados
    def __init__(self, archivo='datos/materiales.json'):
        self._archivo = archivo
        self._materiales = [] #lista donde se guardaràn los objetos de: Libro, Revista, RecursoDigital

    def guardar(self): #guardamos todos los libros de la biblioteca en un formato JSON para tenerlos ordenados en texto
        """ Convierte todos los objetos materiales a diccionarios y los guarda en un JSON.""" #un JSON es un JavaScript Object Notation
        #JSON es un formato de texto que sirve para guardar datos de forma ordenada
        os.makedirs(os.path.dirname(self._archivo), exist_ok=True)
        with open(self._archivo, 'w', encoding='utf-8') as f: #abre un archivo para escribir dentro de él
        #'w' --> write --> modo escritura, crea un archivo si no existe
        #encoding = utf-8 --> utf-8 es el diccionario que dice a que numero representa cada letra, por ejemplo A = 65
        #'as f' llama al fichero abierto 'f'

            datos = [m.to_dict() for m in self._materiales] #convierte todos los objetos de la lista en diccionarios
            #m.to_dict() es un metodo que convierte cada material en un diccionario
            #self.materiales es la lista vacia que hemos inicializado anteriormente para guardar los materiales
            json.dump(datos, f, ensure_ascii=False, indent=4)
            #json.dump(datos, f) guarda los datos en formato JSON dentro de un fichero
            #ensure_ascii = False significa que permite caracteres especiales ya que ASCII no contiene ñ ni acentos ni emojis
            #indent = 4 --> el 4 viene de que añade sangria al texto, es decir, añade 4 espacios por nivel.
            #indent añade espacios y saltos de linea al texto para organizarlo.

    def cargar(self): #carga todos los materiales desde un archivo JSON al iniciar el programa
        """ Lee el JSON y reconstruye los objetos segun su tipo"""
        if not os.path.exists(self._archivo):  #si no existe una ruta para el archivo, es decir, si no existe
            return #salir

        with open(self._archivo, 'r', encoding='utf-8') as f: #abre un archivo para leer de él usando la codificacion utf-8
            datos = json.load(f) #cargar datos del fichero en formato json
            self._materiales = [] # creamos una lista vacia para los materiales de la biblioteca que vamos a cargar
            for item in datos: #para cada item en la lista datos
                tipo = item.pop('tipo', None) #.pop() saca el valor de la clave 'tipo' y si no existe devuelve 'None'
                #sacamos disponible antes de reconstruir porque no es parametro del constructor
                disponible = item.pop('disponible', True)
                if tipo == "Libro": #si el tipo es 'Libro'
                    m = Libro(**item) #entonces reconstruimos un libro(**item) y lo añadimos a la lista materiales
                    #lo reconstruimos con **item porque al convertirlo a JSON pasa de ser un objeto a un diccionario, por tanto para que vuelva
                    #a ser un un objeto y poder añadirlo lo tenemos que reconstruir.
                    m.disponible = disponible
                    self._materiales.append(m)
                elif tipo == "Revista": #si el tipo es una revista
                    m = Revista(**item) #lo reconstruimos y lo añadimos a la lista materiales
                    m.disponible = disponible
                    self._materiales.append(m)
                elif tipo == "RecursoDigital": #si el tipo es un recurso digital
                    m = RecursoDigital(**item) #reconstruimos dicho item y lo añadimos a la lista materiales.
                    #los recursos digitales ignoran el setter de disponible, siempre estan disponibles
                    self._materiales.append(m)

    def agregar(self, objeto):
        for material in self._materiales:
            if material.id_material == objeto.id_material:
                raise ValueError("Ya existe un material con ese ID")
        self._materiales.append(objeto)

    def obtener(self, id):
        for material in self._materiales:
            if material.id_material == id:
                return material
        raise Exception(f"Material con ID {id} no encontrado.")

    def eliminar(self, id):
        """ elimina un material segun su ID"""
        material = self.obtener(id)  #obtener ya lanza excepcion si no existe
        self._materiales.remove(material)

    def listar_todos(self):
        """ Devuelve todos los materiales """
        return self._materiales

    def listar_disponibles(self):
        """ devuelve solo los materiales disponibles"""
        disponibles = []
        for material in self._materiales:
            if material.disponible:
                disponibles.append(material)
        return disponibles

    def buscar(self, texto):
        """busca materiales por titulo o autor """
        resultados = []
        for material in self._materiales: #para cada material en la lista de materiales
            if (texto.lower() in material.titulo.lower() or
                texto.lower() in material.autor.lower()):
                resultados.append(material)
        return resultados
