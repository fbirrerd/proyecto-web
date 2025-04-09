from sqlalchemy import Column, Integer, String, Float, Text, Boolean, TIMESTAMP, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regiones'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    geom_wkt = Column(Text)
    area_km2 = Column(Float)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class Provincia(Base):
    __tablename__ = 'provincias'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(5), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('regiones.id'))
    geom_wkt = Column(Text)
    area_km2 = Column(Float)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class Comuna(Base):
    __tablename__ = 'comunas'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    provincia_id = Column(Integer, ForeignKey('provincias.id'))
    region_id = Column(Integer, ForeignKey('regiones.id'))
    geom_wkt = Column(Text)
    area_km2 = Column(Float)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class Direccion(Base):
    __tablename__ = 'direcciones'
    id = Column(Integer, primary_key=True)
    calle = Column(String(150), nullable=False)
    numero = Column(String(20))
    complemento = Column(String(100))
    comuna_id = Column(Integer, ForeignKey('comunas.id'))
    provincia_id = Column(Integer, ForeignKey('provincias.id'))
    region_id = Column(Integer, ForeignKey('regiones.id'))
    codigo_postal = Column(String(10))
    latitud = Column(Float)
    longitud = Column(Float)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class Empresa(Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    tipo_empresa = Column(String(50), nullable=False)
    direccion_id = Column(Integer, ForeignKey('direcciones.id'))
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    direccion_id = Column(Integer, ForeignKey('direcciones.id'))
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Integer, default=0)
    duracion = Column(Integer, default=20)

class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class UsuarioEmpresaRol(Base):
    __tablename__ = 'usuario_empresa_rol'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_empresa = Column(Integer, ForeignKey('empresas.id'))
    id_rol = Column(Integer, ForeignKey('roles.id'))
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class MenuGeneral(Base):
    __tablename__ = "menus_generales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    icono = Column(String(50))
    ruta = Column(String(255))
    
    id_padre = Column(Integer, ForeignKey("menus_generales.id", ondelete="SET NULL"), nullable=True)
    es_publico = Column(Boolean, default=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    tipo = Column(String(20), nullable=True)
    orden = Column(Integer)
    estado = Column(Boolean, default=True)

    # Relación recursiva para manejar submenús
    padre = relationship("MenuGeneral", remote_side=[id], backref="submenus")

    def __repr__(self):
        return f"<MenuGeneral(id={self.id}, nombre='{self.nombre}')>"

class MenuGeneralRol(Base):
    __tablename__ = 'menu_general_rol'
    id_menu = Column(Integer, ForeignKey('menus_generales.id'), primary_key=True)
    id_rol = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class MenuEspecifico(Base):
    __tablename__ = "menus_especificos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    icono = Column(String(50))
    ruta = Column(String(255))
    
    id_padre = Column(Integer, ForeignKey("menus_especificos.id", ondelete="SET NULL"), nullable=True)
    es_publico = Column(Boolean, default=False)
    tipo_ventana = Column(String(50))  # 'popup', 'iframe', 'pagina'
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    tipo = Column(String(20), nullable=True)
    orden = Column(Integer)
    estado = Column(Boolean, default=True)

    # Relación recursiva para submenús
    padre = relationship("MenuEspecifico", remote_side=[id], backref="submenus")

    def __repr__(self):
        return f"<MenuEspecifico(id={self.id}, nombre='{self.nombre}')>"

class MenuEspecificoTipoEmpresa(Base):
    __tablename__ = 'menu_especifico_tipo_empresa'
    id_menu = Column(Integer, ForeignKey('menus_especificos.id'), primary_key=True)
    tipo_empresa = Column(String(50), primary_key=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class MenuPublico(Base):
    __tablename__ = 'menus_publicos'
    id = Column(Integer, primary_key=True)
    id_menu = Column(Integer, ForeignKey('menus_generales.id'))
    url_publica = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Boolean, default=True)

class ConfiguracionEmpresa(Base):
    __tablename__ = 'configuracion_empresa'
    id = Column(Integer, primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    clave = Column(String(255), nullable=False)
    valor = Column(Text)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())

class Auditoria(Base):
    __tablename__ = 'auditoria'
    id = Column(BigInteger, primary_key=True)
    fecha_hora = Column(TIMESTAMP, default=func.now())
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    tabla_afectada = Column(String(255), nullable=False)
    accion = Column(String(255), nullable=False)
    registro_id = Column(Integer)
    datos_antes = Column(Text)
    datos_despues = Column(Text)
    direccion_ip = Column(String(45))

class ParametroSistema(Base):
    __tablename__ = 'parametro_sistema'
    id = Column(Integer, primary_key=True)
    clave = Column(String(255), unique=True, nullable=False)
    valor = Column(Text)
    descripcion = Column(Text)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
    estado = Column(Integer, default=0)

class Acceso(Base):
    __tablename__ = 'acceso'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    fecha_ingreso = Column(TIMESTAMP, default=func.now())
    fecha_vencimiento = Column(TIMESTAMP, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now())
