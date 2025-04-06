from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

class Empresa(Base):
    __tablename__ = 'empresa'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)

class Acceso(Base):
    __tablename__ = 'acceso'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresa.id'), nullable=True)
    fecha_ingreso = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_vencimiento = Column(TIMESTAMP, nullable=False)
    token = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.current_timestamp())
    fecha_modificacion = Column(TIMESTAMP, onupdate=func.current_timestamp())
    usuario = relationship('Usuario', backref='accesos')  # Relación con la tabla usuario
    empresa = relationship('Empresa', backref='accesos')  # Relación con la tabla usuario