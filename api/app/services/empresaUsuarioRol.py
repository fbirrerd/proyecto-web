
from app.models.models import EmpresaUsuario, Rol, EmpresaUsuarioRol
from sqlalchemy.orm import Session


from datetime import datetime, timezone
from sqlalchemy import and_, false, func, or_, true



def obtener_roles_por_empresa_usuario(db: Session, id_empresa: int, id_usuario: int):
    query = (
        db.query(
            EmpresaUsuario.id_empresa.label("id_empresa"),
            EmpresaUsuario.id_usuario.label("id_usuario"),
            Rol.id.label("id_rol"),
            Rol.nombre.label("nombre_rol"),
            func.coalesce(EmpresaUsuarioRol.estado, false()).label("estado")
        )
        .join(Rol, Rol.estado == True)
        .join(EmpresaUsuario, and_(
            EmpresaUsuario.id_empresa == id_empresa,
            EmpresaUsuario.id_usuario == id_usuario,
            EmpresaUsuario.estado == True
        ))
        .outerjoin(
            EmpresaUsuarioRol,
            and_(
                EmpresaUsuarioRol.id_empresa == EmpresaUsuario.id_empresa,
                EmpresaUsuarioRol.id_usuario == EmpresaUsuario.id_usuario,
                EmpresaUsuarioRol.id_rol == Rol.id
            )
        )
        .order_by(Rol.nombre)
    )

    return query.all()


