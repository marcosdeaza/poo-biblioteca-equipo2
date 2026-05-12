#Servicio de sanciones - Marcos
#Este servicio gestiona las sanciones de los socios

from datetime import date, timedelta
from model.usuario import Socio

DIAS_SANCION_POR_DIA_RETRASO = 1  #por cada dia de retraso, un dia de sancion

class ServicioSanciones:
    def __init__(self, repo_usuarios):
        self._repo_usuarios = repo_usuarios

    def sancionar(self, id_usuario, dias_retraso):
        #buscamos al usuario
        usuario = self._repo_usuarios.obtener(id_usuario)
        #solo los socios pueden ser sancionados
        if not isinstance(usuario, Socio):
            return 0
        dias_sancion = dias_retraso * DIAS_SANCION_POR_DIA_RETRASO
        usuario.sancionado = True
        usuario.fecha_fin_sancion = date.today() + timedelta(days=dias_sancion)
        return dias_sancion

    def levantar_sancion(self, id_usuario):
        usuario = self._repo_usuarios.obtener(id_usuario)
        if isinstance(usuario, Socio):
            usuario.sancionado = False
            usuario.fecha_fin_sancion = None

    def revisar_sanciones_expiradas(self):
        #revisamos todos los usuarios al arrancar para ver si alguna sancion ha terminado
        usuarios = self._repo_usuarios.listar_todos()
        for u in usuarios:
            if isinstance(u, Socio) and u.sancionado:
                if u.fecha_fin_sancion and u.fecha_fin_sancion <= date.today():
                    u.sancionado = False
                    u.fecha_fin_sancion = None

    def usuarios_sancionados(self):
        usuarios = self._repo_usuarios.listar_todos()
        #devolvemos solo los socios que esten sancionados
        return [u for u in usuarios if isinstance(u, Socio) and u.sancionado]
