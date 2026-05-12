from util.helpers import separador, limpiar
from ui.menu_materiales import menu_materiales
from ui.menu_usuarios import menu_usuarios
from ui.menu_prestamos import menu_prestamos
from ui.menu_informes import menu_informes

def menu_principal(servicio_catalogo, servicio_prestamos, servicio_sanciones):
    while True:
        limpiar()
        separador("OpenBook - Sistema de Biblioteca")
        print("1. Materiales")
        print("2. Usuarios")
        print("3. Prestamos")
        print("4. Informes")
        print("0. Salir")
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "1":
            menu_materiales(servicio_catalogo)
        elif opcion == "2":
            menu_usuarios(servicio_catalogo, servicio_sanciones)
        elif opcion == "3":
            menu_prestamos(servicio_prestamos)
        elif opcion == "4":
            menu_informes(servicio_catalogo, servicio_prestamos, servicio_sanciones)
        elif opcion == "0":
            print("\nHasta luego!")
            break
        else:
            print("Opcion no valida.")
