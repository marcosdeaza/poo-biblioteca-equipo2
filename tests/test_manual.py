import sys
import os
#añadimos la raiz del proyecto al path para que los imports funcionen
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date, timedelta

print("=" * 40)
print("PRUEBAS MANUALES - OpenBook")
print("=" * 40)

errores = 0

def ok(mensaje):
    print(f"  [OK] {mensaje}")

def fallo(mensaje):
    global errores
    errores += 1
    print(f"  [FALLO] {mensaje}")

# TEST 1 - Crear libro
print("\nTEST 1: Crear libro")
try:
    from model.material import Libro
    libro = Libro("L001", "Don Quijote", "Cervantes", 1605, "978-0", "Anaya", 400)
    assert libro.titulo == "Don Quijote"
    assert libro.autor == "Cervantes"
    assert libro.disponible == True
    ok("Clase Libro creada correctamente ")
except Exception as e:
    fallo(f"Error creando libro: {e}")

# TEST 2 - Duplicado lanza excepcion
print("\nTEST 2: Duplicado lanza excepcion")
try:
    from repository.repositorio_materiales import RepositorioMateriales
    from model.material import Libro
    repo_test = RepositorioMateriales()
    libro_dup = Libro("L001", "Don Quijote", "Cervantes", 1605, "978-0", "Anaya", 400)
    repo_test.agregar(libro_dup)
    #intentamos agregar el mismo libro otra vez, tiene que fallar
    try:
        repo_test.agregar(libro_dup)
        fallo("No lanzo excepcion para duplicado")
    except Exception:
        ok("Duplicado lanza excepcion ")
except Exception as e:
    fallo(f"Error inesperado: {e}")

# TEST 3 - No encontrado lanza excepcion
print("\nTEST 3: No encontrado lanza excepcion")
try:
    from repository.repositorio_materiales import RepositorioMateriales
    repo_test2 = RepositorioMateriales()
    #intentamos obtener un id que no existe
    try:
        repo_test2.obtener("ID_QUE_NO_EXISTE")
        fallo("No lanzo excepcion para no encontrado")
    except Exception:
        ok("No encontrado lanza excepcion ")
except Exception as e:
    fallo(f"Error inesperado: {e}")

# TEST 4 - Socio sancionado no puede pedir prestamo
print("\nTEST 4: Socio sancionado no puede pedir prestamo")
try:
    from model.usuario import Socio
    socio = Socio("U001", "Juan", "juan@test.com")
    socio.sancionado = True
    #un socio sancionado no deberia poder pedir prestamo
    assert socio.puede_pedir_prestamo() == False
    ok("Socio sancionado bloqueado correctamente ")
except Exception as e:
    fallo(f"Error: {e}")

# TEST 5 - Prestamo vencido
print("\nTEST 5: Prestamo vencido")
try:
    from model.prestamo import Prestamo
    p = Prestamo("P0001", "U001", "L001")
    #ponemos la fecha limite en el pasado para simular que esta vencido
    p._fecha_limite = date.today() - timedelta(days=1)
    assert p.esta_vencido() == True
    ok("Prestamo vencido detectado correctamente ")
except Exception as e:
    fallo(f"Error: {e}")

# TEST 6 - Devolver tarde genera sancion-
print("\nTEST 6: Devolver tarde genera sancion")
try:
    from model.prestamo import Prestamo
    p = Prestamo("P0002", "U001", "L001")
    #simulamos que la fecha limite fue hace 3 dias
    p._fecha_limite = date.today() - timedelta(days=3)
    p.devolver()
    dias = p.dias_retraso()
    assert dias == 3
    ok("Devolucion tarde genera sancion ")
except Exception as e:
    fallo(f"Error: {e}")

# TEST 7 - Limite de prestamos
print("\nTEST 7: Limite de prestamos")
try:
    from model.usuario import Socio
    socio = Socio("U002", "Maria", "maria@test.com")
    #llenamos la lista hasta el maximo de prestamos
    socio._prestamos_activos = ["P0001", "P0002", "P0003"]
    assert socio.puede_pedir_prestamo() == False
    ok("Limite de prestamos funciona ")
except Exception as e:
    fallo(f"Error: {e}")

# TEST 8 - Reservar material no disponible
print("\nTEST 8: Reservar material no disponible")
try:
    from model.material import Libro
    from model.usuario import Socio
    from repository.repositorio_materiales import RepositorioMateriales
    from repository.repositorio_usuarios import RepositorioUsuarios
    from repository.repositorio_prestamos import RepositorioPrestamos
    from service.servicio_prestamos import ServicioPrestamos

    repo_m = RepositorioMateriales()
    repo_u = RepositorioUsuarios()
    repo_p = RepositorioPrestamos()

    libro8 = Libro("L008", "El Principito", "Saint-Exupery", 1943, "978-1", "Salamandra", 100)
    socio8 = Socio("U008", "Pedro", "pedro@test.com")
    repo_m.agregar(libro8)
    repo_u.agregar(socio8)

    libro8.disponible = False  #simulamos que el libro esta prestado

    servicio = ServicioPrestamos(repo_u, repo_m, repo_p)
    reserva = servicio.reservar("U008", "L008")
    assert reserva.id_reserva.startswith("V")
    assert reserva.activa == True
    ok("Reserva creada correctamente ")
except Exception as e:
    fallo(f"Error: {e}")

# TEST 9 - Guardar JSON y recargar
print("\nTEST 9: Guardar JSON y recargar")
try:
    from model.material import Libro
    from repository.repositorio_materiales import RepositorioMateriales

    #usamos un archivo temporal para no tocar los datos reales
    archivo_temp = "datos/_test_temp.json"
    os.makedirs("datos", exist_ok=True)

    repo1 = RepositorioMateriales(archivo=archivo_temp)
    libro9 = Libro("L999", "Libro de prueba", "Autor Test", 2020, "000-0", "Ed. Test", 100)
    repo1.agregar(libro9)
    repo1.guardar()

    #cargamos en un repositorio nuevo para ver si los datos se guardaron bien
    repo2 = RepositorioMateriales(archivo=archivo_temp)
    repo2.cargar()
    m = repo2.obtener("L999")
    assert m.titulo == "Libro de prueba"
    assert m.autor == "Autor Test"

    #borramos el archivo temporal
    os.remove(archivo_temp)
    ok("Persistencia JSON funciona ")
except Exception as e:
    fallo(f"Error: {e}")

# RESULTADO FINAL
print("\n" + "=" * 40)
if errores == 0:
    print("TODOS LOS TESTS PASARON")
else:
    print(f"{errores} TEST(S) FALLARON")
print("=" * 40)
