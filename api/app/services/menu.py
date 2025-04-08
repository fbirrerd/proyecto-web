from sqlalchemy.orm import Session
from app.models.menu import Menu
from app.schemas.menu import MenuSchema

def obtener_menus_por_usuario(db: Session, usuario_id: int):

    menu_items = db.query(Menu).filter(Menu.estado == 0).all()  # ejemplo
    menus = [MenuSchema.from_orm(item) for item in menu_items]        

    return menus            
    
    
    # else:
    # Realizamos la consulta con las condiciones que mencionaste
        # result1 = db.query(UsuarioEmpresa.usuario_id).filter(
        #     and_(
        #         UsuarioEmpresa.usuario_id == usuario_id,
        #         Empresa.estado == 0
        #     )
        # ).all()

        # # Extraer los ids de empresas de result1
        # empresa_ids = [r.empresa_id for r in result1]

        # # Filtrar result2 usando los ids de empresa extraídos de result1
        # result2 = db.query(Empresa.id, Empresa.nombre).filter(
        #     and_(
        #         Empresa.id.in_(empresa_ids),  # Filtrar por los ids de empresas
        #         Empresa.estado==0
        #     )
        # ).all()
        # return result2        
