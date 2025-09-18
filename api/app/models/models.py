from sqlalchemy import BigInteger, Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Float, CheckConstraint, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# =========================
# TABLAS GEOGRÁFICAS
# =========================
class Region(Base):
    __tablename__ = "regiones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    abreviatura = Column(String(10))
    capital = Column(String(100))
    estado = Column(Boolean, default=True)

    provincias = relationship("Provincia", back_populates="region", cascade="all, delete")


class Provincia(Base):
    __tablename__ = "provincias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    id_region = Column(Integer, ForeignKey("regiones.id", ondelete="CASCADE"))
    estado = Column(Boolean, default=True)

    region = relationship("Region", back_populates="provincias")
    comunas = relationship("Comuna", back_populates="provincia", cascade="all, delete")


class Comuna(Base):
    __tablename__ = "comunas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    codigo = Column(String(10))
    id_provincia = Column(Integer, ForeignKey("provincias.id", ondelete="CASCADE"))
    estado = Column(Boolean, default=True)

    provincia = relationship("Provincia", back_populates="comunas")


class Nacionalidad(Base):
    __tablename__ = "nacionalidad"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    gentilicio_nac = Column(String(100), nullable=False)
    iso_nac = Column(String(3), nullable=False)
    estado = Column(Boolean, default=True)


class EstadoCivil(Base):
    __tablename__ = "estado_civil"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)


class Profesion(Base):
    __tablename__ = "profesion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    estado = Column(Boolean, default=True)


class NivelEducacional(Base):
    __tablename__ = "niveles_educacionales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    estado = Column(Boolean, default=True)


# =========================
# TABLA DE DIRECCIONES
# =========================
class Direccion(Base):
    __tablename__ = "direccion"

    id = Column(Integer, primary_key=True, index=True)
    calle = Column(String(150), nullable=False)
    numero = Column(String(20))
    complemento = Column(String(100))
    id_comuna = Column(Integer, ForeignKey("comunas.id", ondelete="SET NULL"))
    id_provincia = Column(Integer, ForeignKey("provincias.id", ondelete="SET NULL"))
    id_region = Column(Integer, ForeignKey("regiones.id", ondelete="SET NULL"))
    codigo_postal = Column(String(10))
    latitud = Column(Float)
    longitud = Column(Float)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(Boolean, default=True)


# =========================
# TABLAS DE EMPRESAS Y USUARIOS
# =========================
class TipoEmpresa(Base):
    __tablename__ = "tipos_empresa"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    id_tipo_empresa = Column(Integer, ForeignKey("tipos_empresa.id", ondelete="CASCADE"))
    id_direccion = Column(Integer, ForeignKey("direccion.id", ondelete="SET NULL"))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DashboardInicial(Base):
    __tablename__ = "dashboard_inicial"

    id = Column(Integer, primary_key=True, index=True)
    pagina = Column(String(100), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Persona(Base):
    __tablename__ = "personas"

    id = Column(Integer, primary_key=True, index=True)
    run_rut = Column(String(20), unique=True)
    pasaporte = Column(String(20))
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100))
    fecha_nacimiento = Column(Date)
    sexo = Column(String(1), CheckConstraint("sexo IN ('M','F','O')"))
    email = Column(String(150), unique=True)
    telefono = Column(String(20))
    telefono_secundario = Column(String(20))
    id_direccion = Column(Integer, ForeignKey("direccion.id", ondelete="SET NULL"))
    id_estado_civil = Column(Integer, ForeignKey("estado_civil.id", ondelete="SET NULL"))
    id_nacionalidad = Column(Integer, ForeignKey("nacionalidad.id", ondelete="SET NULL"))
    id_profesion = Column(Integer, ForeignKey("profesion.id", ondelete="SET NULL"))
    id_nivel_educacional = Column(Integer, ForeignKey("niveles_educacionales.id", ondelete="SET NULL"))
    estado = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# =========================
# USUARIOS
# =========================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    duracion = Column(Integer, default=20)
    pagina_inicio = Column(String(255), nullable=False)
    id_dashboard = Column(Integer, ForeignKey("dashboard_inicial.id", ondelete="SET NULL"))
    id_persona = Column(Integer, ForeignKey("personas.id", ondelete="SET NULL"))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# =========================
# ROLES Y MENÚS
# =========================
class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TipoMenu(Base):
    __tablename__ = "tipos_menu"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False, unique=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Menu(Base):
    __tablename__ = "menus"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    icono = Column(String(50))
    id_tipo_menu = Column(Integer, ForeignKey("tipos_menu.id", ondelete="SET NULL"))
    id_padre = Column(Integer, ForeignKey("menus.id", ondelete="SET NULL"))
    url = Column(String(255))
    descripcion = Column(String(255))
    token = Column(String(255), unique=True)
    orden = Column(Integer)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    padre = relationship("Menu", remote_side=[id])


class MenuRol(Base):
    __tablename__ = "menu_rol"

    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmpresaUsuarioRol(Base):
    __tablename__ = "empresa_usuario_rol"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    id_rol = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(Boolean, default=True)


# =========================
# ACCESO, AUDITORÍA Y TOKENS
# =========================
class ConfiguracionEmpresa(Base):
    __tablename__ = "configuracion_empresa"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    clave = Column(String(255), primary_key=True)
    valor = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="SET NULL"))
    tabla_afectada = Column(String(255), nullable=False)
    accion = Column(String(255), nullable=False)
    id_registro = Column(Integer)
    datos_antes = Column(Text)
    datos_despues = Column(Text)
    direccion_ip = Column(String(45))


class Acceso(Base):
    __tablename__ = "acceso"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="SET NULL"))
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    fecha_vencimiento = Column(DateTime, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# =========================
# MENÚS ESPECÍFICOS Y RELACIONES
# =========================
class MenuPublico(Base):
    __tablename__ = "menus_publicos"

    id = Column(Integer, primary_key=True, index=True)
    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"))
    token = Column(String(255), unique=True)
    fecha_expiracion = Column(DateTime)
    estado = Column(Boolean, default=True)


class MenuTipoEmpresa(Base):
    __tablename__ = "menu_tipo_empresa"

    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)
    id_tipo_empresa = Column(Integer, ForeignKey("tipos_empresa.id", ondelete="CASCADE"), primary_key=True)


# =========================
# PARÁMETROS DEL SISTEMA
# =========================
class ParametroSistema(Base):
    __tablename__ = "parametro_sistema"

    id = Column(Integer, primary_key=True, index=True)
    clave = Column(String(255), unique=True, nullable=False)
    valor = Column(Text)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    estado = Column(Boolean, default=True)


class LogAcceso(Base):
    __tablename__ = "logs_acceso"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id", ondelete="SET NULL"))
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="SET NULL"))
    username = Column(String(255), nullable=False)
    exito = Column(Boolean, nullable=False)
    mensaje = Column(Text, nullable=False)
    ip = Column(String(45))
    user_agent = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)


# =========================
# TABLAS MÓDULOS
# =========================
class Modulo(Base):
    __tablename__ = "modulos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EmpresaModulo(Base):
    __tablename__ = "empresa_modulo"

    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), primary_key=True)
    id_modulo = Column(Integer, ForeignKey("modulos.id", ondelete="CASCADE"), primary_key=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ModuloMenu(Base):
    __tablename__ = "modulo_menu"

    id_modulo = Column(Integer, ForeignKey("modulos.id", ondelete="CASCADE"), primary_key=True)
    id_menu = Column(Integer, ForeignKey("menus.id", ondelete="CASCADE"), primary_key=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# =========================
# VADEMÉCUM
# =========================
class VademecumLaboratorio(Base):
    __tablename__ = "vademecum_laboratorios"

    id_laboratorio = Column(Integer, primary_key=True, index=True)
    nombre_laboratorio = Column(String(100), nullable=False)
    pais = Column(String(50))
    direccion = Column(String(255))
    sitio_web = Column(String(100))
    contacto = Column(String(100))
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumCategoriaTerapeutica(Base):
    __tablename__ = "vademecum_categorias_terapeuticas"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nombre_categoria = Column(String(100), nullable=False)
    descripcion = Column(Text)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumMedicamento(Base):
    __tablename__ = "vademecum_medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True)
    nombre_comercial = Column(String(100), nullable=False)
    nombre_generico = Column(String(100), nullable=False)
    forma_farmaceutica = Column(String(50))
    concentracion = Column(String(50))
    id_laboratorio = Column(Integer, ForeignKey("vademecum_laboratorios.id_laboratorio", ondelete="CASCADE"), nullable=False)
    registro_sanitario = Column(String(50))
    clasificacion = Column(String(50))
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumIndicacion(Base):
    __tablename__ = "vademecum_indicaciones"

    id_indicacion = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    indicacion = Column(Text, nullable=False)
    mecanismo_accion = Column(Text)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumPosologia(Base):
    __tablename__ = "vademecum_posologias"

    id_posologia = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    dosis = Column(String(100))
    via_administracion = Column(String(50))
    edad_minima = Column(Integer)
    edad_maxima = Column(Integer)
    instrucciones_especiales = Column(Text)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumContraindicacion(Base):
    __tablename__ = "vademecum_contraindicaciones"

    id_contraindicacion = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    contraindicacion = Column(Text, nullable=False)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumInteraccion(Base):
    __tablename__ = "vademecum_interacciones"

    id_interaccion = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    id_medicamento_interactua = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="SET NULL"))
    descripcion_interaccion = Column(Text, nullable=False)
    tipo_interaccion = Column(String(50))
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumEfectoSecundario(Base):
    __tablename__ = "vademecum_efectos_secundarios"

    id_efecto = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    efecto_secundario = Column(Text, nullable=False)
    frecuencia = Column(String(50))
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumPresentacion(Base):
    __tablename__ = "vademecum_presentaciones"

    id_presentacion = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    formato = Column(String(100))
    concentracion = Column(String(50))
    codigo_barras = Column(String(50))
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumFarmacocinetica(Base):
    __tablename__ = "vademecum_farmacocinetica"

    id_farmacocinetica = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), nullable=False)
    absorcion = Column(Text)
    distribucion = Column(Text)
    metabolismo = Column(Text)
    eliminacion = Column(Text)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumProtocoloClinico(Base):
    __tablename__ = "vademecum_protocolos_clinicos"

    id_protocolo = Column(Integer, primary_key=True, index=True)
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento"))
    protocolo_clinico = Column(Text, nullable=False)
    descripcion = Column(Text)
    fuente = Column(String(100))
    fecha_actualizacion = Column(Date)
    id_empresa = Column(Integer, ForeignKey("empresas.id", ondelete="CASCADE"), nullable=False)
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)


class VademecumMedicamentoCategoria(Base):
    __tablename__ = "vademecum_medicamento_categoria"

    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="CASCADE"), primary_key=True)
    id_categoria = Column(Integer, ForeignKey("vademecum_categorias_terapeuticas.id_categoria", ondelete="CASCADE"), primary_key=True)


class Imagen(Base):
    __tablename__ = "imagenes"

    id_imagen = Column(Integer, primary_key=True, index=True)
    url = Column(String(255), nullable=False)
    descripcion = Column(String(255))
    id_medicamento = Column(Integer, ForeignKey("vademecum_medicamentos.id_medicamento", ondelete="SET NULL"))
    id_laboratorio = Column(Integer, ForeignKey("vademecum_laboratorios.id_laboratorio", ondelete="SET NULL"))
    id_persona = Column(Integer, ForeignKey("personas.id", ondelete="SET NULL"))
    estado = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_edicion = Column(DateTime)

    __table_args__ = (
        CheckConstraint(
            "((id_medicamento IS NOT NULL AND id_laboratorio IS NULL AND id_persona IS NULL) "
            "OR (id_medicamento IS NULL AND id_laboratorio IS NOT NULL AND id_persona IS NULL) "
            "OR (id_medicamento IS NULL AND id_laboratorio IS NULL AND id_persona IS NOT NULL))",
            name="chk_imagen_ref"
        ),
    )

# app/models/medicamento.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class Vademecum(Base):
    __tablename__ = "vw_medicamentos_completos"

    url_logo = Column(String, nullable=True)
    nombre_laboratorio = Column(String, nullable=False)
    id_medicamento = Column(Integer, primary_key=True, nullable=False)  # Definir como clave primaria
    url_medicamento = Column(String, nullable=True)
    nombre_comercial = Column(String, nullable=False)
    nombre_generico = Column(String, nullable=True)
    forma_farmaceutica = Column(String, nullable=True)
    concentracion = Column(String, nullable=True)
    nombre_categoria = Column(String, nullable=True)
    estado = Column(Boolean, nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
    id_empresa = Column(Integer, nullable=True)  # Asumiendo que está en la vista

    __table_args__ = {'schema': 'public'}