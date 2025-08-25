from typing import Any, List, Optional
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from app.models.models import EmpresaUsuario, EmpresaUsuarioRol, Menu, MenuRol, ModuloMenu
from app.utils.tree import getArbolOrdenadoTabulado
from app.schemas.respond import objRespuesta
from app.schemas.menus import MenuAcceso, MenuFiltroPlus, MenuUpdate
import logging
from sqlalchemy.exc import SQLAlchemyError


logger = logging.getLogger(__name__)

    
# def get_lista_menu(db: Session)  -> objRespuesta:
#     try:
#         MenuList = db.query(Menu).all()
#         if not MenuList:
#             raise Exception("Registro Menu no encontrada ")
#         for menu in MenuList:
#             # Verificar si el menú tiene hijos
#             has_children = db.query(Menu).filter(Menu.id_padre == menu.id).count() > 0
#             # Agregar el campo 'tiene_hijos' al menú
#             menu.hijos = has_children
                
#         # Si hay empresas, las convertimos a Pydantic
#         menu_pydantic_list = [MenuAcceso.from_orm(Menu) for Menu in MenuList]
        
#         return objRespuesta(
#             respuesta=True,
#             data=menu_pydantic_list
#         )        
        
#     except Exception as e:
#         # Captura de errores genéricos
#         return objRespuesta(
#             respuesta=False,
#             data={"error": str(e)}
#         ) 
    
def actualizar_menu(db: Session, menu: MenuUpdate)  -> objRespuesta:
    try:

        valor = editar_menu(db, menu.id, menu.nombre, menu.icono, menu.url, menu.id_padre,None,menu.tipo, None)
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
        
         
 
        
def editar_menu(db, id_menu, nombre=None, icono=None, url=None, id_padre=None, es_publico=None, tipo=None, estado=None):
    try:
        # Buscar el menú en la base de datos
        menu = db.query(Menu).filter(Menu.id == id_menu).one()

        # Actualizar los campos proporcionados
        if nombre:
            menu.nombre = nombre
        if icono:
            menu.icono = icono
        if url:
            menu.url = url
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


# def getListMenuModulos(db: Session,UsuarioId: int, EmpresaId: int):
    try:
        # Obtener todos los registros de la tabla Menu
        # menu_general_list=[]
        if(EmpresaId and UsuarioId):
            # print(f"::::::: UsuarioId: {UsuarioId} EmpresaId: {EmpresaId} :::::::")
            menu_general_list = filtrarEspecial(db, UsuarioId, EmpresaId,1)
        else:
            menu_general_list = db.query(Menu).all()

        # Verificar si la lista está vacía
        if not menu_general_list:
            raise ValueError("No se encontraron registros en Menu")

        # Construir árbol ordenado y devolverlo como parte de la respuesta
        menu_general_list = getArbolOrdenadoTabulado(menu_general_list)

        return menu_general_list
    except Exception as e:
        # Captura de errores genéricos
        return None

# def getArbolMenuModulo(db: Session, ModuloId: int, EmpresaId: int, usuarioId: int) -> list[Any]:       
#     try:
#         if EmpresaId is None or usuarioId is None:
#             raise ValueError("Faltan EmpresaId o usuarioId")

#         # print(f"🔍 Consultando menús para EmpresaId={EmpresaId}, UsuarioId={usuarioId}, ModuloId={ModuloId}")

#         menu_general_list = filtrarEspecial(db, usuarioId, EmpresaId, 2, ModuloId)

#         # if not menu_general_list:
#         #     raise ValueError("No se encontraron registros en Menu")

#         # print(f"✅ Menús visibles encontrados: {len(menu_general_list)}")
#         # for menu in menu_general_list[:10]:
#         #     print(f"   - Menu ID: {menu.id}, Nombre: {menu.nombre}")

#         menu_general_list = getArbolOrdenadoTabulado(menu_general_list)
#         # print(f"🌳 Árbol de menús generado: {len(menu_general_list)} elementos")



#         # menu_general_list = [menu for menu in menu_general_list if menu.id in menus_ids]
        
#         # print(f"✅ Menús filtrados finales: {len(menu_general_list)}")
#         # for menu in menu_general_list[:10]:
#         #     print(f"   - Menu Final ID: {menu.id}, Nombre: {menu.nombre}")

#         return menu_general_list

#     except Exception as e:
#         print(f"❌ Error en getArbolMenuModulo: {e}")
#         db.rollback()
#         return None

def getListMenus(db: Session, param: MenuFiltroPlus):
    try:
        menus_ids = []
        menus_mod_ids = []
        menu_list = []
        
        # print(f"{param}")

        # FILTRADO POR ROLES/EMPRESAS
        ####################################
        ####################################
        ####################################
        if(param.id_empresa!=None and param.id_usuario!=None):
            
            cantidad = db.query(EmpresaUsuario).filter(
                EmpresaUsuario.id_usuario == param.id_usuario, 
                EmpresaUsuario.id_empresa == param.id_empresa,
                EmpresaUsuario.estado == True
            ).count()        
                
            # print(f"Count en EmpresaUsuario {cantidad}")
            if cantidad==0:
                return [] 
                           
            EmpresaUsuarioRolList = db.query(EmpresaUsuarioRol).filter(
                and_(EmpresaUsuarioRol.id_usuario == param.id_usuario, 
                    EmpresaUsuarioRol.id_empresa == param.id_empresa,
                    EmpresaUsuarioRol.estado == True)
            ).all()
            
            roles_ids = [item.id_rol for item in EmpresaUsuarioRolList] 
            # print(f"roles {roles_ids}")
            
            MenuRolList = db.query(MenuRol).filter(
                and_(
                    MenuRol.id_rol.in_(roles_ids),
                    MenuRol.estado == True    
                )
                ).all()
            if not MenuRolList:
                return []                            
            menus_ids = [item.id_menu for item in MenuRolList]
            # print(f"menus {menus_ids}")


        # FILTRADO POR MODULOS
        ####################################
        ####################################
        ####################################

        print(f"{param.id_modulo}")
        if param.id_modulo!=None:
            ModuloMenuList = db.query(ModuloMenu).filter(
                and_(
                    ModuloMenu.id_modulo == param.id_modulo,
                    ModuloMenu.estado == True    
                )
                
            ).all()    
            menus_mod_ids = set(item.id_menu for item in ModuloMenuList)
            print(f"📦 Menús del módulo {param.id_modulo} encontrados: {menus_mod_ids}")
        
        ####################################
        ####################################
        # CONSULTA A LA TABLA DE MENU
        # POR ID DE TIPO DE MENU
        ####################################
        ####################################
        query = db.query(Menu).filter(
            or_(
                and_(
                    param.solo_activos == True,
                    Menu.id_tipo_menu == param.id_tipo_menu,
                    Menu.estado == True
                ),
                and_(
                    param.solo_activos == False,
                    Menu.id_tipo_menu == param.id_tipo_menu,
                )
            )
        )

        ####################################
        ####################################
        if menus_ids:
            query = query.filter(Menu.id.in_(menus_ids))
        if menus_mod_ids:
            query = query.filter(Menu.id.in_(menus_mod_ids))
        menu_list = query.all()

        if (param.ordenado):
            menu_ordenado = getArbolOrdenadoTabulado(menu_list)
            return menu_ordenado;

        print("***fin***" )
        return menu_list    

    except SQLAlchemyError as db_err:
        logger.error(f"Error de base de datos en getListMenuOrdenada: {str(db_err)}")
        return []

    except Exception as e:
        logger.error(f"Error inesperado en getListMenuOrdenada: {str(e)}")
        return []
        
def getListMenuOrdenada(db: Session, UsuarioId: int, EmpresaId: int):
    try:
        if EmpresaId and UsuarioId:
            # Filtrar menús especiales por usuario y empresa
            menu_general_list = filtrarEspecial(db, UsuarioId, EmpresaId, 1)
        else:
            # Obtener todos los menús si no hay filtros
            menu_general_list = db.query(Menu).all()

        # Verificar si se encontraron menús
        if not menu_general_list:
            logger.warning(f"No se encontraron registros en Menu para UsuarioId={UsuarioId}, EmpresaId={EmpresaId}")
            return []  # Mejor devolver lista vacía que None

        # Construir árbol ordenado
        menu_ordenado = getArbolOrdenadoTabulado(menu_general_list)

        return menu_ordenado

    except SQLAlchemyError as db_err:
        logger.error(f"Error de base de datos en getListMenuOrdenada: {str(db_err)}")
        return []

    except Exception as e:
        logger.error(f"Error inesperado en getListMenuOrdenada: {str(e)}")
        return []    
    
def filtrarEspecial(db: Session, id_usuario: int, id_empresa: int, id_tipo: int,  moduloId: int = None) -> List[MenuAcceso]:
    EmpresaUsuarioRolList = db.query(EmpresaUsuarioRol).filter(
        and_(EmpresaUsuarioRol.id_usuario == id_usuario, 
             EmpresaUsuarioRol.id_empresa == id_empresa,
             EmpresaUsuarioRol.estado == True)
    ).all()
    
    if not EmpresaUsuarioRolList:
        return None

    roles_ids = [item.id_rol for item in EmpresaUsuarioRolList] 
    # print(f" roles_ids {roles_ids} ")

    MenuRolList = db.query(MenuRol).filter(MenuRol.id_rol.in_(roles_ids)).all()
    if not MenuRolList:
        raise Exception("Registro MenuRol no encontrado ")
    
    menus_ids = [item.id_menu for item in MenuRolList]
    # print(f" menus_ids {menus_ids} ")
    



    if(id_tipo==1):
        MenuList = db.query(Menu).filter(
            and_(Menu.id.in_(menus_ids),
                Menu.estado == True,
                Menu.id_tipo_menu==id_tipo)).all() 

    if(id_tipo==2):
        ModuloMenuList = db.query(ModuloMenu).filter(
            ModuloMenu.id_modulo == moduloId
        ).all()    
        menus_ids = set(item.id_menu for item in ModuloMenuList)
        print(f"📦 Menús del módulo {moduloId} encontrados: {menus_ids}")
        
        MenuList = db.query(Menu).filter(
            and_(Menu.id.in_(menus_ids),
                Menu.estado == True,
                Menu.id_tipo_menu==id_tipo)).all() 




    
    return MenuList   
