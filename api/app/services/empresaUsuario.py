

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
  
def generar_relaciones(data: AsignacionEmpresas, db: Session):
    id_usuario = data.id
    relaciones_guardadas = []

    for empresa in data.empresas:
        id_empresa = int(empresa.id)
        estado = empresa.checked
        existente = db.query(EmpresaUsuario).filter(
            and_(EmpresaUsuario.id_usuario == id_usuario, 
                 EmpresaUsuario.id_empresa == id_empresa)
        ).first()

        if existente:
            if existente.estado != estado:
                existente.estado = estado
                # existente.fecha_modificacion = 
                db.commit()
                db.refresh(existente)
            relaciones_guardadas.append({
                "id_usuario": id_usuario,
                "id_empresa": id_empresa,
                "estado": estado
            })
        else:
            nueva_relacion = EmpresaUsuario(
                estado=estado,
                id_empresa=id_empresa,
                id_usuario=id_usuario
            )
            db.add(nueva_relacion)
            db.commit()
            db.refresh(nueva_relacion)

            relaciones_guardadas.append({
                "id_usuario": nueva_relacion.id_usuario,
                "id_empresa": nueva_relacion.id_empresa,
                "estado": nueva_relacion.estado
            })
    
        return relaciones_guardadas
  