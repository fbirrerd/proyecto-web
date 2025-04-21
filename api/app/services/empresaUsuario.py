

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
        .filter(EmpresaUsuario.estado == True)
        .all()
    )
    return [EmpresaUsuarioList.from_orm(r) for r in datos]
  
def setEmpresaUsuario(db: Session, oCrear: EmpresaUsuarioCreate) -> EmpresaUsuarioOut:
    # Verificar si ya existe la relación
    existe = db.query(EmpresaUsuario).filter_by(
        id_empresa = oCrear.id_empresa,
        id_usuario = oCrear.id_usuario
    ).first()

    nueva_relacion = EmpresaUsuario(
        id_empresa = oCrear.id_empresa,
        id_usuario = oCrear.id_usuario,
        estado = oCrear.estado
    )

    db.add(nueva_relacion)
    db.commit()
    return [EmpresaUsuarioOut.from_orm(r) for r in nueva_relacion]
  
   
  
  
  
   
   
  
  
  
  
  