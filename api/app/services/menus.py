from typing import Any, List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.models.models import EmpresaUsuarioRol, Menu, MenuRol, ModuloMenu
from app.utils.tree import getArbolOrdenadoTabulado
from app.schemas.respond import objRespuesta
from app.schemas.menus import MenuAcceso, MenuUpdate


def filtrarEspecial(db: Session, UsuarioId: int, EmpresaId: int, tipo: int,  moduloId: int = 0) -> List[MenuAcceso]:
    EmpresaUsuarioRolList = db.query(EmpresaUsuarioRol).filter(
        and_(EmpresaUsuarioRol.id_usuario == UsuarioId, 
             EmpresaUsuarioRol.id_empresa == EmpresaId,
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
    
    if(tipo==1):
        MenuList = db.query(Menu).filter(
            and_(Menu.id.in_(menus_ids),
                Menu.estado == True,
                Menu.id_tipo_menu==tipo)).all() 
    else:
        ModuloMenuList = db.query(ModuloMenu).filter(
            ModuloMenu.id_modulo == moduloId
        ).all()

        menus_ids = set(item.id_menu for item in ModuloMenuList)

        MenuList = db.query(Menu).filter(
            and_(Menu.id.in_(menus_ids),
                Menu.estado == True,
                Menu.id_tipo_menu==tipo)).all()         
        print(f"📦 Menús del módulo {moduloId} encontrados: {menus_ids}")

    
    return MenuList   

  
def getListMenuOrdenada(db: Session,UsuarioId: int, EmpresaId: int):
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
        print(f"Error getListaMenuOrdenada {str(e)}")
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


def getListMenuModulos(db: Session,UsuarioId: int, EmpresaId: int):
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

def getArbolMenuModulo(db: Session, ModuloId: int, EmpresaId: int, usuarioId: int) -> list[Any]:       
    try:
        if EmpresaId is None or usuarioId is None:
            raise ValueError("Faltan EmpresaId o usuarioId")

        # print(f"🔍 Consultando menús para EmpresaId={EmpresaId}, UsuarioId={usuarioId}, ModuloId={ModuloId}")

        menu_general_list = filtrarEspecial(db, usuarioId, EmpresaId, 2, ModuloId)

        # if not menu_general_list:
        #     raise ValueError("No se encontraron registros en Menu")

        # print(f"✅ Menús visibles encontrados: {len(menu_general_list)}")
        # for menu in menu_general_list[:10]:
        #     print(f"   - Menu ID: {menu.id}, Nombre: {menu.nombre}")

        menu_general_list = getArbolOrdenadoTabulado(menu_general_list)
        # print(f"🌳 Árbol de menús generado: {len(menu_general_list)} elementos")



        # menu_general_list = [menu for menu in menu_general_list if menu.id in menus_ids]
        
        # print(f"✅ Menús filtrados finales: {len(menu_general_list)}")
        # for menu in menu_general_list[:10]:
        #     print(f"   - Menu Final ID: {menu.id}, Nombre: {menu.nombre}")

        return menu_general_list

    except Exception as e:
        print(f"❌ Error en getArbolMenuModulo: {e}")
        db.rollback()
        return None
