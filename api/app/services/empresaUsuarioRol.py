
from app.schemas.rol import RolAcceso, RolCreate, RolUpdate
from app.models.models import Rol, EmpresaUsuarioRol
from sqlalchemy.orm import Session


from datetime import datetime, timezone
from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta


def getDatosEmpresaUsuarioRol(db: Session, UsuarioId: int, EmpresaId: int):
  
