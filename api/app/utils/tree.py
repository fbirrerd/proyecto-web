from typing import Any, Dict, List
from app.schemas.menus import MenuAcceso


def getArbolOrdenadoTabulado(data: List[MenuAcceso]) -> List[Any]:
    # Ya son objetos MenuGeneral, no necesitamos convertirlos
    menus_con_nivel = []

    try:
        # Iterar sobre cada menú para calcular su nivel y verificar si tiene hijos
        for menu in data:
            try:
                nivel = calcular_nivel(menu, data)  # Pasamos el listado completo de menús
                tiene_hijos = len([hijo for hijo in data if hijo.id_padre == menu.id]) > 0
                menus_con_nivel.append({
                    'id': menu.id,
                    'url': menu.url,
                    'icono': menu.icono,
                    'orden': menu.orden,
                    'nombre': menu.nombre,
                    'id_padre': menu.id_padre,
                    # 'tipo': menu.tipo,
                    'nivel': nivel,
                    'hijos': tiene_hijos,
                    'estado': menu.estado,
                    'descripcion': menu.descripcion
                })
                # print(f"✅ Menú '{menu.nombre}' procesado con nivel {nivel} y {'con hijos' if tiene_hijos else 'sin hijos'}... descripcion {menu.descripcion} ")
            except Exception as e:
                print(f"🔴 Error al procesar el menú con ID {menu.id}: {e}")
    
        # Crear un diccionario de hijos por cada menú padre
        hijos_por_padre = {}
        for menu in menus_con_nivel:
            try:
                hijos_por_padre.setdefault(menu['id_padre'], []).append(menu)
                # print(f"🟡 Hijos agregados para el menú ID {menu['id_padre']}")
            except Exception as e:
                print(f"🔴 Error al agregar hijos para el menú ID {menu['id']}: {e}")
    
        # Ordenamos los hijos por 'orden' (de menor a mayor)
        for lista_hijos in hijos_por_padre.values():
            try:
                lista_hijos.sort(key=lambda x: x['orden'])  # Asegúrate de que 'orden' esté presente
                # print(f"🟢 Hijos ordenados para el menú padre {lista_hijos[0]['id_padre']}")
            except Exception as e:
                print(f"🔴 Error al ordenar los hijos de un menú padre: {e}")
    
        # Función recursiva para agregar los menús junto con sus hijos
        def agregar_con_hijos(menu: dict, resultado: List):
            try:
                resultado.append(menu)
                hijos = hijos_por_padre.get(menu['id'], [])
                # print(f"🟡 Agregando hijos para el menú ID {menu['id']}")
                for hijo in hijos:
                    agregar_con_hijos(hijo, resultado)
            except Exception as e:
                print(f"🔴 Error al agregar el menú con ID {menu['id']} y sus hijos: {e}")

        # Empezamos por los menús raíz (padre_id = None)
        resultado_final = []
        for menu_raiz in sorted(hijos_por_padre.get(None, []), key=lambda x: x['orden']):
            try:
                # print(f"🌳 Procesando menú raíz '{menu_raiz['nombre']}'")
                agregar_con_hijos(menu_raiz, resultado_final)
            except Exception as e:
                print(f"🔴 Error al procesar el menú raíz con ID {menu_raiz['id']}: {e}")

        return resultado_final

    except Exception as e:
        print(f"🔴 Error general al construir el árbol: {e}")
        return []


def calcular_nivel(menu, data):
    try:
        if menu.id_padre is None:
            return 0  # Si no tiene padre, el nivel es 0 (raíz)
        
        # Encontramos el menú padre y calculamos su nivel
        menu_padre = next((m for m in data if m.id == menu.id_padre), None)
        if menu_padre:
            return calcular_nivel(menu_padre, data) + 1
        else:
            return 0  # Si no se encuentra el padre, asumimos nivel 0
    except Exception as e:
        print(f"🔴 Error al calcular el nivel del menú con ID {menu.id}: {e}")
        return 0
