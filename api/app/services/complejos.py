from datetime import datetime, timedelta
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.schemas.menu import MenuBase, TipoMenu
from app.services.usuario_empresa import obtener_empresas_por_usuario
from app.models.empresa import Empresa
from app.utils.security import generar_jwt
from app.services.acceso import create_acceso
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioLogin
from app.schemas.complejos import AccesoDuracion, DatosAcceso
from app.models.acceso import Acceso  # Corregir la importación

def get_objeto_acceso(db: Session, user: UsuarioLogin) -> DatosAcceso:
    #traer la informacion del usuario
    # Buscar el usuario con el nombre de usuario proporcionado

    userObj = db.query(Usuario).filter(
        or_(Usuario.nombre_usuario == user.userName, 
            Usuario.email == user.userName)
        ).first()
    if not userObj:
        raise Exception("Usuario no encontrado")
    
    idUsuario = userObj.id
    minutosAcceso = userObj.duracion

    # Se genera el Token
    newToken = generar_jwt(idUsuario, minutosAcceso)
        
    # Crear el acceso
    db_acceso = Acceso(
        usuario_id=idUsuario,
        empresa_id=None,
        token=newToken,
        fecha_ingreso=datetime.now(),
        fecha_creacion=datetime.now(),
        fecha_vencimiento=datetime.now() + timedelta(minutes=minutosAcceso),
    )
    # retornar el token
    objAcceso = create_acceso(db, db_acceso)
    #retornar los roles
    #crear el super objeto

    empresaList = obtener_empresas_por_usuario(db, idUsuario)
    
    duracion = AccesoDuracion(
        inicio = datetime.now(),
        termino = datetime.now()+ timedelta(minutes=minutosAcceso),
        minutos = minutosAcceso
    )
    
    menus_dummies: List[MenuBase] = [
        MenuBase(id=11, nombre="Dashboard", tipo=TipoMenu.url, valor="/dashboard", icono="dashboard", orden=5, padre_id=None, estado=0),
        MenuBase(id=12, nombre="Estadísticas", tipo=TipoMenu.url, valor="/estadisticas", icono="pie-chart", orden=6, padre_id=None, estado=0),
        MenuBase(id=13, nombre="Ayuda", tipo=TipoMenu.url, valor="/ayuda", icono="help-circle", orden=7, padre_id=None, estado=0),

        MenuBase(id=20, nombre="FAQ", tipo=TipoMenu.url, valor="/ayuda/faq", icono="help-circle", orden=1, padre_id=13, estado=0),
        MenuBase(id=14, nombre="Soporte", tipo=TipoMenu.formulario, valor="soporte_form", icono="life-buoy", orden=8, padre_id=None, estado=0),        MenuBase(id=1, nombre="Inicio", tipo=TipoMenu.url, valor="/inicio", icono="home", orden=1, padre_id=None, estado=0),
        MenuBase(id=2, nombre="Usuarios", tipo=TipoMenu.formulario, valor="usuarios_form", icono="users", orden=2, padre_id=None, estado=0),

        MenuBase(id=5, nombre="Perfil", tipo=TipoMenu.formulario, valor="perfil_form", icono="user", orden=1, padre_id=2, estado=0),
        MenuBase(id=15, nombre="Cambiar Contraseña", tipo=TipoMenu.formulario, valor="cambiar_pass", icono="key", orden=2, padre_id=5, estado=0),

        MenuBase(id=6, nombre="Permisos", tipo=TipoMenu.formulario, valor="permisos_form", icono="lock", orden=2, padre_id=2, estado=0),
        MenuBase(id=16, nombre="Logs de Usuario", tipo=TipoMenu.url, valor="/usuarios/logs", icono="file-text", orden=3, padre_id=2, estado=0),
        MenuBase(id=17, nombre="Carga Masiva", tipo=TipoMenu.otro, valor="carga_csv", icono="upload", orden=4, padre_id=2, estado=0),        MenuBase(id=7, nombre="Informe Diario", tipo=TipoMenu.url, valor="/reportes/diario", icono="calendar", orden=1, padre_id=3, estado=0),


        MenuBase(id=3, nombre="Reportes", tipo=TipoMenu.url, valor="/reportes", icono="bar-chart", orden=3, padre_id=None, estado=0),

        MenuBase(id=8, nombre="Informe Mensual", tipo=TipoMenu.url, valor="/reportes/mensual", icono="calendar-check", orden=2, padre_id=3, estado=0),
        MenuBase(id=18, nombre="Gráficos Comparativos", tipo=TipoMenu.url, valor="/reportes/graficos", icono="bar-chart-2", orden=3, padre_id=3, estado=0),

        MenuBase(id=4, nombre="Configuración", tipo=TipoMenu.url, valor="/config", icono="settings", orden=4, padre_id=None, estado=0),
        
        MenuBase(id=9, nombre="Temas", tipo=TipoMenu.otro, valor="temas_config", icono="palette", orden=1, padre_id=4, estado=0),
        MenuBase(id=10, nombre="Notificaciones", tipo=TipoMenu.formulario, valor="notif_form", icono="bell", orden=2, padre_id=4, estado=0),
        MenuBase(id=19, nombre="Preferencias", tipo=TipoMenu.formulario, valor="prefs_form", icono="sliders", orden=3, padre_id=4, estado=0),
 
    ]
    return DatosAcceso(
        nombre_usuario = userObj.nombre_usuario,
        email = userObj.email,
        token = objAcceso.token,
        duracionAcceso = duracion, 
        empresas = empresaList,  # Lista de empresas
        empresaSeleccionada= empresaList[0].id,
        menu = menus_dummies
    )

    


