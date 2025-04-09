from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.schemas.menugeneral import MenuGeneralAcceso
from app.models.models import MenuGeneral, MenuGeneralRol, Rol, UsuarioEmpresaRol


def getDatosMenuGenerales(db: Session, UsuarioId: int, EmpresaId: int):
    userEmpRolList = db.query(UsuarioEmpresaRol).filter(
        and_(UsuarioEmpresaRol.id_usuario == UsuarioId, 
             UsuarioEmpresaRol.id_empresa == EmpresaId,
             UsuarioEmpresaRol.estado == True)
    ).all()
    if not userEmpRolList:
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")

    roles_ids = [item.id_rol for item in userEmpRolList]
    
    MenuGeneralRolList = db.query(MenuGeneralRol).filter(
        and_(MenuGeneralRol.id_rol.in_(roles_ids),
             MenuGeneralRol.estado == True)
    ).all()

    menus_ids = [item.id_menu for item in MenuGeneralRolList]
    
    MenuGeneralList = db.query(MenuGeneral).filter(
        and_(MenuGeneral.id.in_(menus_ids),
             MenuGeneral.estado == True)).all()


    if not MenuGeneralList:
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")
    
    # Si hay empresas, las convertimos a Pydantic
    menu_pydantic_list = [MenuGeneralAcceso.from_orm(menugeneral) for menugeneral in MenuGeneralList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if menu_pydantic_list:
        return menu_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
