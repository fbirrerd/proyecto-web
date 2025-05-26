from sqlalchemy import (
    CHAR, TIMESTAMP, Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text, Float, BigInteger, UniqueConstraint, func
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regiones'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10))
    capital = Column(String(100))
    estado = Column(Boolean, default=True)


class Provincia(Base):
    __tablename__ = 'provincias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    id_region = Column(Integer, ForeignKey('regiones.id'))
    estado = Column(Boolean, default=True)
    region = relationship("Region")


class Comuna(Base):
    __tablename__ = 'comunas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    id_provincia = Column(Integer, ForeignKey('provincias.id'))
    estado = Column(Boolean, default=True)
    provincia = relationship("Provincia")


class Nacionalidad(Base):
    __tablename__ = 'nacionalidad'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    gentilicio_nac = Column(String(100), nullable=False)
    iso_nac = Column(String(3), nullable=False)
    estado = Column(Boolean, default=True)


class EstadoCivil(Base):
    __tablename__ = 'estado_civil'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)


class Profesion(Base):
    __tablename__ = 'profesion'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    estado = Column(Boolean, default=True)


class NivelEducacional(Base):
    __tablename__ = 'niveles_educacionales'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), unique=True, nullable=False)
    estado = Column(Boolean, default=True)


class Direccion(Base):
    __tablename__ = 'direccion'
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
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(Boolean, default=True)


class TipoEmpresa(Base):
    __tablename__ = 'tipos_empresa'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class Empresa(Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    id_tipo_empresa = Column(Integer, ForeignKey('tipos_empresa.id', ondelete='CASCADE'))
    id_direccion = Column(Integer, ForeignKey('direccion.id', ondelete='SET NULL'))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)

class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    run_rut = Column(String(12), unique=True, nullable=True)
    pasaporte = Column(String(20), nullable=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)
    sexo = Column(CHAR(1), nullable=True)
    email = Column(String(150), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)
    telefono_secundario = Column(String(20), nullable=True)
    id_direccion = Column(Integer, ForeignKey("direccion.id"), nullable=True)
    id_estado_civil = Column(Integer, ForeignKey("estado_civil.id"), nullable=True)
    id_nacionalidad = Column(Integer, ForeignKey("nacionalidad.id"), nullable=True)
    id_profesion = Column(Integer, ForeignKey("profesion.id"), nullable=True)
    id_nivel_educacional = Column(Integer, ForeignKey("niveles_educacionales.id"), nullable=True)
    estado = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    fotos = relationship("FotoPersona", back_populates="persona")
    usuario = relationship("Usuario", back_populates="persona", uselist=False)

class FotoPersona(Base):
    __tablename__ = "fotos_personas"

    id = Column(Integer, primary_key=True, index=True)
    id_persona = Column(Integer, ForeignKey("personas.id", ondelete="CASCADE"))
    url_foto = Column(String(250), nullable=False)
    es_principal = Column(Boolean, default=False)
    estado = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    persona = relationship("Persona", back_populates="fotos")

class DashboardInicial(Base):
    __tablename__ = "dashboard_inicial"

    id = Column(Integer, primary_key=True, index=True)
    pagina = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=func.now())
    fecha_modificacion = Column(DateTime, default=func.now(), onupdate=func.now())

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    nombre_mostrar = Column(String(200), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    duracion = Column(Integer, default=20)
    pagina_inicio = Column(String(255), nullable=False)
    id_dashboard = Column(Integer, ForeignKey("dashboard_inicial.id", ondelete="SET NULL"), nullable=True)
    id_persona = Column(Integer, ForeignKey("personas.id", ondelete="SET NULL"), nullable=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    persona = relationship("Persona", back_populates="usuario")


class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class TipoMenu(Base):
    __tablename__ = 'tipos_menu'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


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
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class MenuRol(Base):
    __tablename__ = 'menu_rol'
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True)
    id_rol = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class EmpresaUsuario(Base):
    __tablename__ = 'empresa_usuario'
    id_empresa = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class EmpresaUsuarioRol(Base):
    __tablename__ = 'empresa_usuario_rol'
    id_empresa = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id', ondelete='CASCADE'), primary_key=True)
    id_rol = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class ConfiguracionEmpresa(Base):
    __tablename__ = 'configuracion_empresa'
    id_empresa = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), primary_key=True)
    clave = Column(String(255), primary_key=True)
    valor = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class Auditoria(Base):
    __tablename__ = 'auditoria'
    id = Column(BigInteger, primary_key=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_empresa = Column(Integer, ForeignKey('empresas.id'))
    tabla_afectada = Column(String(255), nullable=False)
    accion = Column(String(255), nullable=False)
    id_registro = Column(Integer)
    datos_antes = Column(Text)
    datos_despues = Column(Text)
    direccion_ip = Column(String(45))


class Acceso(Base):
    __tablename__ = 'acceso'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    id_empresa = Column(Integer, ForeignKey('empresas.id'))
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class MenusPublicos(Base):
    __tablename__ = 'menus_publicos'
    id = Column(Integer, primary_key=True)
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'))
    token = Column(String(255), unique=True)
    fecha_expiracion = Column(DateTime)
    estado = Column(Boolean, default=True)


class MenuTipoEmpresa(Base):
    __tablename__ = 'menu_tipo_empresa'
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True)
    id_tipo_empresa = Column(Integer, ForeignKey('tipos_empresa.id', ondelete='CASCADE'), primary_key=True)


class ParametroSistema(Base):
    __tablename__ = 'parametro_sistema'
    id = Column(Integer, primary_key=True)
    clave = Column(String(255), unique=True, nullable=False)
    valor = Column(Text)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(Boolean, default=True)


class LogAcceso(Base):
    __tablename__ = 'logs_acceso'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_empresa = Column(Integer, ForeignKey('empresas.id'))
    username = Column(String, nullable=False)
    exito = Column(Boolean, nullable=False)
    mensaje = Column(Text, nullable=False)
    ip = Column(String)
    user_agent = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)


class Modulo(Base):
    __tablename__ = 'modulos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class EmpresaModulo(Base):
    __tablename__ = 'empresa_modulo'
    id_empresa = Column(Integer, ForeignKey('empresas.id', ondelete='CASCADE'), primary_key=True)
    id_modulo = Column(Integer, ForeignKey('modulos.id', ondelete='CASCADE'), primary_key=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)


class ModuloMenu(Base):
    __tablename__ = 'modulo_menu'
    id_modulo = Column(Integer, ForeignKey('modulos.id', ondelete='CASCADE'), primary_key=True)
    id_menu = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow)
