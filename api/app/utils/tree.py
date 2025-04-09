from typing import Dict, List
from app.models.models import MenuGeneral


def construir_arbol_ordenado(data: List[MenuGeneral]) -> List[MenuGeneral]:
    # Ya son objetos MenuGeneral, no necesitamos convertirlos
    menus = data
    
    # Creamos un mapa por id
    mapa_menus = {menu.id: menu for menu in menus}
    
    # Creamos un mapa de hijos por id_padre
    hijos_por_padre = {}
    for menu in menus:
        hijos_por_padre.setdefault(menu.id_padre, []).append(menu)
    
    # Ordenamos los hijos por 'orden'
    for lista_hijos in hijos_por_padre.values():
        lista_hijos.sort(key=lambda x: x.orden)
    
    # Recursivo: agrega un menú y todos sus hijos en orden
    def agregar_con_hijos(menu: MenuGeneral, resultado: List[MenuGeneral]):
        resultado.append(menu)
        hijos = hijos_por_padre.get(menu.id, [])
        for hijo in hijos:
            agregar_con_hijos(hijo, resultado)
    
    # Empezamos por los menús raíz (id_padre = None)
    resultado_final = []
    for menu_raiz in sorted(hijos_por_padre.get(None, []), key=lambda x: x.orden):
        agregar_con_hijos(menu_raiz, resultado_final)
    
    return resultado_final
