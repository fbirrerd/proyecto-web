from sqlalchemy import Column, Integer, SmallInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy.dialects.postgresql import ENUM

class TipoMenu(enum.Enum):
    URL = "url"
    FORM = "formulario"
    OTRO = "otro"

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=True)
    nombre = Column(String(255), nullable=False)
    tipo = Column(ENUM(TipoMenu, name="tipo_menu"), nullable=False)
    valor = Column(String(255), nullable=False)
    icono = Column(String(255), nullable=True)
    orden = Column(Integer)
    padre_id = Column(Integer, ForeignKey("menu.id", ondelete="SET NULL"), nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default="now()")
    fecha_modificacion = Column(TIMESTAMP, server_default="now()")
    estado = Column(SmallInteger, default=0)

    hijos = relationship("Menu", backref="padre", remote_side=[id])
