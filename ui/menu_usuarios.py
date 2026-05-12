from util.helpers import separador, confirmar
from model.usuario import Socio, Bibliotecario

def menu_usuarios(servicio_catalogo, servicio_sanciones):
    while True:
        separador("Gestion de usuarios")
        print("1. Anadir socio")
        print("2. Anadir bibliotecario")
        print("3. Listar usuarios")
        print("4. Ver detalle usuario")
        print("5. Dar de baja usuario")
        print("6. Levantar sancion")
        print("0. Volver")
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "1":
            anadir_socio(servicio_catalogo)
        elif opcion == "2":
            anadir_bibliotecario(servicio_catalogo)
        elif opcion == "3":
            listar_usuarios(servicio_catalogo)
        elif opcion == "4":
            ver_detalle_usuario(servicio_catalogo)
        elif opcion == "5":
            dar_baja_usuario(servicio_catalogo)
        elif opcion == "6":
            levantar_sancion(servicio_catalogo, servicio_sanciones)
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")


def anadir_socio(servicio_catalogo):
    separador("Anadir socio")
    try:
        id_usuario = input("ID (ej: U001): ").strip()
        nombre = input("Nombre: ").strip()
        email = input("Email: ").strip()
        socio = Socio(id_usuario, nombre, email)
        servicio_catalogo.registrar_usuario(socio)
        print(f"\nSocio '{nombre}' anadido correctamente.")
    except Exception as e:
        print(f"Error: {e}")


def anadir_bibliotecario(servicio_catalogo):
    separador("Anadir bibliotecario")
    try:
        id_usuario = input("ID (ej: B001): ").strip()
        nombre = input("Nombre: ").strip()
        email = input("Email: ").strip()
        num_empleado = input("Numero de empleado (ej: EMP042): ").strip()
        bibliotecario = Bibliotecario(id_usuario, nombre, email, num_empleado)
        servicio_catalogo.registrar_usuario(bibliotecario)
        print(f"\nBibliotecario '{nombre}' anadido correctamente.")
    except Exception as e:
        print(f"Error: {e}")


def listar_usuarios(servicio_catalogo):
    separador("Lista de usuarios")
    try:
        usuarios = servicio_catalogo.listar_usuarios()
        if not usuarios:
            print("No hay usuarios registrados.")
            return
        for u in usuarios:
            tipo = type(u).__name__
            extra = ""
            if isinstance(u, Socio):
                if u.sancionado:
                    extra = f" | SANCIONADO hasta {u.fecha_fin_sancion}"
                else:
                    extra = f" | prestamos activos: {len(u.prestamos_activos)}"
            print(f"  {u.id_usuario} | {u.nombre} | {u.email} | {tipo}{extra}")
    except Exception as e:
        print(f"Error: {e}")


def ver_detalle_usuario(servicio_catalogo):
    separador("Detalle de usuario")
    try:
        id_usuario = input("ID del usuario: ").strip()
        u = servicio_catalogo.obtener_usuario(id_usuario)
        print(f"\n  ID:     {u.id_usuario}")
        print(f"  Nombre: {u.nombre}")
        print(f"  Email:  {u.email}")
        print(f"  Tipo:   {type(u).__name__}")
        if isinstance(u, Socio):
            print(f"  Sancionado: {'Si' if u.sancionado else 'No'}")
            if u.sancionado and u.fecha_fin_sancion:
                print(f"  Sancion hasta: {u.fecha_fin_sancion}")
            print(f"  Prestamos activos ({len(u.prestamos_activos)}): {u.prestamos_activos if u.prestamos_activos else 'ninguno'}")
        elif isinstance(u, Bibliotecario):
            print(f"  Num. empleado: {u.num_empleado}")
    except Exception as e:
        print(f"Error: {e}")


def dar_baja_usuario(servicio_catalogo):
    separador("Dar de baja usuario")
    try:
        id_usuario = input("ID del usuario (ej: U001): ").strip()
        if confirmar(f"Seguro que quieres dar de baja al usuario {id_usuario}?"):
            servicio_catalogo.dar_baja_usuario(id_usuario)
            print(f"\nUsuario {id_usuario} dado de baja correctamente.")
        else:
            print("Operacion cancelada.")
    except Exception as e:
        print(f"Error: {e}")


def levantar_sancion(servicio_catalogo, servicio_sanciones):
    separador("Levantar sancion")
    try:
        id_usuario = input("ID del usuario sancionado: ").strip()
        u = servicio_catalogo.obtener_usuario(id_usuario)
        if not isinstance(u, Socio):
            print("Este usuario no es un socio, no puede tener sanciones.")
            return
        if not u.sancionado:
            print(f"El usuario {id_usuario} no tiene ninguna sancion activa.")
            return
        print(f"  {u.nombre} tiene sancion hasta: {u.fecha_fin_sancion}")
        if confirmar("Seguro que quieres levantar la sancion?"):
            servicio_sanciones.levantar_sancion(id_usuario)
            print(f"\nSancion levantada. El usuario {id_usuario} puede volver a pedir prestamos.")
        else:
            print("Operacion cancelada.")
    except Exception as e:
        print(f"Error: {e}")
