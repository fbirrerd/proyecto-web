
from app.schemas.rol import RolAcceso
from app.models.models import Rol, UsuarioEmpresaRol
from app.utils.password import get_password_hash, verify_password
from sqlalchemy.orm import Session


from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta


def getDatosRol(db: Session, UsuarioId: int, EmpresaId: int):
    userEmpRolList = db.query(UsuarioEmpresaRol).filter(
        and_(UsuarioEmpresaRol.id_usuario == UsuarioId, 
             UsuarioEmpresaRol.id_empresa == EmpresaId,
             UsuarioEmpresaRol.estado == True)
    ).all()
    if not userEmpRolList:
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")
    
    roles_ids = [item.id_rol for item in userEmpRolList]
    
    rolList = db.query(Rol).filter(Rol.id.in_(roles_ids)).all()
    
    if not rolList:
        raise Exception("Roles no encontrados")
    
    # Si hay empresas, las convertimos a Pydantic
    rol_pydantic_list = [RolAcceso.from_orm(empresa) for empresa in rolList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if rol_pydantic_list:
        return rol_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
