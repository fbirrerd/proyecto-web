

from sqlalchemy import func
from app.schemas.empresaUsuario import EmpresaUsuarioCreate, EmpresaUsuarioList, EmpresaUsuarioOut
from app.models.models import Empresa, EmpresaUsuario, Usuario
from sqlalchemy.orm import Session


from datetime import datetime, timezone


def getDatosEmpresaUsuario(db: Session):
    datos = (
        db.query(
            func.concat(Usuario.nombres, ' ', Usuario.apellidos).label("usuario_nombre"),
            Empresa.nombre.label("empresa_nombre"),
            Usuario.id.label("usuario_id"),
            Empresa.id.label("empresa_id"),
            EmpresaUsuario.estado.label("estado")
        )
        .join(EmpresaUsuario, Usuario.id == EmpresaUsuario.id_usuario)
        .join(Empresa, Empresa.id == EmpresaUsuario.id_empresa)
        .all()
    )
    return [EmpresaUsuarioList.from_orm(r) for r in datos]
  
def setEmpresaUsuario(db: Session, oCrear: EmpresaUsuarioCreate) -> EmpresaUsuarioOut:
    # Buscar si ya existe la relación
    existe = db.query(EmpresaUsuario).filter_by(
        id_empresa=oCrear.id_empresa,
        id_usuario=oCrear.id_usuario
    ).first()

    if existe:
        # Si existe, actualizar el estado
        existe.estado = oCrear.estado
        db.commit()
        db.refresh(existe)
        return EmpresaUsuarioOut.from_orm(existe)
    else:
        # Si no existe, crear una nueva relación
        nueva_relacion = EmpresaUsuario(
            id_empresa=oCrear.id_empresa,
            id_usuario=oCrear.id_usuario,
            estado=oCrear.estado
        )
        db.add(nueva_relacion)
        db.commit()
        db.refresh(nueva_relacion)
        return EmpresaUsuarioOut.from_orm(nueva_relacion)
   
  
  
  
   
   
  
  
  
  
  