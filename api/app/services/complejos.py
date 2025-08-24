from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.usuario import AccesoUsuario
from app.schemas.menus import MenuFiltroPlus
from app.services.menus import  getListMenus
from app.services.acceso import crear_acceso
from app.services.rol import getDatosRol
from app.services.empresa import getDatosEmpresa
from app.services.usuario import getDatosUsuarioXID
from app.schemas.complejos import AccesoDuracion, AccesoPagina, DatosAcceso
from app.models.models import Acceso
from app.utils.security import generar_jwt
from app.services.modulo import ListMenuXModulo
from app.services.dashboard_inicial import get_dashboard, get_dashboard_pagina


def getObjetoAcceso(db: Session, userid: int, empresaid: Optional[int] = None, token: Optional[str] = None) -> DatosAcceso:
    try:
        # Obtener datos del usuario
        oUsuario = getDatosUsuarioXID(db, userid)
        if not oUsuario:
            raise Exception(f"Usuario no encontrado: {userid}")


        oAccesoUsuario = AccesoUsuario(
            id = userid,
            username=oUsuario.username,
            email=oUsuario.email
        )
        
        # oPagina = AccesoPagina(
        #     dashboard=oUsuario.id_dashboard,
        #     inicio=oUsuario.pagina_inicio,
        # )

        minutosAcceso = oUsuario.duracion

        # Obtener empresas asociadas al usuario
        lEmpresas = getDatosEmpresa(db, userid)
        if not lEmpresas:
            raise Exception("No se encontraron empresas asociadas al usuario.")

        # Determinar empresa seleccionada
        idEmpresaSeleccionada = empresaid if empresaid is not None else lEmpresas[0].id

        # Obtener roles y módulos
        lRoles = getDatosRol(db, userid, idEmpresaSeleccionada)
        lModulos = ListMenuXModulo(db, idEmpresaSeleccionada, userid)

        # Obtener menús ordenados
        
        obj = MenuFiltroPlus(
            id_tipo_menu=1,    
            id_usuario=userid,    
            id_empresa=idEmpresaSeleccionada,    
            solo_activos=True,     
            ordenado=True          
        )
        lMenus = getListMenus(db, obj)

        # Generar token si no viene proporcionado
        if token is None:
            newToken = generar_jwt(userid, minutosAcceso)
            now = datetime.utcnow()
            db_acceso = Acceso(
                id_usuario=userid,
                id_empresa=idEmpresaSeleccionada,
                token=newToken,
                fecha_ingreso=now,
                fecha_creacion=now,
                fecha_vencimiento=now + timedelta(minutes=minutosAcceso),
            )
            crear_acceso(db, db_acceso)
        else:
            newToken = token

        duracion = AccesoDuracion(
            inicio=datetime.utcnow(),
            termino=datetime.utcnow() + timedelta(minutes=minutosAcceso),
            minutos=minutosAcceso,
        )

        # Construir objeto de acceso final
        return DatosAcceso(
            username=oUsuario.username,
            email=oUsuario.email,
            usuario=oAccesoUsuario,
            token=newToken,
            duracionAcceso=duracion,
            modulos=lModulos,
            empresas=lEmpresas,
            empresaSeleccionada=idEmpresaSeleccionada,
            roles=lRoles,
            menus=lMenus,
            pagina= AccesoPagina(
                inicio=oUsuario.pagina_inicio,
                dashboard=get_dashboard_pagina(db, oUsuario.id_dashboard),
            )
        )
    
    except Exception as e:
        print(f"Error en getObjetoAcceso: {e}")
        raise  # Relanzamos el error para que el controlador superior lo capture

def getNombreDashboard(db: Session, dashboardid: int) -> str:
    return get_dashboard(db,dashboardid)    
