from sqlalchemy import (
    Column, DateTime, String, Integer, Boolean, Text, ForeignKey, TIMESTAMP,
    Double, BigInteger, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

# =====================================
# TABLAS GEOGRÁFICAS
# =====================================

class Region(Base):
    __tablename__ = 'regiones'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    geom_wkt = Column(Text)
    area_km2 = Column(Double)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)
    estado = Column(Boolean, default=True)

class Provincia(Base):
    __tablename__ = 'provincias'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    id_region = Column(Integer, ForeignKey('regiones.id'))
    geom_wkt = Column(Text)
    area_km2 = Column(Double)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)
    estado = Column(Boolean, default=True)

class Comuna(Base):
    __tablename__ = 'comunas'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    id_providencia = Column(Integer, ForeignKey('provincias.id'))
    id_region = Column(Integer, ForeignKey('regiones.id'))
    geom_wkt = Column(Text)
    area_km2 = Column(Double)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)
    estado = Column(Boolean, default=True)

# =====================================
# DIRECCIONES
# =====================================

class Direccion(Base):
    __tablename__ = 'direcciones'

    id = Column(Integer, primary_key=True)
    calle = Column(String(150), nullable=False)
    numero = Column(String(20))
    complemento = Column(String(100))
    id_comuna = Column(Integer, ForeignKey('comunas.id'))
    id_providencia = Column(Integer, ForeignKey('provincias.id'))
    id_region = Column(Integer, ForeignKey('regiones.id'))
    codigo_postal = Column(String(10))
    latitud = Column(Double)
    longitud = Column(Double)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)
    estado = Column(Boolean, default=True)

# =====================================
# EMPRESAS Y USUARIOS
# =====================================

class TipoEmpresa(Base):
    __tablename__ = 'tipos_empresa'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    id_tipo_empresa = Column(Integer, ForeignKey('tipos_empresa.id', ondelete='CASCADE'))
    id_direccion = Column(Integer, ForeignKey('direcciones.id', ondelete='SET NULL'))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False, unique=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    id_direccion = Column(Integer, ForeignKey('direcciones.id', ondelete='SET NULL'))
    duracion = Column(Integer, default=20)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

# =====================================
# ROLES Y MENÚS
# =====================================

class Rol(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

class TipoMenu(Base):
    __tablename__ = 'tipos_menu'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    icono = Column(String(50))
    ruta = Column(String(255))
    id_tipo_menu = Column(Integer, ForeignKey('tipos_menu.id'))
    id_padre = Column(Integer, ForeignKey('menus.id', ondelete='SET NULL'))
    url = Column(String(255))
    descripcion = Column(String(255))
    token = Column(String(255), unique=True)
    orden = Column(Integer)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

class MenuRol(Base):
    __tablename__ = "menu_rol"

    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # menu = relationship("Menu", back_populates="menu_roles")
    # rol = relationship("Rol", back_populates="menu_roles")

# =====================================
# RELACIONES EMPRESA-USUARIO-ROL
# =====================================

class EmpresaUsuario(Base):
    __tablename__ = "empresa_usuario"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    estado = Column(Boolean, default=True)

    # empresa = relationship("Empresa", back_populates="empresa_usuarios")
    # usuario = relationship("Usuario", back_populates="empresa_usuarios")

class EmpresaUsuarioRol(Base):
    __tablename__ = "empresa_usuario_rol"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    estado = Column(Boolean, default=True)

    # empresa = relationship("Empresa", back_populates="empresa_usuario_roles")
    # usuario = relationship("Usuario", back_populates="empresa_usuario_roles")
    # rol = relationship("Rol", back_populates="empresa_usuario_roles")

# =====================================
# CONFIGURACIÓN Y ACCESO
# =====================================

class ConfiguracionEmpresa(Base):
    __tablename__ = "configuracion_empresa"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    clave = Column(String(255), primary_key=True)
    valor = Column(Text)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # empresa = relationship("Empresa", back_populates="configuraciones")

class Auditoria(Base):
    __tablename__ = 'auditoria'

    id = Column(BigInteger, primary_key=True)
    fecha_hora = Column(TIMESTAMP, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_empresa = Column(Integer, ForeignKey('empresas.id'))
    tabla_afectada = Column(String(255), nullable=False)
    accion = Column(String(255), nullable=False)
    registro_id = Column(Integer)
    datos_antes = Column(Text)
    datos_despues = Column(Text)
    direccion_ip = Column(String(45))

class Acceso(Base):
    __tablename__ = 'acceso'

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_empresa = Column(Integer, ForeignKey('empresas.id'))
    fecha_ingreso = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_vencimiento = Column(TIMESTAMP, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

# =====================================
# MENÚS ESPECÍFICOS Y RELACIONES
# =====================================

class MenuPublico(Base):
    __tablename__ = 'menus_publicos'

    id = Column(Integer, primary_key=True)
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))
    token = Column(String(255), unique=True)
    fecha_expiracion = Column(TIMESTAMP)
    estado = Column(Boolean, default=True)

class MenuTipoEmpresa(Base):
    __tablename__ = "menu_tipo_empresa"

    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)
    id_tipo_empresa = Column(Integer, ForeignKey("tipos_empresa.id", ondelete="CASCADE"), primary_key=True)

    # Relaciones opcionales (solo si necesitas navegar desde esta tabla a otras)
    # menu = relationship("Menu", back_populates="menu_tipo_empresas")
    # tipo_empresa = relationship("TipoEmpresa", back_populates="menu_tipo_empresas")

# =====================================
# PARÁMETROS DEL SISTEMA
# =====================================

class ParametroSistema(Base):
    __tablename__ = 'parametro_sistema'

    id = Column(Integer, primary_key=True)
    clave = Column(String(255), unique=True, nullable=False)
    valor = Column(Text)
    descripcion = Column(Text)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)
    estado = Column(Integer, default=0)



# =====================================
# LOG DE ACCESO
# =====================================
class LogAcceso(Base):
    __tablename__ = "logs_acceso"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    username = Column(String, nullable=False)
    exito = Column(Boolean, nullable=False)
    mensaje = Column(String, nullable=False)
    ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
