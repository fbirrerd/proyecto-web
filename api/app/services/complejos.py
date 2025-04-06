from datetime import datetime, timedelta
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.services.usuario_empresa import obtener_empresas_por_usuario
from app.models.empresa import Empresa
from app.utils.security import generar_jwt
from app.services.acceso import create_acceso
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin
from app.schemas.complejos import AccesoDuracion, DatosAcceso
from app.models.acceso import Acceso  # Corregir la importación

def get_objeto_acceso(db: Session, user: UsuarioLogin) -> DatosAcceso:
    #traer la informacion del usuario
    # Buscar el usuario con el nombre de usuario proporcionado

    userObj = db.query(Usuario).filter(
        or_(Usuario.nombre_usuario == user.userName, 
            Usuario.email == user.userName)
        ).first()
    if not userObj:
        raise Exception("Usuario no encontrado")
    
    idUsuario = userObj.id
    minutosAcceso = userObj.duracion

    # Se genera el Token
    newToken = generar_jwt(idUsuario, minutosAcceso)
        
    # Crear el acceso
    db_acceso = Acceso(
        usuario_id=idUsuario,
        empresa_id=None,
        token=newToken,
        fecha_ingreso=datetime.now(),
        fecha_creacion=datetime.now(),
        fecha_vencimiento=datetime.now() + timedelta(minutes=minutosAcceso),
    )
    # retornar el token
    objAcceso = create_acceso(db, db_acceso)
    #retornar los roles
    #crear el super objeto

    empresaList = obtener_empresas_por_usuario(db, idUsuario)
    
    duracion = AccesoDuracion(
        inicio = datetime.now(),
        termino = datetime.now()+ timedelta(minutes=minutosAcceso),
        minutos = minutosAcceso
    )
    return DatosAcceso(
        nombre_usuario = userObj.nombre_usuario,
        email = userObj.email,
        token = objAcceso.token,
        duracionAcceso = duracion, 
        empresas = empresaList,  # Lista de empresas
        empresaSeleccionada= empresaList[0].id
    )

    


