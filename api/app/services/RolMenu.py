import traceback
from fastapi import HTTPException
from app.schemas.rolMenu import ObjetoRelaciones, RelacionMenuRol, RolMenu, RolMenu_relacion
from app.schemas.rol import RolAcceso
from app.models.models import MenuGeneral, MenuGeneralRol, Rol, UsuarioEmpresaRol
from sqlalchemy.orm import Session

from sqlalchemy import and_, or_
from app.schemas.respond import objRespuesta


def getDatosRol(db: Session, UsuarioId: int, EmpresaId: int):
    userEmpRolList = db.query(UsuarioEmpresaRol).filter(
        and_(UsuarioEmpresaRol.id_usuario == UsuarioId, 
             UsuarioEmpresaRol.id_empresa == EmpresaId,
             UsuarioEmpresaRol.estado == True)
    ).all()
    if not userEmpRolList:
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
    datos = db.query(MenuGeneralRol).all()
    return objRespuesta(
        respuesta=True,
        data=datos
    )
    

def set_relaciones(db: Session, obj: ObjetoRelaciones) -> objRespuesta:
    relaciones_guardadas = []

    try:
        for relacion in obj.relaciones:
            existente = db.query(MenuGeneralRol).filter(
                and_(
                    MenuGeneralRol.id_rol == relacion.id_rol,
                    MenuGeneralRol.id_menu == relacion.id_menu
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
                nueva_relacion = MenuGeneralRol(
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

            print(f"Guardar: Rol {relacion.id_rol} - Menú {relacion.id_menu} - Estado {relacion.estado}")

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
            MenuGeneralRol.id_rol,
            Rol.nombre.label("rol_nombre"),
            MenuGeneralRol.id_menu,
            MenuGeneral.nombre.label("menu_nombre"),
            MenuGeneralRol.estado
        )
        .join(Rol, Rol.id == MenuGeneralRol.id_rol)
        .join(MenuGeneral, MenuGeneral.id == MenuGeneralRol.id_menu)
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
    
