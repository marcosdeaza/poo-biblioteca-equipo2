#menu_informes.py - Marcos
#Menu de informes y estadisticas de la biblioteca

from util.helpers import separador

def menu_informes(servicio_catalogo, servicio_prestamos, servicio_sanciones):
    while True:
        separador("Informes")
        print("1. Materiales disponibles")
        print("2. Todos los materiales")
        print("3. Prestamos vencidos")
        print("4. Usuarios sancionados")
        print("0. Volver")
        opcion = input("\nElige una opcion: ").strip()

        if opcion == "1":
            ver_disponibles(servicio_catalogo)
        elif opcion == "2":
            ver_todos_materiales(servicio_catalogo)
        elif opcion == "3":
            ver_prestamos_vencidos(servicio_prestamos)
        elif opcion == "4":
            ver_sancionados(servicio_sanciones)
        elif opcion == "0":
            break
        else:
            print("Opcion no valida.")


def ver_disponibles(servicio_catalogo):
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


def ver_todos_materiales(servicio_catalogo):
    separador("Todos los materiales del catalogo")
    try:
        materiales = servicio_catalogo.listar_todos()
        if not materiales:
            print("No hay materiales en el catalogo.")
            return
        disponibles = [m for m in materiales if m.disponible]
        prestados = [m for m in materiales if not m.disponible]
        print(f"Total: {len(materiales)} | Disponibles: {len(disponibles)} | Prestados: {len(prestados)}\n")
        for m in materiales:
            estado = "disponible" if m.disponible else "prestado"
            tipo = type(m).__name__
            print(f"  {m.id_material} | {m.titulo} | {m.autor} | {tipo} | [{estado}]")
    except Exception as e:
        print(f"Error: {e}")


def ver_prestamos_vencidos(servicio_prestamos):
    separador("Prestamos vencidos")
    try:
        vencidos = servicio_prestamos.listar_vencidos()
        if not vencidos:
            print("No hay prestamos vencidos.")
            return
        #mostramos cada prestamo vencido con su info
        for p in vencidos:
            print(f"  {p.id_prestamo} | Usuario: {p.id_usuario} | Material: {p.id_material} | Limite: {p.fecha_limite}")
    except Exception as e:
        print(f"Error: {e}")


def ver_sancionados(servicio_sanciones):
    separador("Usuarios sancionados")
    try:
        sancionados = servicio_sanciones.usuarios_sancionados()
        if not sancionados:
            print("No hay usuarios sancionados.")
            return
        for u in sancionados:
            print(f"  {u.id_usuario} | {u.nombre} | Sancion hasta: {u.fecha_fin_sancion}")
    except Exception as e:
        print(f"Error: {e}")
