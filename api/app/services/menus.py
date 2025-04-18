from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import EmpresaUsuarioRol, Menu, MenuRol
from app.utils.tree import getArbolOrdenadoTabulado
from app.schemas.respond import objRespuesta
from app.schemas.menus import MenuAcceso, MenuUpdate


def filtrarEspecial(db: Session, UsuarioId: int, EmpresaId: int) -> List[any]:
    EmpresaUsuarioRolList = db.query(EmpresaUsuarioRol).filter(
        and_(EmpresaUsuarioRol.id_usuario == UsuarioId, 
             EmpresaUsuarioRol.id_empresa == EmpresaId,
             EmpresaUsuarioRol.estado == True)
    ).all()
    
    if not EmpresaUsuarioRolList:
        raise Exception("Registro UsuarioRolEmpresa no encontrada ")

    roles_ids = [item.id_rol for item in EmpresaUsuarioRolList] 
    print(f" roles_ids {roles_ids} ")

    MenuRolList = db.query(MenuRol).filter(MenuRol.id_rol.in_(roles_ids)).all()
    if not MenuRolList:
        raise Exception("Registro MenuRol no encontrado ")
    
    menus_ids = [item.id_menu for item in MenuRolList]
    print(f" menus_ids {menus_ids} ")
    
    MenuList = db.query(Menu).filter(
        and_(Menu.id.in_(menus_ids),
             Menu.estado == True)).all() 
   
    print(f" MenuList {MenuList.count} ")    
    
    return MenuList   

# def getDatosMenues(db: Session, UsuarioId: int, EmpresaId: int):
#     userEmpRolList = db.query(EmpresaUsuarioRol).filter(
#         and_(EmpresaUsuarioRol.id_usuario == UsuarioId, 
#              EmpresaUsuarioRol.id_empresa == EmpresaId,
#              EmpresaUsuarioRol.estado == True)
#     ).all()
#     if not userEmpRolList:
#         raise Exception("Registro UsuarioRolEmpresa no encontrada ")

#     roles_ids = [item.id_rol for item in userEmpRolList]
#     MenuRolList = db.query(MenuRol).filter(
#         and_(MenuRol.id_rol.in_(roles_ids),
#              MenuRol.estado == True)
#     ).all()

#     menus_ids = [item.id_menu for item in MenuRolList]
#     MenuList = db.query(Menu).filter(
#         and_(Menu.id.in_(menus_ids),
#              Menu.estado == True)).all()
    
    
    
    
#     if not MenuList:
#         raise Exception("Registro Menu no encontrada ")
#     for menu in MenuList:
#         # Verificar si el menú tiene hijos
#         has_children = db.query(Menu).filter(Menu.id_padre == menu.id).count() > 0
#         # Agregar el campo 'tiene_hijos' al menú
#         menu.hijos = has_children
            
#     # Si hay empresas, las convertimos a Pydantic
#     menu_pydantic_list = [MenuAcceso.from_orm(Menu) for Menu in MenuList]
#     if menu_pydantic_list:
#         return menu_pydantic_list  # O devolver la lista completa si es necesario
#     else:
#         return None
  
def getListMenuOrdenada(db: Session,UsuarioId: int, EmpresaId: int):
    try:
        # Obtener todos los registros de la tabla Menu
        # menu_general_list=[]
        if(EmpresaId and UsuarioId):
            print(f"::::::: UsuarioId: {UsuarioId} EmpresaId: {EmpresaId} :::::::")
            menu_general_list = filtrarEspecial(db, UsuarioId, EmpresaId)
        else:
            menu_general_list = db.query(Menu).all()

        # Verificar si la lista está vacía
        if not menu_general_list:
            raise ValueError("No se encontraron registros en Menu")

        # Construir árbol ordenado y devolverlo como parte de la respuesta
        # menu_general_list = getArbolOrdenadoTabulado(menu_general_list)

        return menu_general_list
    except Exception as e:
        # Captura de errores genéricos
        return None
        
        
    
def get_lista_menu(db: Session)  -> objRespuesta:
    try:
        MenuList = db.query(Menu).all()
        if not MenuList:
            raise Exception("Registro Menu no encontrada ")
        for menu in MenuList:
            # Verificar si el menú tiene hijos
            has_children = db.query(Menu).filter(Menu.id_padre == menu.id).count() > 0
            # Agregar el campo 'tiene_hijos' al menú
            menu.hijos = has_children
                
        # Si hay empresas, las convertimos a Pydantic
        menu_pydantic_list = [MenuAcceso.from_orm(Menu) for Menu in MenuList]
        
        return objRespuesta(
            respuesta=True,
            data=menu_pydantic_list
        )        
        
    except Exception as e:
        # Captura de errores genéricos
        return objRespuesta(
            respuesta=False,
            data={"error": str(e)}
        ) 
    
def actualizar_menu_general(db: Session, menu: MenuUpdate)  -> objRespuesta:
    try:

        valor = editar_menu(db, menu.id, menu.nombre, menu.icono, menu.ruta, menu.id_padre,None,menu.tipo, None)
        if valor:
            return objRespuesta(
                respuesta=True,
                data=getListMenuOrdenada(db, None, None)
            )
                        
    except Exception as e:
        # Captura de errores genéricos
        return objRespuesta(
            respuesta=False,
            data={"error": str(e)}
        )         
        
 
def actualizar_estado(db: Session, id_menu: int, estado: bool):
    try:
        menu = db.query(Menu).filter(Menu.id == id_menu).first()

        if menu is None:
            print(f"No se encontró el menú con ID: {id_menu}")
            return False

        if estado is not None:
            menu.estado = estado

        db.commit()
        return True
    except Exception as e:
        db.rollback()  # Revertir la transacción en caso de error
        print(f"Error al editar el menú: {e}")
        return False
    finally:
        db.close()  # Asegurar el cierre de la sesión
        
         
 
        
def editar_menu(db, id_menu, nombre=None, icono=None, ruta=None, id_padre=None, es_publico=None, tipo=None, estado=None):
    try:
        # Buscar el menú en la base de datos
        menu = db.query(Menu).filter(Menu.id == id_menu).one()

        # Actualizar los campos proporcionados
        if nombre:
            menu.nombre = nombre
        if icono:
            menu.icono = icono
        if ruta:
            menu.ruta = ruta
        if id_padre is not None:  # Para manejar la asignación de null correctamente
            menu.id_padre = id_padre
        if es_publico is not None:
            menu.es_publico = es_publico
        if tipo:
            menu.tipo = tipo
        if estado is not None:
            menu.estado = estado

        # La fecha de modificación se actualiza automáticamente con onupdate
        # Si no es automático, se puede actualizar manualmente:
        # menu.fecha_modificacion = func.now()

        # Guardar los cambios en la base de datos
        db.commit()

        return True  # Retorna el menú actualizado
    except Exception as e:
        print(f"Error al editar el menú: {e}")
        return False

# def getListMenuesArbol(db: Session)  -> objRespuesta:
#     try:
#         # Obtener todos los registros de la tabla Menu
#         menu_general_list = db.query(Menu).all()

#         # Verificar si la lista está vacía
#         if not menu_general_list:
#             raise ValueError("No se encontraron registros en Menu")

#         # Construir árbol ordenado y devolverlo como parte de la respuesta
#         data_ordenada = construir_arbol_ordenado(menu_general_list)

#         return objRespuesta(
#             respuesta=True,
#             data=data_ordenada
#         )
#     except Exception as e:
#         # Captura de errores genéricos
#         return objRespuesta(
#             respuesta=False,
#             data={"error": str(e)}
#         )
    