from typing import Dict, List
from app.schemas.menuGeneral import MenuOut
from app.models.models import MenuGeneral


def getArbolOrdenadoTabulado(data: List[MenuGeneral]) -> List:
    # Ya son objetos MenuGeneral, no necesitamos convertirlos
    menus_con_nivel = []
    
    for menu in data:
        nivel = calcular_nivel(menu)
        tiene_hijos = len([hijo for hijo in data if hijo.id_padre == menu.id]) > 0
        menus_con_nivel.append({
            'id': menu.id,
            'ruta': menu.ruta,
            'icono': menu.icono,
            'orden': menu.orden,
            'nombre': menu.nombre,
            'id_padre': menu.id_padre,            
            'tipo': menu.tipo,
            'nivel': nivel,
            'hijos': tiene_hijos,
            'estado': menu.estado
        })    
    
 # Crear un diccionario de hijos por cada menú padre
    hijos_por_padre = {}
    for menu in menus_con_nivel:
        hijos_por_padre.setdefault(menu['id_padre'], []).append(menu)
    
    # Ordenamos los hijos por 'orden' (de menor a mayor)
    for lista_hijos in hijos_por_padre.values():
        lista_hijos.sort(key=lambda x: x['orden'])  # Asegúrate de que 'orden' esté presente

    # Función recursiva para agregar los menús junto con sus hijos
    def agregar_con_hijos(menu: dict, resultado: List):
        resultado.append(menu)
        hijos = hijos_por_padre.get(menu['id'], [])
        for hijo in hijos:
            agregar_con_hijos(hijo, resultado)

    # Empezamos por los menús raíz (padre_id = None)
    resultado_final = []
    for menu_raiz in sorted(hijos_por_padre.get(None, []), key=lambda x: x['orden']):
        agregar_con_hijos(menu_raiz, resultado_final)

    return resultado_final       



def calcular_nivel(menu):
    if menu.padre is None:
        return 0
    return calcular_nivel(menu.padre) + 1