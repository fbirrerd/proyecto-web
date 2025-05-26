

from typing import Any, Dict, List
from sqlalchemy import and_, func
from app.schemas.empresaUsuario import AsignacionEmpresas, EmpresaUsuarioCreate, EmpresaUsuarioList, EmpresaUsuarioOut
from app.models.models import Empresa, EmpresaUsuario, Usuario
from sqlalchemy.orm import Session


from datetime import datetime, timezone


def getDatosEmpresaUsuario(db: Session):
    datos = (
        db.query(
            Usuario.nombres.label("usuario_nombre"),
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
   
def getDatosEmpresaUsuario_idUsuario(idUsuario:int, db: Session):
    datos = db.query(EmpresaUsuario).filter(
        and_(EmpresaUsuario.id_usuario == idUsuario,
             EmpresaUsuario.estado==True)).all()
    return datos
  
def getDatosEmpresaUsuario_idEmpresa(idEmpresa:int, db: Session):
    datos = db.query(EmpresaUsuario).filter(
        and_(EmpresaUsuario.id_empresa == idEmpresa, 
             EmpresaUsuario.estado==True)).all()
    return datos
  

def generar_relaciones(data: AsignacionEmpresas, db: Session) -> List[Dict[str, Any]]:
    id_usuario = data.id
    relaciones_procesadas = [] # Changed from relaciones_guardadas for clarity

    for empresa in data.empresas:
        id_empresa = int(empresa.id)
        estado = empresa.checked
        existente = db.query(EmpresaUsuario).filter(
            and_(EmpresaUsuario.id_usuario == id_usuario,
                 EmpresaUsuario.id_empresa == id_empresa)
        ).first()

        if estado is False: # If the incoming state is False, we intend to delete
            if existente:
                db.delete(existente)
                db.commit() # Commit immediately after deletion
                # No need to append deleted items to relaciones_procesadas unless specifically required
        else: # If the incoming state is True
            if existente:
                if existente.estado != estado: # Only update if the state has changed
                    existente.estado = estado
                    # existente.fecha_modificacion = datetime.now() # Uncomment if you have this column and want to manage it manually
                    db.commit()
                    db.refresh(existente)
                relaciones_procesadas.append({
                    "id_usuario": id_usuario,
                    "id_empresa": id_empresa,
                    "estado": estado
                })
            else: # If it doesn't exist and the state is True, create a new one
                nueva_relacion = EmpresaUsuario(
                    estado=estado,
                    id_empresa=id_empresa,
                    id_usuario=id_usuario
                )
                db.add(nueva_relacion)
                db.commit()
                db.refresh(nueva_relacion)

                relaciones_procesadas.append({
                    "id_usuario": nueva_relacion.id_usuario,
                    "id_empresa": nueva_relacion.id_empresa,
                    "estado": nueva_relacion.estado
                })

    return relaciones_procesadas