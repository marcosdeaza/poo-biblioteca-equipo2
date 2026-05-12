#main.py - OpenBook
#Marcos - punto de entrada del programa
#Aqui se conecta todo: repositorios, servicios y menus

from repository.repositorio_materiales import RepositorioMateriales
from repository.repositorio_usuarios import RepositorioUsuarios
from repository.repositorio_prestamos import RepositorioPrestamos
from service.servicio_catalogo import ServicioCatalogo
from service.servicio_prestamos import ServicioPrestamos
from service.servicio_sanciones import ServicioSanciones
from ui.menu_principal import menu_principal

def main():
    print("Iniciando OpenBook...")

    #creamos los repositorios (donde se guardan los datos)
    repo_materiales = RepositorioMateriales()
    repo_usuarios = RepositorioUsuarios()
    repo_prestamos = RepositorioPrestamos()

    #cargamos los datos guardados si existen
    repo_materiales.cargar()
    repo_usuarios.cargar()
    repo_prestamos.cargar()

    #revisamos si alguna sancion ha expirado desde la ultima vez que se abrio el programa
    servicio_sanciones = ServicioSanciones(repo_usuarios)
    servicio_sanciones.revisar_sanciones_expiradas()

    #creamos los servicios pasandoles los repositorios que necesitan
    servicio_catalogo = ServicioCatalogo(repo_materiales, repo_usuarios)
    servicio_prestamos_obj = ServicioPrestamos(repo_usuarios, repo_materiales, repo_prestamos)

    #arrancamos el menu principal
    menu_principal(servicio_catalogo, servicio_prestamos_obj, servicio_sanciones)

    #al salir guardamos todo
    print("\nGuardando datos...")
    repo_materiales.guardar()
    repo_usuarios.guardar()
    repo_prestamos.guardar()
    print("Hasta luego!")

if __name__ == "__main__":
    main()
