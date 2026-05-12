from util.helpers import pedir_int, pedir_float, separador, confirmar
from model.material import Libro, Revista, RecursoDigital

def menu_materiales(servicio_catalogo):
    while True:
        separador("Gestion de materiales")
        print("1. Anadir libro")
        print("2. Anadir revista")
        print("3. Anadir recurso digital")
        print("4. Listar materiales disponibles")
        print("5. Listar todos los materiales")
        print("6. Buscar material")
        print("7. Dar de baja material")
        print("0. Volver")
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "1":
            anadir_libro(servicio_catalogo)
        elif opcion == "2":
            anadir_revista(servicio_catalogo)
        elif opcion == "3":
            anadir_recurso_digital(servicio_catalogo)
        elif opcion == "4":
            listar_disponibles(servicio_catalogo)
        elif opcion == "5":
            listar_todos(servicio_catalogo)
        elif opcion == "6":
            buscar_material(servicio_catalogo)
        elif opcion == "7":
            dar_baja_material(servicio_catalogo)
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")


def anadir_libro(servicio_catalogo):
    separador("Anadir libro")
    try:
        id_material = input("ID (ej: L001): ").strip()
        titulo = input("Titulo: ").strip()
        autor = input("Autor: ").strip()
        anio = pedir_int("Año: ")
        isbn = input("ISBN: ").strip()
        editorial = input("Editorial: ").strip()
        num_paginas = pedir_int("Numero de paginas: ")
        libro = Libro(id_material, titulo, autor, anio, isbn, editorial, num_paginas)
        servicio_catalogo.alta_material(libro)
        print(f"\nLibro '{titulo}' anadido correctamente.")
    except Exception as e:
        print(f"Error: {e}")


def anadir_revista(servicio_catalogo):
    separador("Anadir revista")
    try:
        id_material = input("ID (ej: R001): ").strip()
        titulo = input("Titulo: ").strip()
        autor = input("Autor: ").strip()
        anio = pedir_int("Año: ")
        numero_edicion = pedir_int("Numero de edicion: ")
        mes_publicacion = input("Mes de publicacion: ").strip()
        issn = input("ISSN: ").strip()
        revista = Revista(id_material, titulo, autor, anio, numero_edicion, mes_publicacion, issn)
        servicio_catalogo.alta_material(revista)
        print(f"\nRevista '{titulo}' anadida correctamente.")
    except Exception as e:
        print(f"Error: {e}")


def anadir_recurso_digital(servicio_catalogo):
    separador("Anadir recurso digital")
    try:
        id_material = input("ID (ej: D001): ").strip()
        titulo = input("Titulo: ").strip()
        autor = input("Autor: ").strip()
        anio = pedir_int("Año: ")
        url = input("URL: ").strip()
        formato = input("Formato (pdf/ebook/video): ").strip().lower()
        while formato not in ("pdf", "ebook", "video"):
            print("Formato no valido. Escribe pdf, ebook o video.")
            formato = input("Formato (pdf/ebook/video): ").strip().lower()
        tamanio_mb = pedir_float("Tamanio en MB: ")
        recurso = RecursoDigital(id_material, titulo, autor, anio, formato, tamanio_mb, url)
        servicio_catalogo.alta_material(recurso)
        print(f"\nRecurso digital '{titulo}' anadido correctamente.")
    except Exception as e:
        print(f"Error: {e}")


def listar_disponibles(servicio_catalogo):
    separador("Materiales disponibles")
    try:
        materiales = servicio_catalogo.listar_disponibles()
        if not materiales:
            print("No hay materiales disponibles.")
            return
        for m in materiales:
            print(f"  {m.id_material} | {m.titulo} | {m.autor}")
    except Exception as e:
        print(f"Error: {e}")


def listar_todos(servicio_catalogo):
    separador("Todos los materiales")
    try:
        materiales = servicio_catalogo.listar_todos()
        if not materiales:
            print("No hay materiales en el catalogo.")
            return
        for m in materiales:
            estado = "disponible" if m.disponible else "prestado"
            tipo = type(m).__name__
            print(f"  {m.id_material} | {m.titulo} | {m.autor} | {tipo} | [{estado}]")
    except Exception as e:
        print(f"Error: {e}")


def buscar_material(servicio_catalogo):
    separador("Buscar material")
    try:
        texto = input("Buscar por titulo o autor: ").strip()
        if not texto:
            print("Escribe algo para buscar.")
            return
        resultados = servicio_catalogo.buscar_materiales(texto)
        if not resultados:
            print(f"No se encontraron materiales con '{texto}'.")
            return
        print(f"\n{len(resultados)} resultado(s):")
        for m in resultados:
            estado = "disponible" if m.disponible else "prestado"
            print(f"  {m.id_material} | {m.titulo} | {m.autor} | [{estado}]")
    except Exception as e:
        print(f"Error: {e}")


def dar_baja_material(servicio_catalogo):
    separador("Dar de baja material")
    try:
        id_material = input("ID del material (ej: L001): ").strip()
        if confirmar(f"Seguro que quieres eliminar el material {id_material}?"):
            servicio_catalogo.baja_material(id_material)
            print(f"\nMaterial {id_material} eliminado correctamente.")
        else:
            print("Operacion cancelada.")
    except Exception as e:
        print(f"Error: {e}")
