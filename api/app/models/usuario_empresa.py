from datetime import datetime
from sqlalchemy import Column, Integer, Date, TIMESTAMP, ForeignKey, SmallInteger, String

from sqlalchemy.sql import func
from app.database import Base



class UsuarioEmpresa(Base):
    __tablename__ = 'usuario_empresa'

    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete="CASCADE"), primary_key=True)
    empresa_id = Column(Integer, ForeignKey('empresa.id', ondelete="CASCADE"), primary_key=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

