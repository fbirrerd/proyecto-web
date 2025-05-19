from typing import List
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import Empresa, EmpresaUsuario, EmpresaUsuarioRol, Usuario
from app.schemas.empresa import EmpresaAcceso, EmpresaCreate, EmpresaList, EmpresaOut, EmpresaUpdate, UsuarioListado


def getDatosEmpresa(db: Session, UsuarioId: int):
    userEmpObj = db.query(EmpresaUsuario).filter(
        and_(EmpresaUsuario.id_usuario == UsuarioId, 
             EmpresaUsuario.estado == True)).all()
    if not userEmpObj:
        raise Exception("Registro EmpresaUsuario no encontrado")
    
    id_empresas = [item.id_empresa for item in userEmpObj]
    
    empresaList = db.query(Empresa).filter(Empresa.id.in_(id_empresas)).all()
    
    if not empresaList:
        raise Exception("Empresas no encontrada")
    
    # Si hay empresas, las convertimos a Pydantic
    empresa_pydantic_list = [EmpresaAcceso.from_orm(empresa) for empresa in empresaList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if empresa_pydantic_list:
        return empresa_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
def get_all(db: Session) ->  List[EmpresaOut]:
    return db.query(Empresa).order_by(Empresa.nombre).all()

def get_by_id(db: Session, empresa_id: int) ->  EmpresaOut:
    return db.query(Empresa).filter(Empresa.id == empresa_id).first()

def create(db: Session, empresa: EmpresaCreate) ->  EmpresaOut:
    nueva = Empresa(**empresa.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

def update(db: Session, empresa_id: int, data: EmpresaUpdate) ->  EmpresaOut:
    obj = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def update_estado(db: Session, empresa_id: int, estado:bool) ->  EmpresaOut:
    obj = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not obj:
        return None

    obj.estado = estado
        
    db.commit()
    db.refresh(obj)
    return obj


def delete(db: Session, empresa_id: int) ->  EmpresaOut:
    obj = db.query(Empresa).filter(Empresa.id == empresa_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj

def get_lista(db: Session) ->  EmpresaList:
    datos = db.query(Empresa).filter(Empresa.estado == True).order_by(Empresa.nombre).all()
    return [EmpresaList.from_orm(emp) for emp in datos]


def get_lista_usuarios(db: Session, empresa_id: int) -> List[UsuarioListado]:
    try:
        # Paso 1: Obtener ids como lista de enteros
        subquery = db.query(EmpresaUsuario.id_usuario)\
                     .filter(EmpresaUsuario.id_empresa == empresa_id)\
                     .all()
        id_usuarios = [r[0] for r in subquery]  # Desempaquetar correctamente

        # Paso 2: Obtener usuarios activos
        usuarios = db.query(Usuario)\
                     .filter(Usuario.estado == True, Usuario.id.in_(id_usuarios))\
                     .all()

        # Paso 3: Construir lista de UsuarioListado
        return [
            UsuarioListado(
                username=u.username,
                nombre=f"{u.nombres} {u.apellidos}"
            ) for u in usuarios
        ]
    except Exception as e:
        print(f"Error en get_lista_usuarios: {e}")
        raise
