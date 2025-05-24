from sqlalchemy import (
    CHAR, Column, Date, DateTime, String, Integer, Boolean, Text, ForeignKey, TIMESTAMP,
    BigInteger, Float  , func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    estado = Column(Boolean, default=True)

class Provincia(Base):
    __tablename__ = 'provincias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    id_region = Column(Integer, ForeignKey('regiones.id'))
    estado = Column(Boolean, default=True)
    region = relationship('Region')

class Comuna(Base):
    __tablename__ = 'comunas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    id_provincia = Column(Integer, ForeignKey('provincias.id'))
    estado = Column(Boolean, default=True)
    provincia = relationship('Provincia')

class Nacionalidad(Base):
    __tablename__ = 'nacionalidad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    gentilicio_nac = Column(String(100), nullable=False)
    iso_nac = Column(CHAR(3), nullable=False)
    estado = Column(Boolean, default=True)

class EstadoCivil(Base):
    __tablename__ = 'estado_civil'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)

class Profesion(Base):
    __tablename__ = 'profesiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    estado = Column(Boolean, default=True)

class NivelEducacional(Base):
    __tablename__ = 'niveles_educacionales'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    estado = Column(Boolean, default=True)

class Direccion(Base):
    __tablename__ = 'direcciones'
    id = Column(Integer, primary_key=True)
    calle = Column(String(150), nullable=False)
    numero = Column(String(20))
    complemento = Column(String(100))
    id_comuna = Column(Integer, ForeignKey('comunas.id'))
    id_provincia = Column(Integer, ForeignKey('provincias.id'))
    id_region = Column(Integer, ForeignKey('regiones.id'))
    codigo_postal = Column(String(10))
    latitud = Column(Float)
    longitud = Column(Float)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())
    estado = Column(Boolean, default=True)

class Persona(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    run_rut = Column(String(12), unique=True)
    pasaporte = Column(String(20))
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100))
    fecha_nacimiento = Column(Date)
    sexo = Column(CHAR(1))
    email = Column(String(150), unique=True)
    telefono = Column(String(20))
    telefono_secundario = Column(String(20))
    id_direccion = Column(Integer, ForeignKey('direcciones.id'))
    id_estado_civil = Column(Integer, ForeignKey('estado_civil.id'))
    id_nacionalidad = Column(Integer, ForeignKey('nacionalidad.id'))
    id_profesion = Column(Integer, ForeignKey('profesiones.id'))
    id_nivel_educacional = Column(Integer, ForeignKey('niveles_educacionales.id'))
    estado = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class FotoPersona(Base):
    __tablename__ = 'fotos_personas'
    id = Column(Integer, primary_key=True)
    id_persona = Column(Integer, ForeignKey('personas.id', ondelete='CASCADE'))
    url_foto = Column(String(250), nullable=False)
    es_principal = Column(Boolean, default=False)
    estado = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
# =====================================
# EMPRESAS Y USUARIOS
# =====================================
# Tabla intermedia: modulo_menu
class ModuloMenu(Base):
    __tablename__ = 'modulo_menu'

    id_modulo = Column(Integer, ForeignKey('modulos.id', ondelete='CASCADE'), primary_key=True)
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# Tabla intermedia: empresa_modulo
class EmpresaModulo(Base):
    __tablename__ = 'empresa_modulo'

    id_empresa = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), primary_key=True)
    id_modulo = Column(Integer, ForeignKey('modulos.id', ondelete='CASCADE'), primary_key=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    empresa = relationship("Empresa", back_populates="modulo")
    modulo = relationship("Modulo", back_populates="empresa")


# Tabla principal: modulos
class Modulo(Base):
    __tablename__ = 'modulos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    empresa = relationship("EmpresaModulo", back_populates="modulo", cascade="all, delete-orphan")
    menu = relationship("ModuloMenu", backref="modulo", cascade="all, delete-orphan")

class TipoEmpresa(Base):
    __tablename__ = 'tipos_empresa'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

    # Relación bidireccional con Empresa
    empresa = relationship("Empresa", back_populates="tipo_empresa")
    # Relación con MenuTipoEmpresa
    menu_tipo_empresa = relationship("MenuTipoEmpresa", back_populates="tipo_empresa")
    
    

class Empresa(Base):
    __tablename__ = 'empresas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    id_tipo_empresa = Column(Integer, ForeignKey('tipos_empresa.id', ondelete='CASCADE'))
    id_direccion = Column(Integer, ForeignKey('direcciones.id', ondelete='SET NULL'))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

    # Relación bidireccional con TipoEmpresa
    tipo_empresa = relationship("TipoEmpresa", back_populates="empresa")

    # Relación con EmpresaModulo
    modulo = relationship("EmpresaModulo", back_populates="empresa")

    # Relación con EmpresaUsuario
    empresa_usuario = relationship("EmpresaUsuario", back_populates="empresa")    
    
    empresa_usuario_rol = relationship("EmpresaUsuarioRol", back_populates="empresa")
    
    configuracion = relationship("ConfiguracionEmpresa", back_populates="empresa")
    
    

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    duracion = Column(Integer, default=20)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())
     # Relación con Direccion
    direccion = relationship("Direccion", back_populates="usuario")
    empresa_usuario = relationship("EmpresaUsuario", back_populates="usuario")
    empresa_usuario_rol = relationship("EmpresaUsuarioRol", back_populates="usuario")   


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

    # Definir la relación con MenuRoles
    menu_rol = relationship("MenuRol", back_populates="rol")
    
    empresa_usuario_rol = relationship("EmpresaUsuarioRol", back_populates="rol")
    
    
class TipoMenu(Base):
    __tablename__ = 'tipos_menu'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)
    
    # Relación con Menu
    menu = relationship("Menu", back_populates="tipo_menu")  
    

class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    icono = Column(String(50))
    id_tipo_menu = Column(Integer, ForeignKey('tipos_menu.id'))
    id_padre = Column(Integer, ForeignKey('menus.id', ondelete='SET NULL'))
    url = Column(String(255))
    descripcion = Column(String(255))
    token = Column(String(255), unique=True)
    orden = Column(Integer)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    fecha_modificacion = Column(TIMESTAMP, default=datetime.utcnow)

    # Relación con TipoMenu
    tipo_menu = relationship("TipoMenu", back_populates="menu")

    # Relación con MenuRoles
    menu_rol = relationship("MenuRol", back_populates="menu")
    
    menu_tipo_empresa = relationship("MenuTipoEmpresa", back_populates="menu")
    
    
class MenuRol(Base):
    __tablename__ = "menu_rol"

    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    # Relación con Menu
    menu = relationship("Menu", back_populates="menu_rol")

    # Relación con Rol
    rol = relationship("Rol", back_populates="menu_rol")
    
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

    # Relación con Empresa
    empresa = relationship("Empresa", back_populates="empresa_usuario")

    # Relación con Usuario (si es necesario)
    usuario = relationship("Usuario", back_populates="empresa_usuario")

class EmpresaUsuarioRol(Base):
    __tablename__ = "empresa_usuario_rol"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    fecha_creacion = Column(TIMESTAMP, default=func.now())
    fecha_modificacion = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    estado = Column(Boolean, default=True)

    empresa = relationship("Empresa", back_populates="empresa_usuario_rol")
    usuario = relationship("Usuario", back_populates="empresa_usuario_rol")
    rol = relationship("Rol", back_populates="empresa_usuario_rol")

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

    empresa = relationship("Empresa", back_populates="configuracion")

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
    menu = relationship("Menu", back_populates="menu_tipo_empresa")
    # Relación con TipoEmpresa
    tipo_empresa = relationship("TipoEmpresa", back_populates="menu_tipo_empresa")


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

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    username = Column(String, nullable=False)
    exito = Column(Boolean, nullable=False)
    mensaje = Column(String, nullable=False)
    ip = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())
