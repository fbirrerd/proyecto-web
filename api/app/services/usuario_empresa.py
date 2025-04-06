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

def obtener_empresas_por_usuario(db: Session, usuario_id: int):
    if usuario_id==1:
        result2 = db.query(Empresa.id, Empresa.nombre).all()
        return result2            
    else:
    # Realizamos la consulta con las condiciones que mencionaste
        result1 = db.query(UsuarioEmpresa.usuario_id).filter(
            and_(
                UsuarioEmpresa.usuario_id == usuario_id,
                Empresa.estado == 0
            )
        ).all()

        # Extraer los ids de empresas de result1
        empresa_ids = [r.empresa_id for r in result1]

        # Filtrar result2 usando los ids de empresa extraídos de result1
        result2 = db.query(Empresa.id, Empresa.nombre).filter(
            and_(
                Empresa.id.in_(empresa_ids),  # Filtrar por los ids de empresas
                Empresa.estado==0
            )
        ).all()
        return result2        
    
    
