from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.utils.tree import getArbolOrdenadoTabulado
from app.schemas.respond import objRespuesta
from app.schemas.menuGeneral import MenuGeneralAcceso, MenuUpdate
from app.models.models import MenuGeneral, MenuGeneralRol, UsuarioEmpresaRol

def filtrarEspecial(db: Session, UsuarioId: int, EmpresaId: int) -> List:
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

# def getDatosMenuGenerales(db: Session, UsuarioId: int, EmpresaId: int):
#     userEmpRolList = db.query(UsuarioEmpresaRol).filter(
#         and_(UsuarioEmpresaRol.id_usuario == UsuarioId, 
#              UsuarioEmpresaRol.id_empresa == EmpresaId,
#              UsuarioEmpresaRol.estado == True)
#     ).all()
#     if not userEmpRolList:
#         raise Exception("Registro UsuarioRolEmpresa no encontrada ")

#     roles_ids = [item.id_rol for item in userEmpRolList]
#     MenuGeneralRolList = db.query(MenuGeneralRol).filter(
#         and_(MenuGeneralRol.id_rol.in_(roles_ids),
#              MenuGeneralRol.estado == True)
#     ).all()

#     menus_ids = [item.id_menu for item in MenuGeneralRolList]
#     MenuGeneralList = db.query(MenuGeneral).filter(
#         and_(MenuGeneral.id.in_(menus_ids),
#              MenuGeneral.estado == True)).all()
    
    
    
    
#     if not MenuGeneralList:
#         raise Exception("Registro MenuGeneral no encontrada ")
#     for menu in MenuGeneralList:
#         # Verificar si el menú tiene hijos
#         has_children = db.query(MenuGeneral).filter(MenuGeneral.id_padre == menu.id).count() > 0
#         # Agregar el campo 'tiene_hijos' al menú
#         menu.hijos = has_children
            
#     # Si hay empresas, las convertimos a Pydantic
#     menu_pydantic_list = [MenuGeneralAcceso.from_orm(menugeneral) for menugeneral in MenuGeneralList]
#     if menu_pydantic_list:
#         return menu_pydantic_list  # O devolver la lista completa si es necesario
#     else:
#         return None
  
def getListMenuOrdenada(db: Session,UsuarioId: int, EmpresaId: int)  -> objRespuesta:
    try:
        # Obtener todos los registros de la tabla MenuGeneral
        
        # if(EmpresaId and UsuarioId):
        #     menu_general_list = filtrarEspecial(db, UsuarioId, EmpresaId)
        # else:
        menu_general_list = db.query(MenuGeneral).all()

        # Verificar si la lista está vacía
        if not menu_general_list:
            raise ValueError("No se encontraron registros en MenuGeneral")

        # Construir árbol ordenado y devolverlo como parte de la respuesta
        menu_general_list = getArbolOrdenadoTabulado(menu_general_list)

        return menu_general_list
        # return objRespuesta(
        #     respuesta=True,
        #     data=menu_general_list
        # )
    except Exception as e:
        # Captura de errores genéricos
        return objRespuesta(
            respuesta=False,
            data={"error": str(e)}
        )
    
def get_lista_menu(db: Session)  -> objRespuesta:
    try:
        MenuGeneralList = db.query(MenuGeneral).all()
        if not MenuGeneralList:
            raise Exception("Registro MenuGeneral no encontrada ")
        for menu in MenuGeneralList:
            # Verificar si el menú tiene hijos
            has_children = db.query(MenuGeneral).filter(MenuGeneral.id_padre == menu.id).count() > 0
            # Agregar el campo 'tiene_hijos' al menú
            menu.hijos = has_children
                
        # Si hay empresas, las convertimos a Pydantic
        menu_pydantic_list = [MenuGeneralAcceso.from_orm(menugeneral) for menugeneral in MenuGeneralList]
        
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

        valor = editar_menu(db, menu.id, menu.nombre, menu.icono, menu.ruta, None,None,menu.tipo, menu.orden, menu.estado)
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
        
        
def editar_menu(db, id_menu, nombre=None, icono=None, ruta=None, id_padre=None, es_publico=None, tipo=None, orden=None, estado=None):
    try:
        # Buscar el menú en la base de datos
        menu = db.query(MenuGeneral).filter(MenuGeneral.id == id_menu).one()

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
        if orden is not None:
            menu.orden = orden
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

# def getListMenuGeneralesArbol(db: Session)  -> objRespuesta:
#     try:
#         # Obtener todos los registros de la tabla MenuGeneral
#         menu_general_list = db.query(MenuGeneral).all()

#         # Verificar si la lista está vacía
#         if not menu_general_list:
#             raise ValueError("No se encontraron registros en MenuGeneral")

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
    