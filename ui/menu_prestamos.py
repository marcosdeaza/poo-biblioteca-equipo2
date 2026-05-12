from util.helpers import separador

def menu_prestamos(servicio_prestamos):
    while True:
        separador("Gestion de prestamos")
        print("1. Prestar material")
        print("2. Devolver material")
        print("3. Reservar material")
        print("4. Cancelar reserva")
        print("5. Ver prestamos activos")
        print("6. Ver reservas activas")
        print("7. Cancelar prestamo")
        print("0. Volver")
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "1":
            prestar(servicio_prestamos)
        elif opcion == "2":
            devolver(servicio_prestamos)
        elif opcion == "3":
            reservar(servicio_prestamos)
        elif opcion == "4":
            cancelar_reserva(servicio_prestamos)
        elif opcion == "5":
            ver_activos(servicio_prestamos)
        elif opcion == "6":
            ver_reservas(servicio_prestamos)
        elif opcion == "7":
            cancelar_prestamo(servicio_prestamos)
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")


def prestar(servicio_prestamos):
    separador("Prestar material")
    try:
        id_usuario = input("ID del usuario (ej: U001): ").strip()
        id_material = input("ID del material (ej: L001): ").strip()
        prestamo = servicio_prestamos.prestar(id_usuario, id_material)
        print(f"\nPrestamo creado correctamente. ID: {prestamo.id_prestamo}")
        print(f"Fecha limite de devolucion: {prestamo.fecha_limite}")
    except Exception as e:
        print(f"Error: {e}")


def devolver(servicio_prestamos):
    separador("Devolver material")
    try:
        id_prestamo = input("ID del prestamo (ej: P0001): ").strip()
        dias_retraso = servicio_prestamos.devolver(id_prestamo)
        if dias_retraso > 0:
            print(f"\nDevolucion registrada. Retraso de {dias_retraso} dias. Se aplica sancion.")
        else:
            print("\nDevolucion registrada a tiempo. Sin sancion.")
    except Exception as e:
        print(f"Error: {e}")


def reservar(servicio_prestamos):
    separador("Reservar material")
    try:
        id_usuario = input("ID del usuario (ej: U001): ").strip()
        id_material = input("ID del material (ej: L001): ").strip()
        reserva = servicio_prestamos.reservar(id_usuario, id_material)
        print(f"\nReserva creada correctamente. ID: {reserva.id_reserva}")
    except Exception as e:
        print(f"Error: {e}")


def cancelar_reserva(servicio_prestamos):
    separador("Cancelar reserva")
    try:
        id_reserva = input("ID de la reserva (ej: V0001): ").strip()
        servicio_prestamos.cancelar_reserva(id_reserva)
        print(f"\nReserva {id_reserva} cancelada correctamente.")
    except Exception as e:
        print(f"Error: {e}")


def ver_activos(servicio_prestamos):
    separador("Prestamos activos")
    try:
        activos = servicio_prestamos.listar_activos()
        if not activos:
            print("No hay prestamos activos en este momento.")
            return
        print(f"{len(activos)} prestamo(s) activo(s):\n")
        for p in activos:
            vencido = " [VENCIDO]" if p.esta_vencido() else ""
            print(f"  {p.id_prestamo} | Usuario: {p.id_usuario} | Material: {p.id_material} | Limite: {p.fecha_limite}{vencido}")
    except Exception as e:
        print(f"Error: {e}")


def ver_reservas(servicio_prestamos):
    separador("Reservas activas")
    try:
        reservas = servicio_prestamos.listar_reservas()
        activas = [r for r in reservas if r.activa]
        if not activas:
            print("No hay reservas activas en este momento.")
            return
        print(f"{len(activas)} reserva(s) activa(s):\n")
        for r in activas:
            print(f"  {r.id_reserva} | Usuario: {r.id_usuario} | Material: {r.id_material} | Fecha: {r._fecha_reserva}")
    except Exception as e:
        print(f"Error: {e}")


def cancelar_prestamo(servicio_prestamos):
    separador("Cancelar prestamo")
    try:
        id_prestamo = input("ID del prestamo a cancelar (ej: P0001): ").strip()
        servicio_prestamos.cancelar_prestamo(id_prestamo)
        print(f"\nPrestamo {id_prestamo} cancelado. Material vuelve a estar disponible.")
    except Exception as e:
        print(f"Error: {e}")
