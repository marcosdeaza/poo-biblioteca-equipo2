#repositorio_prestamos.py - Marcos
#Este repositorio guarda y carga los prestamos y reservas en archivos JSON

import json
import os
from datetime import date
from model.prestamo import Prestamo, Reserva

class RepositorioPrestamos:
    def __init__(self):
        self._prestamos = []  #lista con todos los prestamos
        self._reservas = []   #lista con todas las reservas
        self._archivo_prestamos = "datos/prestamos.json"
        self._archivo_reservas = "datos/reservas.json"

    def agregar(self, prestamo):
        #comprobamos que no haya otro prestamo con el mismo id
        for p in self._prestamos:
            if p.id_prestamo == prestamo.id_prestamo:
                raise Exception(f"Ya existe un prestamo con id {prestamo.id_prestamo}")
        self._prestamos.append(prestamo)

    def obtener(self, id_prestamo):
        #buscamos el prestamo por su id
        for p in self._prestamos:
            if p.id_prestamo == id_prestamo:
                return p
        raise Exception(f"Prestamo con id {id_prestamo} no encontrado.")

    def eliminar(self, id_prestamo):
        self._prestamos = [p for p in self._prestamos if p.id_prestamo != id_prestamo]

    def listar_todos(self):
        #devolvemos todos los prestamos
        return self._prestamos

    def listar_activos(self):
        #devolvemos solo los que no han sido devueltos todavia
        return [p for p in self._prestamos if not p.devuelto]

    def listar_vencidos(self):
        #devolvemos los que han superado la fecha limite
        return [p for p in self._prestamos if p.esta_vencido()]

    def listar_por_usuario(self, id_usuario):
        #devolvemos los prestamos de un usuario concreto
        return [p for p in self._prestamos if p.id_usuario == id_usuario]

    def agregar_reserva(self, reserva):
        self._reservas.append(reserva)

    def obtener_reserva(self, id_reserva):
        for r in self._reservas:
            if r.id_reserva == id_reserva:
                return r
        raise Exception(f"Reserva con id {id_reserva} no encontrada.")

    def listar_reservas(self):
        return self._reservas

    def listar_reservas_material(self, id_material):
        #devolvemos las reservas activas de un material concreto
        return [r for r in self._reservas if r.id_material == id_material and r.activa]

    def guardar(self):
        #guardamos los prestamos y reservas en sus archivos JSON
        os.makedirs(os.path.dirname(self._archivo_prestamos), exist_ok=True)

        with open(self._archivo_prestamos, 'w', encoding='utf-8') as f:
            datos = [p.to_dict() for p in self._prestamos]
            json.dump(datos, f, ensure_ascii=False, indent=4)

        with open(self._archivo_reservas, 'w', encoding='utf-8') as f:
            datos = [r.to_dict() for r in self._reservas]
            json.dump(datos, f, ensure_ascii=False, indent=4)

    def cargar(self):
        #cargamos los prestamos del archivo JSON si existe
        if os.path.exists(self._archivo_prestamos):
            with open(self._archivo_prestamos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            for item in datos:
                #reconstruimos el prestamo y le ponemos las fechas del JSON
                p = Prestamo(item["id_prestamo"], item["id_usuario"], item["id_material"])
                p._fecha_prestamo = date.fromisoformat(item["fecha_prestamo"])
                p._fecha_limite = date.fromisoformat(item["fecha_limite"])
                if item["fecha_devolucion"]:
                    p._fecha_devolucion = date.fromisoformat(item["fecha_devolucion"])
                p._devuelto = item["devuelto"]
                self._prestamos.append(p)

        #cargamos las reservas del archivo JSON si existe
        if os.path.exists(self._archivo_reservas):
            with open(self._archivo_reservas, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            for item in datos:
                r = Reserva(item["id_reserva"], item["id_usuario"], item["id_material"])
                r._fecha_reserva = date.fromisoformat(item["fecha_reserva"])
                r.activa = item.get("activa", True)
                if item.get("fecha_disponible"):
                    r.fecha_disponible = date.fromisoformat(item["fecha_disponible"])
                self._reservas.append(r)
