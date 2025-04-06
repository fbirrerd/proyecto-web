from sqlalchemy.orm import Session
from app.models.empresa import Empresa
from app.models.usuario_empresa import UsuarioEmpresa
from app.schemas.usuario_empresa import UsuarioEmpresaCreate
from sqlalchemy import and_

def crear_usuario_empresa(db: Session, relacion: UsuarioEmpresaCreate):
    db_rel = UsuarioEmpresa(**relacion.dict())
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel


# def obtener_empresas_por_usuario(db: Session, usuario_id: int):
#     # Realizamos la consulta con las condiciones que mencionaste
#     result = db.query(UsuarioEmpresa, Empresa).join(Empresa, UsuarioEmpresa.empresa_id == Empresa.id).filter(
#         and_(
#             UsuarioEmpresa.usuario_id == usuario_id,
#             Empresa.estado == 0,
#         )
#     ).all()

#     return result