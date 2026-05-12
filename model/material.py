class Material:
    #id_material es el identificador de dicho material, es decir, su codigo
    def __init__(self, id_material, titulo, autor, anio):
        self._id_material = id_material #atributos protegidos
        self._titulo = titulo
        self._autor = autor
        self._anio = anio
        self._disponible = True #por defecto el material estara disponible

    #@property crea un acceso controlado a un atributo
    #convierte el metodo titulo() en un archivo de solo lectura
    @property
    def titulo(self): # al poner def, titulo se convierte en un metodo
        return self._titulo

    @property
    def id_material(self):
        return self._id_material

    @property
    def autor(self):
        return self._autor

    @property
    def anio(self):
        return self._anio

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = valor

    def to_dict(self):
        return {
            "id_material": self._id_material,
            "titulo": self._titulo,
            "autor": self._autor,
            "anio": self._anio,
            "disponible": self._disponible,
            "tipo": "Material"
        }

#issn --> international standard serial number (es un identificador unico para publicaciones periodicas)
#ponemos los atributos protegidos para que solo puedan cambiarse dentro de la misma clase
class Revista(Material):
    def __init__(self, id_material, titulo, autor, anio, numero_edicion, mes_publicacion, issn):
        super().__init__(id_material, titulo, autor, anio)
        self._numero_edicion = numero_edicion
        self._mes_publicacion = mes_publicacion
        self._issn = issn

    def to_dict(self): #convierte el objeto en un diccionario (to_dict --> a diccionario)
        d = super().to_dict() #d es el diccionario que devuelve to_dict()
        d.update({
        "numero_edicion": self._numero_edicion,
        "mes_publicacion": self._mes_publicacion,
        "issn": self._issn,
        "tipo": "Revista"
    })
        return d #devolvemos el diccionario actualizado

class RecursoDigital(Material): #un recurso digital podria ser por ejemplo un video educativo
    def __init__(self, id_material, titulo, autor, anio, formato, tamanio_mb, url): #tamanio_mb es el tamaño en MB del recurso digital
        super().__init__(id_material, titulo, autor, anio) #recogemos los valores de la clase Material basica, no incluimos los especificos de la revista
        self._formato = formato
        self._tamanio_mb = tamanio_mb
        self._url = url

    @property
    def disponible(self):
        return True #segun las reglas siempre esta disponible el recurso digital

    @disponible.setter
    def disponible(self, valor):
        pass #los recursos digitales siempre estan disponibles, ignoramos el setter

    def to_dict(self):
        d = super().to_dict()
        d.update({ #actualizamos el diccionario otra vez esta vez aplicando los atributos de un recurso digital
            "url": self._url,
            "formato": self._formato,
            "tamanio_mb": self._tamanio_mb,
            "tipo": "RecursoDigital"
        })
        return d

class Libro(Material): #hasta anio todo se hereda de material
    def __init__(self, id_material, titulo, autor, anio, isbn, editorial, num_paginas):
        super().__init__(id_material, titulo, autor, anio)
        self._isbn = isbn
        self._editorial = editorial
        self._num_paginas = num_paginas

    def to_dict(self):
        d = super().to_dict()
        d.update({ #añadimos los nuevos datos al diccionario anterior
            "isbn": self._isbn,
            "editorial": self._editorial,
            "num_paginas": self._num_paginas,
            "tipo": "Libro"
        })
        return d
