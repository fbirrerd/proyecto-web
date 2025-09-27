from typing import Any, List, Optional
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session
from app.models.models import EmpresaModulo, EmpresaUsuarioRol, Menu, MenuRol, Modulo, ModuloMenu
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
                # data=getListMenuOrdenada(db, None, None)
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

def obtener_menu(db: Session, filtro: MenuFiltroPlus):
    try:
        # 1. obtener ids de menús disponibles
        if filtro.id_usuario is None and filtro.id_empresa is None:
            ids = [
                id_menu
                for (id_menu,) in db.query(Menu.id)
                    .filter(
                        Menu.id_tipo_menu == filtro.id_tipo_menu,
                        (Menu.id_padre == filtro.id_padre) if filtro.id_padre is not None else Menu.id_padre.is_(None)
                    )
                    .all()
            ]
        else:
            ids = [
                id_menu
                for (id_menu,) in get_menus_por_usuario_empresa(
                    db, filtro.id_usuario, filtro.id_empresa
                )
            ]

        if not ids:  # si no hay nada, retornar vacío
            return []

        # 2. traer menús según el padre actual
        menus = (
            db.query(Menu)
            .filter(
                Menu.id.in_(ids),
                (Menu.id_padre == filtro.id_padre) if filtro.id_padre is not None else Menu.id_padre.is_(None),
                Menu.id_tipo_menu == filtro.id_tipo_menu
            )
            .order_by(Menu.orden.asc())
            .all()
        )

        resultado = []
        for menu in menus:
            # construir filtro hijo
            if filtro.id_usuario is None and filtro.id_empresa is None:
                filtro_hijo = MenuFiltroPlus(
                    id_padre=menu.id,
                    id_tipo_menu=filtro.id_tipo_menu,
                    modo=filtro.modo
                )
            else:
                filtro_hijo = MenuFiltroPlus(
                    id_usuario=filtro.id_usuario,
                    id_empresa=filtro.id_empresa,
                    id_padre=menu.id,
                    id_tipo_menu=filtro.id_tipo_menu,
                    modo=filtro.modo
                )

            # llamada recursiva
            children = obtener_menu(db, filtro_hijo)
            nodo = {
                "id": menu.id,
                "icono": menu.icono,
                "nombre": getattr(menu, "nombre", None),
                "id_padre": getattr(menu, "id_padre", None),
                "url": menu.url,
                "orden": getattr(menu, "orden", None),
            }

            if filtro.modo == 1:
                # modo árbol → children dentro del nodo
                nodo["children"] = children
                resultado.append(nodo)
            elif filtro.modo == 2:
                # modo aplanado → hijos al mismo nivel
                resultado.append(nodo)
                if children:
                    resultado.extend(children)

        return resultado
    except Exception as e:
        print(f"Error en obtener_menu: {e}")
        return []
    

def obtener_menu_modulo(db: Session, filtro: MenuFiltroPlus):
    try:
        # 1. obtener ids de módulos activos
        print(f"Filtros {filtro}")
        modulos = obtener_modulos_activos(db, filtro)
        id_modulos = [modulo['id'] for modulo in modulos]

        print(f"Modulos {id_modulos}")

        if not modulos:
            return []

        # 2. obtener ids de menús relacionados a esos módulos
        if filtro.id_usuario is None and filtro.id_empresa is None:
            menus1 = (
                db.query(ModuloMenu.id_menu)
                .join(MenuRol, MenuRol.id_menu == ModuloMenu.id_menu)
                .filter(
                    MenuRol.estado == True,
                    MenuRol.id_rol == EmpresaUsuarioRol.id_rol,
                    ModuloMenu.estado == True,
                    ModuloMenu.id_modulo.in_(id_modulos)
                )
                .all()
            )
        else:
            menus1 = (
                db.query(ModuloMenu.id_menu)
                .join(EmpresaModulo, EmpresaModulo.id_modulo == ModuloMenu.id_modulo)
                .join(EmpresaUsuarioRol, EmpresaUsuarioRol.id_empresa == EmpresaModulo.id_empresa)
                .join(MenuRol, MenuRol.id_menu == ModuloMenu.id_menu)
                .filter(
                    EmpresaUsuarioRol.estado == True,
                    EmpresaUsuarioRol.id_empresa == filtro.id_empresa,
                    EmpresaUsuarioRol.id_usuario == filtro.id_usuario,
                    EmpresaModulo.estado == True,
                    MenuRol.estado == True,
                    MenuRol.id_rol == EmpresaUsuarioRol.id_rol,
                    ModuloMenu.estado == True,
                    ModuloMenu.id_modulo.in_(id_modulos)
                )
                .all()
            )
            

        # Convertimos a lista plana de IDs
        id_menus = [row.id_menu for row in menus1]

        if not id_menus:
            return []

        # 3. traer menús según el padre actual
        menus = (
            db.query(Menu)
            .filter(
                Menu.id.in_(id_menus),
                Menu.id_padre.is_(filtro.id_padre) if filtro.id_padre is None else Menu.id_padre == filtro.id_padre,
                Menu.id_tipo_menu == filtro.id_tipo_menu
            )
            .order_by(Menu.orden.asc())
            .all()
        )

        resultado = []

        for menu in menus:
            filtro_hijo = MenuFiltroPlus(
                id_usuario=filtro.id_usuario,
                id_empresa=filtro.id_empresa,
                id_padre=menu.id,
                id_tipo_menu=filtro.id_tipo_menu,
                modo=filtro.modo  # heredamos el modo
            )

            children = obtener_menu(db, filtro_hijo)
            nodo = {
                "id": menu.id,
                "icono": menu.icono,
                "nombre": getattr(menu, "nombre", None),
                "id_padre": getattr(menu, "id_padre", None),
                # "id_tipo_menu": getattr(menu, "id_tipo_menu", 1),
                "url": menu.url,
                "orden": getattr(menu, "orden", None),
            }

            if filtro.modo == 1:
                # modo árbol → agregamos children
                nodo["children"] = children
                resultado.append(nodo)
            elif filtro.modo == 2:
                # modo aplanado → agregamos el nodo actual
                resultado.append(nodo)
                # concatenamos los hijos al mismo nivel
                resultado.extend(children)

        return resultado
    except Exception as e:
        print(f"Error en obtener_menu_modulo: {e}")
        return []


      
    
def get_menus_por_modulo_usuario_empresa(db: Session, id_usuario: int, id_empresa: int):
    query = (
        db.query(MenuRol.id_menu)
        .join(EmpresaUsuarioRol, EmpresaUsuarioRol.id_rol == MenuRol.id_rol)
        .filter(
            MenuRol.estado == True,
            EmpresaUsuarioRol.estado == True,
            EmpresaUsuarioRol.id_usuario == id_usuario,
            EmpresaUsuarioRol.id_empresa == id_empresa
        )
    )
    return query.all()     
    
def get_menus_por_usuario_empresa(db: Session, id_usuario: int, id_empresa: int):
    query = (
        db.query(MenuRol.id_menu)
        .join(EmpresaUsuarioRol, EmpresaUsuarioRol.id_rol == MenuRol.id_rol)
        .filter(
            MenuRol.estado == True,
            EmpresaUsuarioRol.estado == True,
            EmpresaUsuarioRol.id_usuario == id_usuario,
            EmpresaUsuarioRol.id_empresa == id_empresa
        )
    )
    return query.all()     

# def get_menus_detalle(db: Session, id_usuario: int, id_empresa: int):
#     # 1. obtener ids de menús disponibles
#     ids = [id_menu for (id_menu,) in get_menus_por_usuario_empresa(db, id_usuario, id_empresa)]

#     if not ids:  # si no hay nada, retornar vacío
#         return []

#     # 2. usarlos como filtro en otra consulta
#     query = db.query(Menu).filter(Menu.id.in_(ids))
#     return query.all()

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict

def obtener_modulos_activos(db: Session, filtro: MenuFiltroPlus) -> List[Modulo]:
    try:
        if filtro.id_usuario is None and filtro.id_empresa is None:
            modulos = (
                db.query(Modulo)
                .order_by(Modulo.nombre.asc())
                .all()
            )
        else:
            modulos = (
                db.query(Modulo.id, Modulo.nombre, Modulo.descripcion)
                .join(EmpresaModulo, EmpresaModulo.id_modulo == Modulo.id)
                .filter(
                    Modulo.estado == True,
                    EmpresaModulo.estado == True,
                    EmpresaModulo.id_empresa == filtro.id_empresa
                )
                .group_by(Modulo.id, Modulo.nombre, Modulo.descripcion)
                .order_by(Modulo.nombre.asc())
                .all()
            )

        if not modulos:
            # Retorna lista vacía si no hay resultados
            return []

        # Convertimos a lista de diccionarios
        arreglo = [{"id": m.id, "nombre": m.nombre, "descripcion": m.descripcion} for m in modulos]
        return [{"id": m.id, "nombre": m.nombre, "descripcion": m.descripcion} for m in modulos]

    except SQLAlchemyError as e:
        # Captura errores de SQLAlchemy (conexión, consulta, etc.)
        print(f"[ERROR] SQLAlchemyError en obtener_modulos_activos: {e}")
        return []

    except Exception as e:
        # Captura cualquier otro error inesperado
        print(f"[ERROR] Exception en obtener_modulos_activos: {e}")
        return []
