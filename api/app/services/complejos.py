from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.services.menu import getDatosMenuGenerales
from app.services.acceso import crear_acceso
from app.services.rol import getDatosRol
from app.services.empresa import getDatosEmpresa
from app.services.usuario import getDatosUsuarioXID
from app.schemas.auth import UsuarioLogin
from app.models.models import Acceso, Usuario


from app.utils.security import generar_jwt



from app.schemas.complejos import AccesoDuracion, DatosAcceso


def getObjetoAcceso(db: Session, userid:int, empresaid: Optional[int] = None , token: Optional[str] = None ) -> DatosAcceso:
    
    oUsuario = getDatosUsuarioXID(db, userid);
    if not oUsuario:
        raise Exception("Usuario no encontrado ${userid}`")

    idUsuario = oUsuario.id
    minutosAcceso = oUsuario.duracion
    
    lEmpresas = getDatosEmpresa(db, idUsuario);
    if not lEmpresas:
        raise Exception("Empresas no encontrada")
    
    if(empresaid==None):
        idEmpresaSeleccionada = lEmpresas[0].id;
    else:
        idEmpresaSeleccionada = empresaid;

    lRoles = getDatosRol(db, idUsuario, idEmpresaSeleccionada);
    if not lEmpresas:
        raise Exception("Empresas no encontrada")
    
    lMenusGenerales = getDatosMenuGenerales(db, idUsuario, idEmpresaSeleccionada)

    
    
    # Se genera el Token
    if token == None:
        newToken = generar_jwt(idUsuario, minutosAcceso)
        db_acceso = Acceso(
            usuario_id=idUsuario,
            empresa_id=None,
            token=newToken,
            fecha_ingreso=datetime.now(),
            fecha_creacion=datetime.now(),
            fecha_vencimiento=datetime.now() + timedelta(minutes=minutosAcceso),
        )   
        crear_acceso(db, db_acceso)             
    else:
        newToken = token


    duracion = AccesoDuracion(
        inicio = datetime.now(),
        termino = datetime.now()+ timedelta(minutes=minutosAcceso),
        minutos = minutosAcceso
    )
    

    return DatosAcceso(
        username = oUsuario.username,
        email = oUsuario.email,
        token = newToken,
        duracionAcceso = duracion, 
        usuario = oUsuario,
        empresas = lEmpresas,
        empresaSeleccionada= idEmpresaSeleccionada,
        roles = lRoles,
        menusGenerales = lMenusGenerales
    )

    


