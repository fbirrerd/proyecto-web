

from app.models.models import EmpresaUsuario
from sqlalchemy.orm import Session


from datetime import datetime, timezone



def getDatosEmpresaUsuario(db: Session):
    empresaUsuarioList = db.query(EmpresaUsuario).all()
    if not empresaUsuarioList:
        raise Exception("Registro EmpresaUsuario no encontrada ")
    
    # Si hay empresas, las convertimos a Pydantic
    empresaUsuario_pydantic_list = [EmpresaUsuario.from_orm(dato) for dato in empresaUsuarioList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if empresaUsuario_pydantic_list:
        return empresaUsuario_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
def getDatosEmpresaUsuarioList(db: Session):
    empresaUsuarioList = db.query(EmpresaUsuario).all()
    if not empresaUsuarioList:
        raise Exception("Registro EmpresaUsuario no encontrada ")
    
    # Si hay empresas, las convertimos a Pydantic
    empresaUsuario_pydantic_list = [EmpresaUsuario.from_orm(dato) for dato in empresaUsuarioList]

    # Si necesitas devolver solo una empresa (por ejemplo, la primera), puedes hacer esto:
    if empresaUsuario_pydantic_list:
        return empresaUsuario_pydantic_list  # O devolver la lista completa si es necesario
    else:
        return None
  
  
  
   
  
  
  
  
  