import traceback
from fastapi import HTTPException
from app.schemas.rolMenu import ObjetoRelaciones, RelacionMenuRol, RolMenu, RolMenu_relacion
from app.schemas.rol import RolAcceso
from app.models.models import Menu, MenuRol, Rol, EmpresaUsuarioRol
from sqlalchemy.orm import Session

from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta


def getDatosRol(db: Session, UsuarioId: int, EmpresaId: int):
    userEmpRolList = db.query(EmpresaUsuarioRol).filter(
        and_(EmpresaUsuarioRol.id_usuario == UsuarioId, 
             EmpresaUsuarioRol.id_empresa == EmpresaId,
             EmpresaUsuarioRol.estado == True)
    ).all()
    if not userEmpRolList:
        print (f"Registro UsuarioRolEmpresa 3 no encontrada EmpresaUsuarioRol.id_usuario == {UsuarioId}, EmpresaUsuarioRol.id_empresa == {EmpresaId}, EmpresaUsuarioRol.estado == True ")
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")
    
    roles_ids = [item.id_rol for item in userEmpRolList]
    
    rolList = db.query(Rol).filter(Rol.id.in_(roles_ids)).all()
    
    if not rolList:
        raise Exception("Roles no encontrados")
    
    # Si hay empresas, las convertimos a Pydantic
    rol_pydantic_list = [RolAcceso.from_orm(empresa) for empresa in rolList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if rol_pydantic_list:
        return rol_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None

def get_RolMenu(db: Session)  -> objRespuesta:
    data = db.query(MenuRol).all()
    return objRespuesta(
        respuesta = True,
        data = data
    )
    

def set_relaciones(db: Session, obj: ObjetoRelaciones) -> objRespuesta:
    relaciones_guardadas = []

    try:
        for relacion in obj.relaciones:
            existente = db.query(MenuRol).filter(
                and_(
                    MenuRol.id_rol == relacion.id_rol,
                    MenuRol.id_menu == relacion.id_menu
                )
            ).first()

            if existente:
                if existente.estado != relacion.estado:
                    existente.estado = relacion.estado
                    # existente.fecha_modificacion = 
                    db.commit()
                    db.refresh(existente)
                relaciones_guardadas.append({
                    "id_menu": existente.id_menu,
                    "id_rol": existente.id_rol,
                    "estado": existente.estado
                })
            else:
                nueva_relacion = MenuRol(
                    estado=relacion.estado,
                    id_menu=relacion.id_menu,
                    id_rol=relacion.id_rol
                )
                db.add(nueva_relacion)
                db.commit()
                db.refresh(nueva_relacion)
                relaciones_guardadas.append({
                    "id_menu": nueva_relacion.id_menu,
                    "id_rol": nueva_relacion.id_rol,
                    "estado": nueva_relacion.estado
                })

        return objRespuesta(
            respuesta= True,
            data = { 
                    "mensaje": relaciones_guardadas
                    }
            )
    except Exception as e:
        db.rollback()
        return objRespuesta(
            respuesta= True,
            data = { 
                    "status_code": 500, 
                    "detail": "Error al guardar relaciones. Detalles: " + str(e)
                    }
            )        

       
  

def obtener_menu_rol_info(db: Session):
    resultados = (
        db.query(
            MenuRol.id_rol,
            Rol.nombre.label("rol_nombre"),
            MenuRol.id_menu,
            Menu.nombre.label("menu_nombre"),
            MenuRol.estado
        )
        .join(Rol, Rol.id == MenuRol.id_rol)
        .join(Menu, Menu.id == MenuRol.id_menu)
        .all()
    )

    return [
        {
            "id_rol": r.id_rol,
            "rol_nombre": r.rol_nombre,
            "id_menu": r.id_menu,
            "menu_nombre": r.menu_nombre,
            "estado": r.estado
        }
        for r in resultados
    ]
    
