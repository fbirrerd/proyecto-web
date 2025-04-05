from sqlalchemy.orm import Session
from app.models.usuario_empresa import UsuarioEmpresa
from app.schemas.usuario_empresa import UsuarioEmpresaCreate

def crear_usuario_empresa(db: Session, relacion: UsuarioEmpresaCreate):
    db_rel = UsuarioEmpresa(**relacion.dict())
    db.add(db_rel)
    db.commit()
    db.refresh(db_rel)
    return db_rel
